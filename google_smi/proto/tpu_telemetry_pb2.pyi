from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TpuCoreTypeProto(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TPU_CORE_TYPE_INVALID: _ClassVar[TpuCoreTypeProto]
    TPU_CORE_TYPE_TENSOR_CORE: _ClassVar[TpuCoreTypeProto]
    TPU_CORE_TYPE_SPARSE_CORE_V0: _ClassVar[TpuCoreTypeProto]
    TPU_CORE_TYPE_SPARSE_CORE: _ClassVar[TpuCoreTypeProto]

class TpuSequencerTypeProto(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TPU_SEQUENCER_TYPE_INVALID: _ClassVar[TpuSequencerTypeProto]
    TPU_SEQUENCER_TYPE_TENSOR_CORE_SEQUENCER: _ClassVar[TpuSequencerTypeProto]
    TPU_SEQUENCER_TYPE_SPARSE_CORE_V0_SEQUENCER: _ClassVar[TpuSequencerTypeProto]
    TPU_SEQUENCER_TYPE_SPARSE_CORE_V0_ADDRESS_HANDLER: _ClassVar[TpuSequencerTypeProto]
    TPU_SEQUENCER_TYPE_SPARSE_CORE_SEQUENCER: _ClassVar[TpuSequencerTypeProto]
    TPU_SEQUENCER_TYPE_SPARSE_CORE_TILE_ACCESS_CORE_SEQUENCER: _ClassVar[TpuSequencerTypeProto]
    TPU_SEQUENCER_TYPE_SPARSE_CORE_TILE_EXECUTE_CORE_SEQUENCER: _ClassVar[TpuSequencerTypeProto]
TPU_CORE_TYPE_INVALID: TpuCoreTypeProto
TPU_CORE_TYPE_TENSOR_CORE: TpuCoreTypeProto
TPU_CORE_TYPE_SPARSE_CORE_V0: TpuCoreTypeProto
TPU_CORE_TYPE_SPARSE_CORE: TpuCoreTypeProto
TPU_SEQUENCER_TYPE_INVALID: TpuSequencerTypeProto
TPU_SEQUENCER_TYPE_TENSOR_CORE_SEQUENCER: TpuSequencerTypeProto
TPU_SEQUENCER_TYPE_SPARSE_CORE_V0_SEQUENCER: TpuSequencerTypeProto
TPU_SEQUENCER_TYPE_SPARSE_CORE_V0_ADDRESS_HANDLER: TpuSequencerTypeProto
TPU_SEQUENCER_TYPE_SPARSE_CORE_SEQUENCER: TpuSequencerTypeProto
TPU_SEQUENCER_TYPE_SPARSE_CORE_TILE_ACCESS_CORE_SEQUENCER: TpuSequencerTypeProto
TPU_SEQUENCER_TYPE_SPARSE_CORE_TILE_EXECUTE_CORE_SEQUENCER: TpuSequencerTypeProto

class TpuCoreOnChipProto(_message.Message):
    __slots__ = ("type", "index")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    type: TpuCoreTypeProto
    index: int
    def __init__(self, type: _Optional[_Union[TpuCoreTypeProto, str]] = ..., index: _Optional[int] = ...) -> None: ...

class TpuCoreIdentifier(_message.Message):
    __slots__ = ("global_core_id", "chip_id", "core_on_chip")
    GLOBAL_CORE_ID_FIELD_NUMBER: _ClassVar[int]
    CHIP_ID_FIELD_NUMBER: _ClassVar[int]
    CORE_ON_CHIP_FIELD_NUMBER: _ClassVar[int]
    global_core_id: int
    chip_id: int
    core_on_chip: TpuCoreOnChipProto
    def __init__(self, global_core_id: _Optional[int] = ..., chip_id: _Optional[int] = ..., core_on_chip: _Optional[_Union[TpuCoreOnChipProto, _Mapping]] = ...) -> None: ...

class QueuedProgramInfo(_message.Message):
    __slots__ = ("run_id", "launch_id", "program_fingerprint")
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_ID_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    run_id: int
    launch_id: int
    program_fingerprint: bytes
    def __init__(self, run_id: _Optional[int] = ..., launch_id: _Optional[int] = ..., program_fingerprint: _Optional[bytes] = ...) -> None: ...

class SequencerInfo(_message.Message):
    __slots__ = ("sequencer_type", "sequencer_index", "pc", "tag", "tracemark", "program_id", "run_id", "hlo_location", "hlo_detailed_info")
    SEQUENCER_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCER_INDEX_FIELD_NUMBER: _ClassVar[int]
    PC_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    TRACEMARK_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    HLO_LOCATION_FIELD_NUMBER: _ClassVar[int]
    HLO_DETAILED_INFO_FIELD_NUMBER: _ClassVar[int]
    sequencer_type: TpuSequencerTypeProto
    sequencer_index: int
    pc: int
    tag: int
    tracemark: int
    program_id: int
    run_id: int
    hlo_location: str
    hlo_detailed_info: str
    def __init__(self, sequencer_type: _Optional[_Union[TpuSequencerTypeProto, str]] = ..., sequencer_index: _Optional[int] = ..., pc: _Optional[int] = ..., tag: _Optional[int] = ..., tracemark: _Optional[int] = ..., program_id: _Optional[int] = ..., run_id: _Optional[int] = ..., hlo_location: _Optional[str] = ..., hlo_detailed_info: _Optional[str] = ...) -> None: ...

class CurrentCoreStateSummary(_message.Message):
    __slots__ = ("core_id", "sequencer_info", "xdb_server_running", "program_fingerprint", "launch_id", "queued_program_info", "error_message")
    CORE_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCER_INFO_FIELD_NUMBER: _ClassVar[int]
    XDB_SERVER_RUNNING_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_ID_FIELD_NUMBER: _ClassVar[int]
    QUEUED_PROGRAM_INFO_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    core_id: TpuCoreIdentifier
    sequencer_info: _containers.RepeatedCompositeFieldContainer[SequencerInfo]
    xdb_server_running: bool
    program_fingerprint: bytes
    launch_id: int
    queued_program_info: _containers.RepeatedCompositeFieldContainer[QueuedProgramInfo]
    error_message: str
    def __init__(self, core_id: _Optional[_Union[TpuCoreIdentifier, _Mapping]] = ..., sequencer_info: _Optional[_Iterable[_Union[SequencerInfo, _Mapping]]] = ..., xdb_server_running: bool = ..., program_fingerprint: _Optional[bytes] = ..., launch_id: _Optional[int] = ..., queued_program_info: _Optional[_Iterable[_Union[QueuedProgramInfo, _Mapping]]] = ..., error_message: _Optional[str] = ...) -> None: ...

class AllCoreStateSummaries(_message.Message):
    __slots__ = ("core_states",)
    class CoreStatesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: CurrentCoreStateSummary
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[CurrentCoreStateSummary, _Mapping]] = ...) -> None: ...
    CORE_STATES_FIELD_NUMBER: _ClassVar[int]
    core_states: _containers.MessageMap[int, CurrentCoreStateSummary]
    def __init__(self, core_states: _Optional[_Mapping[int, CurrentCoreStateSummary]] = ...) -> None: ...
