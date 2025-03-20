from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DEBUG: LogLevel
DESCRIPTOR: _descriptor.FileDescriptor
ERROR: LogLevel
INACCESSIBLE: ana_state
INFO: LogLevel
NON_OPTIMIZED: ana_state
NOTICE: LogLevel
OPTIMIZED: ana_state
UNSET: ana_state
WARNING: LogLevel
critical: GwLogLevel
debug: GwLogLevel
error: GwLogLevel
info: GwLogLevel
ipv4: AddressFamily
ipv6: AddressFamily
notset: GwLogLevel
warning: GwLogLevel

class add_host_req(_message.Message):
    __slots__ = ["dhchap_key", "host_nqn", "key_encrypted", "psk", "psk_encrypted", "subsystem_nqn"]
    DHCHAP_KEY_FIELD_NUMBER: _ClassVar[int]
    HOST_NQN_FIELD_NUMBER: _ClassVar[int]
    KEY_ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    PSK_ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    PSK_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    dhchap_key: str
    host_nqn: str
    key_encrypted: bool
    psk: str
    psk_encrypted: bool
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., host_nqn: _Optional[str] = ..., psk: _Optional[str] = ..., dhchap_key: _Optional[str] = ..., psk_encrypted: bool = ..., key_encrypted: bool = ...) -> None: ...

class ana_group_state(_message.Message):
    __slots__ = ["grp_id", "state"]
    GRP_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    grp_id: int
    state: ana_state
    def __init__(self, grp_id: _Optional[int] = ..., state: _Optional[_Union[ana_state, str]] = ...) -> None: ...

class ana_info(_message.Message):
    __slots__ = ["states"]
    STATES_FIELD_NUMBER: _ClassVar[int]
    states: _containers.RepeatedCompositeFieldContainer[nqn_ana_states]
    def __init__(self, states: _Optional[_Iterable[_Union[nqn_ana_states, _Mapping]]] = ...) -> None: ...

class change_host_key_req(_message.Message):
    __slots__ = ["dhchap_key", "host_nqn", "subsystem_nqn"]
    DHCHAP_KEY_FIELD_NUMBER: _ClassVar[int]
    HOST_NQN_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    dhchap_key: str
    host_nqn: str
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., host_nqn: _Optional[str] = ..., dhchap_key: _Optional[str] = ...) -> None: ...

class change_subsystem_key_req(_message.Message):
    __slots__ = ["dhchap_key", "subsystem_nqn"]
    DHCHAP_KEY_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    dhchap_key: str
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., dhchap_key: _Optional[str] = ...) -> None: ...

class cli_version(_message.Message):
    __slots__ = ["error_message", "status", "version"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    status: int
    version: str
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class connection(_message.Message):
    __slots__ = ["adrfam", "connected", "controller_id", "nqn", "qpairs_count", "secure", "traddr", "trsvcid", "trtype", "use_dhchap", "use_psk"]
    ADRFAM_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_ID_FIELD_NUMBER: _ClassVar[int]
    NQN_FIELD_NUMBER: _ClassVar[int]
    QPAIRS_COUNT_FIELD_NUMBER: _ClassVar[int]
    SECURE_FIELD_NUMBER: _ClassVar[int]
    TRADDR_FIELD_NUMBER: _ClassVar[int]
    TRSVCID_FIELD_NUMBER: _ClassVar[int]
    TRTYPE_FIELD_NUMBER: _ClassVar[int]
    USE_DHCHAP_FIELD_NUMBER: _ClassVar[int]
    USE_PSK_FIELD_NUMBER: _ClassVar[int]
    adrfam: AddressFamily
    connected: bool
    controller_id: int
    nqn: str
    qpairs_count: int
    secure: bool
    traddr: str
    trsvcid: int
    trtype: str
    use_dhchap: bool
    use_psk: bool
    def __init__(self, nqn: _Optional[str] = ..., traddr: _Optional[str] = ..., trsvcid: _Optional[int] = ..., trtype: _Optional[str] = ..., adrfam: _Optional[_Union[AddressFamily, str]] = ..., connected: bool = ..., qpairs_count: _Optional[int] = ..., controller_id: _Optional[int] = ..., secure: bool = ..., use_psk: bool = ..., use_dhchap: bool = ...) -> None: ...

class connections_info(_message.Message):
    __slots__ = ["connections", "error_message", "status", "subsystem_nqn"]
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[connection]
    error_message: str
    status: int
    subsystem_nqn: str
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., subsystem_nqn: _Optional[str] = ..., connections: _Optional[_Iterable[_Union[connection, _Mapping]]] = ...) -> None: ...

