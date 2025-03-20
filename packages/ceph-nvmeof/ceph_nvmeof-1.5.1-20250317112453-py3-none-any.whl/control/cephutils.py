#
#  Copyright (c) 2024 International Business Machines
#  All rights reserved.
#
#  SPDX-License-Identifier: LGPL-3.0-or-later
#
#  Authors: gbregman@ibm.com
#
import errno
import rbd
import rados
import time
import json
from .utils import GatewayLogger


class CephUtils:
    """Miscellaneous functions which connect to Ceph
    """

    def __init__(self, config):
        self.logger = GatewayLogger(config).logger
        self.ceph_conf = config.get_with_default("ceph", "config_file", "/etc/ceph/ceph.conf")
        self.rados_id = config.get_with_default("ceph", "id", "")
        self.anagroup_list = []
        self.rebalance_supported = False
        self.rebalance_ana_group = 0
        self.num_gws = 0
        self.last_sent = time.time()

    def execute_ceph_monitor_command(self, cmd):
        self.logger.debug(f"Execute monitor command: {cmd}")
        with rados.Rados(conffile=self.ceph_conf, rados_id=self.rados_id) as cluster:
            rply = cluster.mon_command(cmd, b'')
            self.logger.debug(f"Monitor reply: {rply}")
            return rply

    def get_gw_id_owner_ana_group(self, pool, group, anagrp):
        str = '{' + f'"prefix":"nvme-gw show", "pool":"{pool}", "group":"{group}"' + '}'
        self.logger.debug(f"nvme-show string: {str}")
        rply = self.execute_ceph_monitor_command(str)
        self.logger.debug(f"reply \"{rply}\"")
        conv_str = rply[1].decode()
        data = json.loads(conv_str)

        # Find the gw-id that contains "2: ACTIVE" in "ana states"
        gw_id = None
        comp_str = f"{anagrp}: ACTIVE"
        for gateway in data["Created Gateways:"]:
            if comp_str in gateway["ana states"]:
                gw_id = gateway["gw-id"]
                self.logger.debug(f"found gw owner of anagrp {anagrp}: gw {gw_id}")
                break
        return gw_id

    def is_rebalance_supported(self):
        return self.rebalance_supported

    def get_rebalance_ana_group(self):
        return self.rebalance_ana_group

    def get_num_gws(self):
        return self.num_gws

    def get_number_created_gateways(self, pool, group, caching=True):
        now = time.time()
        if caching and ((now - self.last_sent) < 10) and self.anagroup_list:
            self.logger.info(f"Caching response of the monitor: {self.anagroup_list}")
            return self.anagroup_list
        else:
            try:
                self.anagroup_list = []
                self.last_sent = now
                str = '{' + f'"prefix":"nvme-gw show", "pool":"{pool}", "group":"{group}"' + '}'
                self.logger.debug(f"nvme-show string: {str}")
                rply = self.execute_ceph_monitor_command(str)
                self.logger.debug(f"reply \"{rply}\"")
                conv_str = rply[1].decode()
                pos = conv_str.find('"LB"')
                if pos != -1:
                    data = json.loads(conv_str)
                    self.rebalance_supported = True
                    self.rebalance_ana_group = data.get("rebalance_ana_group", None)
                    self.num_gws = data.get("num gws", None)
                    self.logger.info(f"Rebalance ana_group: {self.rebalance_ana_group}, "
                                     f"num-gws: {self.num_gws}")
                else:
                    self.rebalance_supported = False
                pos = conv_str.find("[")
                if pos != -1:
                    new_str = conv_str[pos + len("["):]
                    pos = new_str.find("]")
                    new_str = new_str[: pos].strip()
                    int_str_list = new_str.split(' ')
                    self.logger.debug(f"new_str : {new_str}")
                    for x in int_str_list:
                        self.anagroup_list.append(int(x))
                    self.logger.info(f"ANA group list: {self.anagroup_list}")
                else:
                    self.logger.warning("GWs not found")

            except Exception:
                self.logger.exception("Failure get number created gateways")
                self.anagroup_list = []

            return self.anagroup_list

    def fetch_and_display_ceph_version(self):
        try:
            rply = self.execute_ceph_monitor_command('{"prefix":"mon versions"}')
            ceph_ver = rply[1].decode().removeprefix("{").strip().split(":")[0]
            ceph_ver = ceph_ver.removeprefix('"').removesuffix('"')
            ceph_ver = ceph_ver.removeprefix("ceph version ")
            self.logger.info(f"Connected to Ceph with version \"{ceph_ver}\"")
        except Exception:
            self.logger.exception("Failure fetching Ceph version")
            pass

    def fetch_ceph_fsid(self) -> str:
        fsid = None
        try:
            with rados.Rados(conffile=self.ceph_conf, rados_id=self.rados_id) as cluster:
                fsid = cluster.get_fsid()
        except Exception:
            self.logger.exception("Failure fetching Ceph fsid")

        return fsid

    def pool_exists(self, pool) -> bool:
        try:
            with rados.Rados(conffile=self.ceph_conf, rados_id=self.rados_id) as cluster:
                if cluster.pool_exists(pool):
                    return True
        except Exception:
            self.logger.exception(f"Can't check if pool {pool} exists, assume it does")
            return True

        return False

    def service_daemon_register(self, cluster, metadata):
        try:
            if cluster:              # rados client
                daemon_name = metadata['id']
                cluster.service_daemon_register("nvmeof", daemon_name, metadata)
                self.logger.info(f"Registered {daemon_name} to service_map!")
        except Exception:
            self.logger.exception("Can't register daemon to service_map!")

    def service_daemon_update(self, cluster, status_buffer):
        try:
            if cluster and status_buffer:
                cluster.service_daemon_update(status_buffer)
        except Exception:
            self.logger.exception("Can't update daemon status to service_map!")

    def create_image(self, pool_name, image_name, size) -> bool:
        # Check for pool existence in advance as we don't create it if it's not there
        if not self.pool_exists(pool_name):
            raise rbd.ImageNotFound(f"Pool {pool_name} doesn't exist", errno=errno.ENODEV)

        image_exists = False
        try:
            image_size = self.get_image_size(pool_name, image_name)
            image_exists = True
        except rbd.ImageNotFound:
            self.logger.debug(f"Image {pool_name}/{image_name} doesn't exist, will "
                              f"create it using size {size}")
            pass

        if image_exists:
            if image_size != size:
                raise rbd.ImageExists(f"Image {pool_name}/{image_name} already exists with "
                                      f"a size of {image_size} bytes which differs from the "
                                      f"requested size of {size} bytes",
                                      errno=errno.EEXIST)
            return False    # Image exists with an idetical size, there is nothing to do here

        with rados.Rados(conffile=self.ceph_conf, rados_id=self.rados_id) as cluster:
            with cluster.open_ioctx(pool_name) as ioctx:
                rbd_inst = rbd.RBD()
                try:
                    rbd_inst.create(ioctx, image_name, size)
                except rbd.ImageExists:
                    self.logger.exception(f"Image {pool_name}/{image_name} was created just now")
                    raise rbd.ImageExists(f"Image {pool_name}/{image_name} was just created by "
                                          f"someone else, please retry",
                                          errno=errno.EAGAIN)
                except Exception:
                    self.logger.exception(f"Can't create image {pool_name}/{image_name}")
                    raise

        return True

    def delete_image(self, pool_name, image_name) -> bool:
        if not pool_name and not image_name:
            return True

        if not self.pool_exists(pool_name):
            self.logger.warning(f"Pool {pool_name} doesn't exist, can't delete RBD image")
            return True

        with rados.Rados(conffile=self.ceph_conf, rados_id=self.rados_id) as cluster:
            with cluster.open_ioctx(pool_name) as ioctx:
                rbd_inst = rbd.RBD()
                try:
                    rbd_inst.remove(ioctx, image_name)
                except rbd.ImageNotFound:
                    self.logger.warning(f"Image {pool_name}/{image_name} is not found")
                    return True
                except (rbd.ImageBusy, rbd.ImageHasSnapshots):
                    self.logger.exception(f"Can't delete image {pool_name}/{image_name}")
                    return False

        return True

    def get_image_size(self, pool_name: str, image_name: str) -> int:
        image_size = 0
        if not self.pool_exists(pool_name):
            raise rbd.ImageNotFound(f"Pool {pool_name} doesn't exist", errno=errno.ENODEV)

        with rados.Rados(conffile=self.ceph_conf, rados_id=self.rados_id) as cluster:
            with cluster.open_ioctx(pool_name) as ioctx:
                rbd.RBD()
                try:
                    with rbd.Image(ioctx, image_name) as img:
                        image_size = img.size()
                except rbd.ImageNotFound:
                    raise rbd.ImageNotFound(f"Image {pool_name}/{image_name} doesn't exist",
                                            errno=errno.ENODEV)
                except Exception as ex:
                    self.logger.exception(f"Error while trying to get the size of image "
                                          f"{pool_name}/{image_name}")
                    raise ex

        return image_size

    def does_image_exist(self, pool_name: str, image_name: str) -> bool:
        try:
            self.get_image_size(pool_name, image_name)
            return True
        except rbd.ImageNotFound:
            return False
        except Exception:
            self.logger.exception("Failure getting image size")
        return False

    def get_rbd_exception_details(self, ex):
        ex_details = (None, None)
        if rbd.OSError in type(ex).__bases__:
            msg = str(ex).strip()
            # remove the [errno] part
            if msg.startswith("["):
                pos = msg.find("]")
                if pos >= 0:
                    msg = msg[pos + 1:].strip()
            ex_details = (ex.errno, msg)
        return ex_details
