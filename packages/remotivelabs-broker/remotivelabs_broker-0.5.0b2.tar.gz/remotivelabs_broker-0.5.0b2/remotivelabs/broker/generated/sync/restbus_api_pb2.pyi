from remotivelabs.broker.generated.sync import common_pb2 as _common_pb2
from remotivelabs.broker.generated.sync.google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartOption(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    START_AFTER_INIT: _ClassVar[StartOption]
    STOPPED: _ClassVar[StartOption]
START_AFTER_INIT: StartOption
STOPPED: StartOption

class RestbusRequest(_message.Message):
    __slots__ = ("namespace",)
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    namespace: _common_pb2.NameSpace
    def __init__(self, namespace: _Optional[_Union[_common_pb2.NameSpace, _Mapping]] = ...) -> None: ...

class ConfigurationRequest(_message.Message):
    __slots__ = ("clientId", "namespace", "frames", "startOption")
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FRAMES_FIELD_NUMBER: _ClassVar[int]
    STARTOPTION_FIELD_NUMBER: _ClassVar[int]
    clientId: _common_pb2.ClientId
    namespace: _common_pb2.NameSpace
    frames: FrameConfigs
    startOption: StartOption
    def __init__(self, clientId: _Optional[_Union[_common_pb2.ClientId, _Mapping]] = ..., namespace: _Optional[_Union[_common_pb2.NameSpace, _Mapping]] = ..., frames: _Optional[_Union[FrameConfigs, _Mapping]] = ..., startOption: _Optional[_Union[StartOption, str]] = ...) -> None: ...

class FrameRemoveRequest(_message.Message):
    __slots__ = ("namespace", "frames")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FRAMES_FIELD_NUMBER: _ClassVar[int]
    namespace: _common_pb2.NameSpace
    frames: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, namespace: _Optional[_Union[_common_pb2.NameSpace, _Mapping]] = ..., frames: _Optional[_Iterable[str]] = ...) -> None: ...

class SignalUpdateRequest(_message.Message):
    __slots__ = ("namespace", "items")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    namespace: _common_pb2.NameSpace
    items: _containers.RepeatedCompositeFieldContainer[FrameWithSignals]
    def __init__(self, namespace: _Optional[_Union[_common_pb2.NameSpace, _Mapping]] = ..., items: _Optional[_Iterable[_Union[FrameWithSignals, _Mapping]]] = ...) -> None: ...

class ResetRequest(_message.Message):
    __slots__ = ("namespace", "busReset", "signalReset")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    BUSRESET_FIELD_NUMBER: _ClassVar[int]
    SIGNALRESET_FIELD_NUMBER: _ClassVar[int]
    namespace: _common_pb2.NameSpace
    busReset: BusResetRequest
    signalReset: SignalResetRequest
    def __init__(self, namespace: _Optional[_Union[_common_pb2.NameSpace, _Mapping]] = ..., busReset: _Optional[_Union[BusResetRequest, _Mapping]] = ..., signalReset: _Optional[_Union[SignalResetRequest, _Mapping]] = ...) -> None: ...

class BusResetRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SignalResetRequest(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[FrameWithSignalNames]
    def __init__(self, items: _Optional[_Iterable[_Union[FrameWithSignalNames, _Mapping]]] = ...) -> None: ...

class FrameConfigs(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[FrameConfig]
    def __init__(self, items: _Optional[_Iterable[_Union[FrameConfig, _Mapping]]] = ...) -> None: ...

class FrameConfig(_message.Message):
    __slots__ = ("name", "cycleTime", "signals")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CYCLETIME_FIELD_NUMBER: _ClassVar[int]
    SIGNALS_FIELD_NUMBER: _ClassVar[int]
    name: str
    cycleTime: float
    signals: _containers.RepeatedCompositeFieldContainer[ValueSequence]
    def __init__(self, name: _Optional[str] = ..., cycleTime: _Optional[float] = ..., signals: _Optional[_Iterable[_Union[ValueSequence, _Mapping]]] = ...) -> None: ...

class ValueSequence(_message.Message):
    __slots__ = ("name", "items", "prefix")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    name: str
    items: _containers.RepeatedCompositeFieldContainer[Value]
    prefix: _containers.RepeatedCompositeFieldContainer[Value]
    def __init__(self, name: _Optional[str] = ..., items: _Optional[_Iterable[_Union[Value, _Mapping]]] = ..., prefix: _Optional[_Iterable[_Union[Value, _Mapping]]] = ...) -> None: ...

class Value(_message.Message):
    __slots__ = ("integer", "raw", "double", "strValue")
    INTEGER_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    STRVALUE_FIELD_NUMBER: _ClassVar[int]
    integer: int
    raw: bytes
    double: float
    strValue: str
    def __init__(self, integer: _Optional[int] = ..., raw: _Optional[bytes] = ..., double: _Optional[float] = ..., strValue: _Optional[str] = ...) -> None: ...

class FrameWithSignalNames(_message.Message):
    __slots__ = ("name", "signals")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIGNALS_FIELD_NUMBER: _ClassVar[int]
    name: str
    signals: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., signals: _Optional[_Iterable[str]] = ...) -> None: ...

class FrameWithSignals(_message.Message):
    __slots__ = ("name", "signals")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIGNALS_FIELD_NUMBER: _ClassVar[int]
    name: str
    signals: _containers.RepeatedCompositeFieldContainer[ValueSequence]
    def __init__(self, name: _Optional[str] = ..., signals: _Optional[_Iterable[_Union[ValueSequence, _Mapping]]] = ...) -> None: ...