class create_listener_req(_message.Message):
    __slots__ = ["adrfam", "host_name", "nqn", "secure", "traddr", "trsvcid", "verify_host_name"]
    ADRFAM_FIELD_NUMBER: _ClassVar[int]
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    NQN_FIELD_NUMBER: _ClassVar[int]
    SECURE_FIELD_NUMBER: _ClassVar[int]
    TRADDR_FIELD_NUMBER: _ClassVar[int]
    TRSVCID_FIELD_NUMBER: _ClassVar[int]
    VERIFY_HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    adrfam: AddressFamily
    host_name: str
    nqn: str
    secure: bool
    traddr: str
    trsvcid: int
    verify_host_name: bool
    def __init__(self, nqn: _Optional[str] = ..., host_name: _Optional[str] = ..., traddr: _Optional[str] = ..., adrfam: _Optional[_Union[AddressFamily, str]] = ..., trsvcid: _Optional[int] = ..., secure: bool = ..., verify_host_name: bool = ...) -> None: ...

class create_subsystem_req(_message.Message):
    __slots__ = ["dhchap_key", "enable_ha", "key_encrypted", "max_namespaces", "no_group_append", "serial_number", "subsystem_nqn"]
    DHCHAP_KEY_FIELD_NUMBER: _ClassVar[int]
    ENABLE_HA_FIELD_NUMBER: _ClassVar[int]
    KEY_ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    MAX_NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    NO_GROUP_APPEND_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    dhchap_key: str
    enable_ha: bool
    key_encrypted: bool
    max_namespaces: int
    no_group_append: bool
    serial_number: str
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., serial_number: _Optional[str] = ..., max_namespaces: _Optional[int] = ..., enable_ha: bool = ..., no_group_append: bool = ..., dhchap_key: _Optional[str] = ..., key_encrypted: bool = ...) -> None: ...

class delete_listener_req(_message.Message):
    __slots__ = ["adrfam", "force", "host_name", "nqn", "traddr", "trsvcid"]
    ADRFAM_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    NQN_FIELD_NUMBER: _ClassVar[int]
    TRADDR_FIELD_NUMBER: _ClassVar[int]
    TRSVCID_FIELD_NUMBER: _ClassVar[int]
    adrfam: AddressFamily
    force: bool
    host_name: str
    nqn: str
    traddr: str
    trsvcid: int
    def __init__(self, nqn: _Optional[str] = ..., host_name: _Optional[str] = ..., traddr: _Optional[str] = ..., adrfam: _Optional[_Union[AddressFamily, str]] = ..., trsvcid: _Optional[int] = ..., force: bool = ...) -> None: ...

class delete_subsystem_req(_message.Message):
    __slots__ = ["force", "subsystem_nqn"]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    force: bool
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., force: bool = ...) -> None: ...

class disable_spdk_nvmf_logs_req(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class gateway_info(_message.Message):
    __slots__ = ["addr", "bool_status", "cli_version", "error_message", "group", "hostname", "load_balancing_group", "max_hosts", "max_hosts_per_subsystem", "max_namespaces", "max_namespaces_per_subsystem", "max_subsystems", "name", "port", "spdk_version", "status", "version"]
    ADDR_FIELD_NUMBER: _ClassVar[int]
    BOOL_STATUS_FIELD_NUMBER: _ClassVar[int]
    CLI_VERSION_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    LOAD_BALANCING_GROUP_FIELD_NUMBER: _ClassVar[int]
    MAX_HOSTS_FIELD_NUMBER: _ClassVar[int]
    MAX_HOSTS_PER_SUBSYSTEM_FIELD_NUMBER: _ClassVar[int]
    MAX_NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    MAX_NAMESPACES_PER_SUBSYSTEM_FIELD_NUMBER: _ClassVar[int]
    MAX_SUBSYSTEMS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    SPDK_VERSION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    addr: str
    bool_status: bool
    cli_version: str
    error_message: str
    group: str
    hostname: str
    load_balancing_group: int
    max_hosts: int
    max_hosts_per_subsystem: int
    max_namespaces: int
    max_namespaces_per_subsystem: int
    max_subsystems: int
    name: str
    port: str
    spdk_version: str
    status: int
    version: str
    def __init__(self, cli_version: _Optional[str] = ..., version: _Optional[str] = ..., name: _Optional[str] = ..., group: _Optional[str] = ..., addr: _Optional[str] = ..., port: _Optional[str] = ..., bool_status: bool = ..., status: _Optional[int] = ..., error_message: _Optional[str] = ..., spdk_version: _Optional[str] = ..., load_balancing_group: _Optional[int] = ..., hostname: _Optional[str] = ..., max_subsystems: _Optional[int] = ..., max_namespaces: _Optional[int] = ..., max_hosts_per_subsystem: _Optional[int] = ..., max_namespaces_per_subsystem: _Optional[int] = ..., max_hosts: _Optional[int] = ...) -> None: ...

class gateway_listener_info(_message.Message):
    __slots__ = ["lb_states", "listener"]
    LB_STATES_FIELD_NUMBER: _ClassVar[int]
    LISTENER_FIELD_NUMBER: _ClassVar[int]
    lb_states: _containers.RepeatedCompositeFieldContainer[ana_group_state]
    listener: listener_info
    def __init__(self, listener: _Optional[_Union[listener_info, _Mapping]] = ..., lb_states: _Optional[_Iterable[_Union[ana_group_state, _Mapping]]] = ...) -> None: ...

class gateway_listeners_info(_message.Message):
    __slots__ = ["error_message", "gw_listeners", "status"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    GW_LISTENERS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    gw_listeners: _containers.RepeatedCompositeFieldContainer[gateway_listener_info]
    status: int
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., gw_listeners: _Optional[_Iterable[_Union[gateway_listener_info, _Mapping]]] = ...) -> None: ...

class gateway_log_level_info(_message.Message):
    __slots__ = ["error_message", "log_level", "status"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    log_level: GwLogLevel
    status: int
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., log_level: _Optional[_Union[GwLogLevel, str]] = ...) -> None: ...

class get_gateway_info_req(_message.Message):
    __slots__ = ["cli_version"]
    CLI_VERSION_FIELD_NUMBER: _ClassVar[int]
    cli_version: str
    def __init__(self, cli_version: _Optional[str] = ...) -> None: ...

class get_gateway_log_level_req(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class get_spdk_nvmf_log_flags_and_level_req(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class get_subsystems_req(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class gw_version(_message.Message):
    __slots__ = ["error_message", "status", "version"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    status: int
    version: str
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class host(_message.Message):
    __slots__ = ["nqn", "use_dhchap", "use_psk"]
    NQN_FIELD_NUMBER: _ClassVar[int]
    USE_DHCHAP_FIELD_NUMBER: _ClassVar[int]
    USE_PSK_FIELD_NUMBER: _ClassVar[int]
    nqn: str
    use_dhchap: bool
    use_psk: bool
    def __init__(self, nqn: _Optional[str] = ..., use_psk: bool = ..., use_dhchap: bool = ...) -> None: ...

class hosts_info(_message.Message):
    __slots__ = ["allow_any_host", "error_message", "hosts", "status", "subsystem_nqn"]
    ALLOW_ANY_HOST_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    allow_any_host: bool
    error_message: str
    hosts: _containers.RepeatedCompositeFieldContainer[host]
    status: int
    subsystem_nqn: str
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., allow_any_host: bool = ..., subsystem_nqn: _Optional[str] = ..., hosts: _Optional[_Iterable[_Union[host, _Mapping]]] = ...) -> None: ...

class list_connections_req(_message.Message):
    __slots__ = ["subsystem"]
    SUBSYSTEM_FIELD_NUMBER: _ClassVar[int]
    subsystem: str
    def __init__(self, subsystem: _Optional[str] = ...) -> None: ...

class list_hosts_req(_message.Message):
    __slots__ = ["subsystem"]
    SUBSYSTEM_FIELD_NUMBER: _ClassVar[int]
    subsystem: str
    def __init__(self, subsystem: _Optional[str] = ...) -> None: ...

class list_listeners_req(_message.Message):
    __slots__ = ["subsystem"]
    SUBSYSTEM_FIELD_NUMBER: _ClassVar[int]
    subsystem: str
    def __init__(self, subsystem: _Optional[str] = ...) -> None: ...

class list_namespaces_req(_message.Message):
    __slots__ = ["nsid", "subsystem", "uuid"]
    NSID_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    nsid: int
    subsystem: str
    uuid: str
    def __init__(self, subsystem: _Optional[str] = ..., nsid: _Optional[int] = ..., uuid: _Optional[str] = ...) -> None: ...

class list_subsystems_req(_message.Message):
    __slots__ = ["serial_number", "subsystem_nqn"]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    serial_number: str
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., serial_number: _Optional[str] = ...) -> None: ...

class listen_address(_message.Message):
    __slots__ = ["adrfam", "secure", "traddr", "transport", "trsvcid", "trtype"]
    ADRFAM_FIELD_NUMBER: _ClassVar[int]
    SECURE_FIELD_NUMBER: _ClassVar[int]
    TRADDR_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    TRSVCID_FIELD_NUMBER: _ClassVar[int]
    TRTYPE_FIELD_NUMBER: _ClassVar[int]
    adrfam: str
    secure: bool
    traddr: str
    transport: str
    trsvcid: str
    trtype: str
    def __init__(self, trtype: _Optional[str] = ..., adrfam: _Optional[str] = ..., traddr: _Optional[str] = ..., trsvcid: _Optional[str] = ..., transport: _Optional[str] = ..., secure: bool = ...) -> None: ...

class listener_info(_message.Message):
    __slots__ = ["adrfam", "host_name", "secure", "traddr", "trsvcid", "trtype"]
    ADRFAM_FIELD_NUMBER: _ClassVar[int]
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    SECURE_FIELD_NUMBER: _ClassVar[int]
    TRADDR_FIELD_NUMBER: _ClassVar[int]
    TRSVCID_FIELD_NUMBER: _ClassVar[int]
    TRTYPE_FIELD_NUMBER: _ClassVar[int]
    adrfam: AddressFamily
    host_name: str
    secure: bool
    traddr: str
    trsvcid: int
    trtype: str
    def __init__(self, host_name: _Optional[str] = ..., trtype: _Optional[str] = ..., adrfam: _Optional[_Union[AddressFamily, str]] = ..., traddr: _Optional[str] = ..., trsvcid: _Optional[int] = ..., secure: bool = ...) -> None: ...

class listeners_info(_message.Message):
    __slots__ = ["error_message", "listeners", "status"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LISTENERS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    listeners: _containers.RepeatedCompositeFieldContainer[listener_info]
    status: int
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., listeners: _Optional[_Iterable[_Union[listener_info, _Mapping]]] = ...) -> None: ...

class namespace(_message.Message):
    __slots__ = ["anagrpid", "auto_visible", "bdev_name", "hosts", "name", "nguid", "nonce", "nsid", "uuid"]
    ANAGRPID_FIELD_NUMBER: _ClassVar[int]
    AUTO_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    BDEV_NAME_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NGUID_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    NSID_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    anagrpid: int
    auto_visible: bool
    bdev_name: str
    hosts: _containers.RepeatedScalarFieldContainer[str]
    name: str
    nguid: str
    nonce: str
    nsid: int
    uuid: str
    def __init__(self, nsid: _Optional[int] = ..., name: _Optional[str] = ..., bdev_name: _Optional[str] = ..., nguid: _Optional[str] = ..., uuid: _Optional[str] = ..., anagrpid: _Optional[int] = ..., nonce: _Optional[str] = ..., auto_visible: bool = ..., hosts: _Optional[_Iterable[str]] = ...) -> None: ...

class namespace_add_host_req(_message.Message):
    __slots__ = ["host_nqn", "nsid", "subsystem_nqn"]
    HOST_NQN_FIELD_NUMBER: _ClassVar[int]
    NSID_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    host_nqn: str
    nsid: int
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., nsid: _Optional[int] = ..., host_nqn: _Optional[str] = ...) -> None: ...

class namespace_add_req(_message.Message):
    __slots__ = ["anagrpid", "block_size", "create_image", "force", "no_auto_visible", "nsid", "rbd_image_name", "rbd_pool_name", "size", "subsystem_nqn", "trash_image", "uuid"]
    ANAGRPID_FIELD_NUMBER: _ClassVar[int]
    BLOCK_SIZE_FIELD_NUMBER: _ClassVar[int]
    CREATE_IMAGE_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    NO_AUTO_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    NSID_FIELD_NUMBER: _ClassVar[int]
    RBD_IMAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    RBD_POOL_NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    TRASH_IMAGE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    anagrpid: int
    block_size: int
    create_image: bool
    force: bool
    no_auto_visible: bool
    nsid: int
    rbd_image_name: str
    rbd_pool_name: str
    size: int
    subsystem_nqn: str
    trash_image: bool
    uuid: str
    def __init__(self, rbd_pool_name: _Optional[str] = ..., rbd_image_name: _Optional[str] = ..., subsystem_nqn: _Optional[str] = ..., nsid: _Optional[int] = ..., block_size: _Optional[int] = ..., uuid: _Optional[str] = ..., anagrpid: _Optional[int] = ..., create_image: bool = ..., size: _Optional[int] = ..., force: bool = ..., no_auto_visible: bool = ..., trash_image: bool = ...) -> None: ...

class namespace_change_load_balancing_group_req(_message.Message):
    __slots__ = ["OBSOLETE_uuid", "anagrpid", "auto_lb_logic", "nsid", "subsystem_nqn"]
    ANAGRPID_FIELD_NUMBER: _ClassVar[int]
    AUTO_LB_LOGIC_FIELD_NUMBER: _ClassVar[int]
    NSID_FIELD_NUMBER: _ClassVar[int]
    OBSOLETE_UUID_FIELD_NUMBER: _ClassVar[int]
    OBSOLETE_uuid: str
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    anagrpid: int
    auto_lb_logic: bool
    nsid: int
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., nsid: _Optional[int] = ..., OBSOLETE_uuid: _Optional[str] = ..., anagrpid: _Optional[int] = ..., auto_lb_logic: bool = ...) -> None: ...

class namespace_change_visibility_req(_message.Message):
    __slots__ = ["auto_visible", "force", "nsid", "subsystem_nqn"]
    AUTO_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    NSID_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    auto_visible: bool
    force: bool
    nsid: int
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., nsid: _Optional[int] = ..., auto_visible: bool = ..., force: bool = ...) -> None: ...

class namespace_cli(_message.Message):
    __slots__ = ["auto_visible", "bdev_name", "block_size", "hosts", "load_balancing_group", "ns_subsystem_nqn", "nsid", "r_mbytes_per_second", "rbd_image_name", "rbd_image_size", "rbd_pool_name", "rw_ios_per_second", "rw_mbytes_per_second", "trash_image", "uuid", "w_mbytes_per_second"]
    AUTO_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    BDEV_NAME_FIELD_NUMBER: _ClassVar[int]
    BLOCK_SIZE_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    LOAD_BALANCING_GROUP_FIELD_NUMBER: _ClassVar[int]
    NSID_FIELD_NUMBER: _ClassVar[int]
    NS_SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    RBD_IMAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    RBD_IMAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    RBD_POOL_NAME_FIELD_NUMBER: _ClassVar[int]
    RW_IOS_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    RW_MBYTES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    R_MBYTES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    TRASH_IMAGE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    W_MBYTES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    auto_visible: bool
    bdev_name: str
    block_size: int
    hosts: _containers.RepeatedScalarFieldContainer[str]
    load_balancing_group: int
    ns_subsystem_nqn: str
    nsid: int
    r_mbytes_per_second: int
    rbd_image_name: str
    rbd_image_size: int
    rbd_pool_name: str
    rw_ios_per_second: int
    rw_mbytes_per_second: int
    trash_image: bool
    uuid: str
    w_mbytes_per_second: int
    def __init__(self, nsid: _Optional[int] = ..., bdev_name: _Optional[str] = ..., rbd_image_name: _Optional[str] = ..., rbd_pool_name: _Optional[str] = ..., load_balancing_group: _Optional[int] = ..., block_size: _Optional[int] = ..., rbd_image_size: _Optional[int] = ..., uuid: _Optional[str] = ..., rw_ios_per_second: _Optional[int] = ..., rw_mbytes_per_second: _Optional[int] = ..., r_mbytes_per_second: _Optional[int] = ..., w_mbytes_per_second: _Optional[int] = ..., auto_visible: bool = ..., hosts: _Optional[_Iterable[str]] = ..., ns_subsystem_nqn: _Optional[str] = ..., trash_image: bool = ...) -> None: ...

class namespace_delete_host_req(_message.Message):
    __slots__ = ["host_nqn", "nsid", "subsystem_nqn"]
    HOST_NQN_FIELD_NUMBER: _ClassVar[int]
    NSID_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    host_nqn: str
    nsid: int
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., nsid: _Optional[int] = ..., host_nqn: _Optional[str] = ...) -> None: ...

class namespace_delete_req(_message.Message):
    __slots__ = ["OBSOLETE_uuid", "i_am_sure", "nsid", "subsystem_nqn"]
    I_AM_SURE_FIELD_NUMBER: _ClassVar[int]
    NSID_FIELD_NUMBER: _ClassVar[int]
    OBSOLETE_UUID_FIELD_NUMBER: _ClassVar[int]
    OBSOLETE_uuid: str
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    i_am_sure: bool
    nsid: int
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., nsid: _Optional[int] = ..., OBSOLETE_uuid: _Optional[str] = ..., i_am_sure: bool = ...) -> None: ...

class namespace_get_io_stats_req(_message.Message):
    __slots__ = ["OBSOLETE_uuid", "nsid", "subsystem_nqn"]
    NSID_FIELD_NUMBER: _ClassVar[int]
    OBSOLETE_UUID_FIELD_NUMBER: _ClassVar[int]
    OBSOLETE_uuid: str
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    nsid: int
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., nsid: _Optional[int] = ..., OBSOLETE_uuid: _Optional[str] = ...) -> None: ...

class namespace_io_error(_message.Message):
    __slots__ = ["name", "value"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: int
    def __init__(self, name: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...

class namespace_io_stats_info(_message.Message):
    __slots__ = ["bdev_name", "bytes_read", "bytes_unmapped", "bytes_written", "copy_latency_ticks", "error_message", "io_error", "max_copy_latency_ticks", "max_read_latency_ticks", "max_unmap_latency_ticks", "max_write_latency_ticks", "min_copy_latency_ticks", "min_read_latency_ticks", "min_unmap_latency_ticks", "min_write_latency_ticks", "nsid", "num_read_ops", "num_unmap_ops", "num_write_ops", "read_latency_ticks", "status", "subsystem_nqn", "tick_rate", "ticks", "unmap_latency_ticks", "uuid", "write_latency_ticks"]
    BDEV_NAME_FIELD_NUMBER: _ClassVar[int]
    BYTES_READ_FIELD_NUMBER: _ClassVar[int]
    BYTES_UNMAPPED_FIELD_NUMBER: _ClassVar[int]
    BYTES_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    COPY_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IO_ERROR_FIELD_NUMBER: _ClassVar[int]
    MAX_COPY_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    MAX_READ_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    MAX_UNMAP_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    MAX_WRITE_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    MIN_COPY_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    MIN_READ_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    MIN_UNMAP_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    MIN_WRITE_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    NSID_FIELD_NUMBER: _ClassVar[int]
    NUM_READ_OPS_FIELD_NUMBER: _ClassVar[int]
    NUM_UNMAP_OPS_FIELD_NUMBER: _ClassVar[int]
    NUM_WRITE_OPS_FIELD_NUMBER: _ClassVar[int]
    READ_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    TICKS_FIELD_NUMBER: _ClassVar[int]
    TICK_RATE_FIELD_NUMBER: _ClassVar[int]
    UNMAP_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    WRITE_LATENCY_TICKS_FIELD_NUMBER: _ClassVar[int]
    bdev_name: str
    bytes_read: int
    bytes_unmapped: int
    bytes_written: int
    copy_latency_ticks: int
    error_message: str
    io_error: _containers.RepeatedCompositeFieldContainer[namespace_io_error]
    max_copy_latency_ticks: int
    max_read_latency_ticks: int
    max_unmap_latency_ticks: int
    max_write_latency_ticks: int
    min_copy_latency_ticks: int
    min_read_latency_ticks: int
    min_unmap_latency_ticks: int
    min_write_latency_ticks: int
    nsid: int
    num_read_ops: int
    num_unmap_ops: int
    num_write_ops: int
    read_latency_ticks: int
    status: int
    subsystem_nqn: str
    tick_rate: int
    ticks: int
    unmap_latency_ticks: int
    uuid: str
    write_latency_ticks: int
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., subsystem_nqn: _Optional[str] = ..., nsid: _Optional[int] = ..., uuid: _Optional[str] = ..., bdev_name: _Optional[str] = ..., tick_rate: _Optional[int] = ..., ticks: _Optional[int] = ..., bytes_read: _Optional[int] = ..., num_read_ops: _Optional[int] = ..., bytes_written: _Optional[int] = ..., num_write_ops: _Optional[int] = ..., bytes_unmapped: _Optional[int] = ..., num_unmap_ops: _Optional[int] = ..., read_latency_ticks: _Optional[int] = ..., max_read_latency_ticks: _Optional[int] = ..., min_read_latency_ticks: _Optional[int] = ..., write_latency_ticks: _Optional[int] = ..., max_write_latency_ticks: _Optional[int] = ..., min_write_latency_ticks: _Optional[int] = ..., unmap_latency_ticks: _Optional[int] = ..., max_unmap_latency_ticks: _Optional[int] = ..., min_unmap_latency_ticks: _Optional[int] = ..., copy_latency_ticks: _Optional[int] = ..., max_copy_latency_ticks: _Optional[int] = ..., min_copy_latency_ticks: _Optional[int] = ..., io_error: _Optional[_Iterable[_Union[namespace_io_error, _Mapping]]] = ...) -> None: ...

class namespace_resize_req(_message.Message):
    __slots__ = ["OBSOLETE_uuid", "new_size", "nsid", "subsystem_nqn"]
    NEW_SIZE_FIELD_NUMBER: _ClassVar[int]
    NSID_FIELD_NUMBER: _ClassVar[int]
    OBSOLETE_UUID_FIELD_NUMBER: _ClassVar[int]
    OBSOLETE_uuid: str
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    new_size: int
    nsid: int
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., nsid: _Optional[int] = ..., OBSOLETE_uuid: _Optional[str] = ..., new_size: _Optional[int] = ...) -> None: ...

class namespace_set_qos_req(_message.Message):
    __slots__ = ["OBSOLETE_uuid", "nsid", "r_mbytes_per_second", "rw_ios_per_second", "rw_mbytes_per_second", "subsystem_nqn", "w_mbytes_per_second"]
    NSID_FIELD_NUMBER: _ClassVar[int]
    OBSOLETE_UUID_FIELD_NUMBER: _ClassVar[int]
    OBSOLETE_uuid: str
    RW_IOS_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    RW_MBYTES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    R_MBYTES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    W_MBYTES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    nsid: int
    r_mbytes_per_second: int
    rw_ios_per_second: int
    rw_mbytes_per_second: int
    subsystem_nqn: str
    w_mbytes_per_second: int
    def __init__(self, subsystem_nqn: _Optional[str] = ..., nsid: _Optional[int] = ..., OBSOLETE_uuid: _Optional[str] = ..., rw_ios_per_second: _Optional[int] = ..., rw_mbytes_per_second: _Optional[int] = ..., r_mbytes_per_second: _Optional[int] = ..., w_mbytes_per_second: _Optional[int] = ...) -> None: ...

class namespace_set_rbd_trash_image_req(_message.Message):
    __slots__ = ["nsid", "subsystem_nqn", "trash_image"]
    NSID_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    TRASH_IMAGE_FIELD_NUMBER: _ClassVar[int]
    nsid: int
    subsystem_nqn: str
    trash_image: bool
    def __init__(self, subsystem_nqn: _Optional[str] = ..., nsid: _Optional[int] = ..., trash_image: bool = ...) -> None: ...

class namespaces_info(_message.Message):
    __slots__ = ["error_message", "namespaces", "status", "subsystem_nqn"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    namespaces: _containers.RepeatedCompositeFieldContainer[namespace_cli]
    status: int
    subsystem_nqn: str
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., subsystem_nqn: _Optional[str] = ..., namespaces: _Optional[_Iterable[_Union[namespace_cli, _Mapping]]] = ...) -> None: ...

class nqn_ana_states(_message.Message):
    __slots__ = ["nqn", "states"]
    NQN_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    nqn: str
    states: _containers.RepeatedCompositeFieldContainer[ana_group_state]
    def __init__(self, nqn: _Optional[str] = ..., states: _Optional[_Iterable[_Union[ana_group_state, _Mapping]]] = ...) -> None: ...

class nsid_status(_message.Message):
    __slots__ = ["error_message", "nsid", "status"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    NSID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    nsid: int
    status: int
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., nsid: _Optional[int] = ...) -> None: ...

class remove_host_req(_message.Message):
    __slots__ = ["host_nqn", "subsystem_nqn"]
    HOST_NQN_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    host_nqn: str
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ..., host_nqn: _Optional[str] = ...) -> None: ...

class req_status(_message.Message):
    __slots__ = ["error_message", "status"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    status: int
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ...) -> None: ...

class set_gateway_log_level_req(_message.Message):
    __slots__ = ["log_level"]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    log_level: GwLogLevel
    def __init__(self, log_level: _Optional[_Union[GwLogLevel, str]] = ...) -> None: ...

class set_spdk_nvmf_logs_req(_message.Message):
    __slots__ = ["log_level", "print_level"]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    PRINT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    log_level: LogLevel
    print_level: LogLevel
    def __init__(self, log_level: _Optional[_Union[LogLevel, str]] = ..., print_level: _Optional[_Union[LogLevel, str]] = ...) -> None: ...

class show_gateway_listeners_info_req(_message.Message):
    __slots__ = ["subsystem_nqn"]
    SUBSYSTEM_NQN_FIELD_NUMBER: _ClassVar[int]
    subsystem_nqn: str
    def __init__(self, subsystem_nqn: _Optional[str] = ...) -> None: ...

class spdk_log_flag_info(_message.Message):
    __slots__ = ["enabled", "name"]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    name: str
    def __init__(self, name: _Optional[str] = ..., enabled: bool = ...) -> None: ...

class spdk_nvmf_log_flags_and_level_info(_message.Message):
    __slots__ = ["error_message", "log_level", "log_print_level", "nvmf_log_flags", "status"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    LOG_PRINT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    NVMF_LOG_FLAGS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    log_level: LogLevel
    log_print_level: LogLevel
    nvmf_log_flags: _containers.RepeatedCompositeFieldContainer[spdk_log_flag_info]
    status: int
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., nvmf_log_flags: _Optional[_Iterable[_Union[spdk_log_flag_info, _Mapping]]] = ..., log_level: _Optional[_Union[LogLevel, str]] = ..., log_print_level: _Optional[_Union[LogLevel, str]] = ...) -> None: ...

class subsys_status(_message.Message):
    __slots__ = ["error_message", "nqn", "status"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    NQN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    nqn: str
    status: int
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., nqn: _Optional[str] = ...) -> None: ...

class subsystem(_message.Message):
    __slots__ = ["allow_any_host", "has_dhchap_key", "hosts", "listen_addresses", "max_cntlid", "max_namespaces", "min_cntlid", "model_number", "namespaces", "nqn", "serial_number", "subtype"]
    ALLOW_ANY_HOST_FIELD_NUMBER: _ClassVar[int]
    HAS_DHCHAP_KEY_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    LISTEN_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    MAX_CNTLID_FIELD_NUMBER: _ClassVar[int]
    MAX_NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    MIN_CNTLID_FIELD_NUMBER: _ClassVar[int]
    MODEL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    NQN_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SUBTYPE_FIELD_NUMBER: _ClassVar[int]
    allow_any_host: bool
    has_dhchap_key: bool
    hosts: _containers.RepeatedCompositeFieldContainer[host]
    listen_addresses: _containers.RepeatedCompositeFieldContainer[listen_address]
    max_cntlid: int
    max_namespaces: int
    min_cntlid: int
    model_number: str
    namespaces: _containers.RepeatedCompositeFieldContainer[namespace]
    nqn: str
    serial_number: str
    subtype: str
    def __init__(self, nqn: _Optional[str] = ..., subtype: _Optional[str] = ..., listen_addresses: _Optional[_Iterable[_Union[listen_address, _Mapping]]] = ..., hosts: _Optional[_Iterable[_Union[host, _Mapping]]] = ..., allow_any_host: bool = ..., serial_number: _Optional[str] = ..., model_number: _Optional[str] = ..., max_namespaces: _Optional[int] = ..., min_cntlid: _Optional[int] = ..., max_cntlid: _Optional[int] = ..., namespaces: _Optional[_Iterable[_Union[namespace, _Mapping]]] = ..., has_dhchap_key: bool = ...) -> None: ...

class subsystem_cli(_message.Message):
    __slots__ = ["allow_any_host", "created_without_key", "enable_ha", "has_dhchap_key", "max_cntlid", "max_namespaces", "min_cntlid", "model_number", "namespace_count", "nqn", "serial_number", "subtype"]
    ALLOW_ANY_HOST_FIELD_NUMBER: _ClassVar[int]
    CREATED_WITHOUT_KEY_FIELD_NUMBER: _ClassVar[int]
    ENABLE_HA_FIELD_NUMBER: _ClassVar[int]
    HAS_DHCHAP_KEY_FIELD_NUMBER: _ClassVar[int]
    MAX_CNTLID_FIELD_NUMBER: _ClassVar[int]
    MAX_NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    MIN_CNTLID_FIELD_NUMBER: _ClassVar[int]
    MODEL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_COUNT_FIELD_NUMBER: _ClassVar[int]
    NQN_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SUBTYPE_FIELD_NUMBER: _ClassVar[int]
    allow_any_host: bool
    created_without_key: bool
    enable_ha: bool
    has_dhchap_key: bool
    max_cntlid: int
    max_namespaces: int
    min_cntlid: int
    model_number: str
    namespace_count: int
    nqn: str
    serial_number: str
    subtype: str
    def __init__(self, nqn: _Optional[str] = ..., enable_ha: bool = ..., serial_number: _Optional[str] = ..., model_number: _Optional[str] = ..., min_cntlid: _Optional[int] = ..., max_cntlid: _Optional[int] = ..., namespace_count: _Optional[int] = ..., subtype: _Optional[str] = ..., max_namespaces: _Optional[int] = ..., has_dhchap_key: bool = ..., allow_any_host: bool = ..., created_without_key: bool = ...) -> None: ...

class subsystems_info(_message.Message):
    __slots__ = ["subsystems"]
    SUBSYSTEMS_FIELD_NUMBER: _ClassVar[int]
    subsystems: _containers.RepeatedCompositeFieldContainer[subsystem]
    def __init__(self, subsystems: _Optional[_Iterable[_Union[subsystem, _Mapping]]] = ...) -> None: ...

class subsystems_info_cli(_message.Message):
    __slots__ = ["error_message", "status", "subsystems"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUBSYSTEMS_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    status: int
    subsystems: _containers.RepeatedCompositeFieldContainer[subsystem_cli]
    def __init__(self, status: _Optional[int] = ..., error_message: _Optional[str] = ..., subsystems: _Optional[_Iterable[_Union[subsystem_cli, _Mapping]]] = ...) -> None: ...

class AddressFamily(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class LogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class GwLogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ana_state(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
