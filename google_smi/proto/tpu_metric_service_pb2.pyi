from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google_smi.proto import tpu_telemetry_pb2 as _tpu_telemetry_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Exemplar(_message.Message):
    __slots__ = ("value", "timestamp", "attributes")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    value: float
    timestamp: _timestamp_pb2.Timestamp
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    def __init__(self, value: _Optional[float] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., attributes: _Optional[_Iterable[_Union[Attribute, _Mapping]]] = ...) -> None: ...

class Distribution(_message.Message):
    __slots__ = ("count", "mean", "min", "max", "sum_of_squared_deviation", "bucket_options", "bucket_counts", "exemplars")
    class BucketOptions(_message.Message):
        __slots__ = ("regular_buckets", "exponential_buckets", "explicit_buckets", "linear_buckets")
        class Regular(_message.Message):
            __slots__ = ("num_finite_buckets", "bounds")
            NUM_FINITE_BUCKETS_FIELD_NUMBER: _ClassVar[int]
            BOUNDS_FIELD_NUMBER: _ClassVar[int]
            num_finite_buckets: int
            bounds: _containers.RepeatedCompositeFieldContainer[Distribution.BucketOptions.Bound]
            def __init__(self, num_finite_buckets: _Optional[int] = ..., bounds: _Optional[_Iterable[_Union[Distribution.BucketOptions.Bound, _Mapping]]] = ...) -> None: ...
        class Exponential(_message.Message):
            __slots__ = ("num_finite_buckets", "growth_factor", "scale")
            NUM_FINITE_BUCKETS_FIELD_NUMBER: _ClassVar[int]
            GROWTH_FACTOR_FIELD_NUMBER: _ClassVar[int]
            SCALE_FIELD_NUMBER: _ClassVar[int]
            num_finite_buckets: int
            growth_factor: float
            scale: float
            def __init__(self, num_finite_buckets: _Optional[int] = ..., growth_factor: _Optional[float] = ..., scale: _Optional[float] = ...) -> None: ...
        class Bound(_message.Message):
            __slots__ = ("width", "offset")
            WIDTH_FIELD_NUMBER: _ClassVar[int]
            OFFSET_FIELD_NUMBER: _ClassVar[int]
            width: float
            offset: float
            def __init__(self, width: _Optional[float] = ..., offset: _Optional[float] = ...) -> None: ...
        class Linear(_message.Message):
            __slots__ = ("num_finite_buckets", "width", "offset")
            NUM_FINITE_BUCKETS_FIELD_NUMBER: _ClassVar[int]
            WIDTH_FIELD_NUMBER: _ClassVar[int]
            OFFSET_FIELD_NUMBER: _ClassVar[int]
            num_finite_buckets: int
            width: float
            offset: float
            def __init__(self, num_finite_buckets: _Optional[int] = ..., width: _Optional[float] = ..., offset: _Optional[float] = ...) -> None: ...
        class Explicit(_message.Message):
            __slots__ = ("bounds",)
            BOUNDS_FIELD_NUMBER: _ClassVar[int]
            bounds: _containers.RepeatedScalarFieldContainer[float]
            def __init__(self, bounds: _Optional[_Iterable[float]] = ...) -> None: ...
        REGULAR_BUCKETS_FIELD_NUMBER: _ClassVar[int]
        EXPONENTIAL_BUCKETS_FIELD_NUMBER: _ClassVar[int]
        EXPLICIT_BUCKETS_FIELD_NUMBER: _ClassVar[int]
        LINEAR_BUCKETS_FIELD_NUMBER: _ClassVar[int]
        regular_buckets: Distribution.BucketOptions.Regular
        exponential_buckets: Distribution.BucketOptions.Exponential
        explicit_buckets: Distribution.BucketOptions.Explicit
        linear_buckets: Distribution.BucketOptions.Linear
        def __init__(self, regular_buckets: _Optional[_Union[Distribution.BucketOptions.Regular, _Mapping]] = ..., exponential_buckets: _Optional[_Union[Distribution.BucketOptions.Exponential, _Mapping]] = ..., explicit_buckets: _Optional[_Union[Distribution.BucketOptions.Explicit, _Mapping]] = ..., linear_buckets: _Optional[_Union[Distribution.BucketOptions.Linear, _Mapping]] = ...) -> None: ...
    COUNT_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    SUM_OF_SQUARED_DEVIATION_FIELD_NUMBER: _ClassVar[int]
    BUCKET_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_COUNTS_FIELD_NUMBER: _ClassVar[int]
    EXEMPLARS_FIELD_NUMBER: _ClassVar[int]
    count: int
    mean: float
    min: float
    max: float
    sum_of_squared_deviation: float
    bucket_options: Distribution.BucketOptions
    bucket_counts: _containers.RepeatedScalarFieldContainer[int]
    exemplars: _containers.RepeatedCompositeFieldContainer[Exemplar]
    def __init__(self, count: _Optional[int] = ..., mean: _Optional[float] = ..., min: _Optional[float] = ..., max: _Optional[float] = ..., sum_of_squared_deviation: _Optional[float] = ..., bucket_options: _Optional[_Union[Distribution.BucketOptions, _Mapping]] = ..., bucket_counts: _Optional[_Iterable[int]] = ..., exemplars: _Optional[_Iterable[_Union[Exemplar, _Mapping]]] = ...) -> None: ...

class Gauge(_message.Message):
    __slots__ = ("as_double", "as_int", "as_string", "as_bool")
    AS_DOUBLE_FIELD_NUMBER: _ClassVar[int]
    AS_INT_FIELD_NUMBER: _ClassVar[int]
    AS_STRING_FIELD_NUMBER: _ClassVar[int]
    AS_BOOL_FIELD_NUMBER: _ClassVar[int]
    as_double: float
    as_int: int
    as_string: str
    as_bool: bool
    def __init__(self, as_double: _Optional[float] = ..., as_int: _Optional[int] = ..., as_string: _Optional[str] = ..., as_bool: bool = ...) -> None: ...

class Counter(_message.Message):
    __slots__ = ("as_double", "as_int", "exemplar")
    AS_DOUBLE_FIELD_NUMBER: _ClassVar[int]
    AS_INT_FIELD_NUMBER: _ClassVar[int]
    EXEMPLAR_FIELD_NUMBER: _ClassVar[int]
    as_double: float
    as_int: int
    exemplar: Exemplar
    def __init__(self, as_double: _Optional[float] = ..., as_int: _Optional[int] = ..., exemplar: _Optional[_Union[Exemplar, _Mapping]] = ...) -> None: ...

class Quantile(_message.Message):
    __slots__ = ("quantile", "value")
    QUANTILE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    quantile: float
    value: float
    def __init__(self, quantile: _Optional[float] = ..., value: _Optional[float] = ...) -> None: ...

class Summary(_message.Message):
    __slots__ = ("sample_count", "sample_sum", "quantile")
    SAMPLE_COUNT_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_SUM_FIELD_NUMBER: _ClassVar[int]
    QUANTILE_FIELD_NUMBER: _ClassVar[int]
    sample_count: int
    sample_sum: float
    quantile: _containers.RepeatedCompositeFieldContainer[Quantile]
    def __init__(self, sample_count: _Optional[int] = ..., sample_sum: _Optional[float] = ..., quantile: _Optional[_Iterable[_Union[Quantile, _Mapping]]] = ...) -> None: ...

class AttrValue(_message.Message):
    __slots__ = ("string_attr", "bool_attr", "int_attr", "double_attr", "array_attr", "kvlist_attr", "bytes_attr")
    STRING_ATTR_FIELD_NUMBER: _ClassVar[int]
    BOOL_ATTR_FIELD_NUMBER: _ClassVar[int]
    INT_ATTR_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_ATTR_FIELD_NUMBER: _ClassVar[int]
    ARRAY_ATTR_FIELD_NUMBER: _ClassVar[int]
    KVLIST_ATTR_FIELD_NUMBER: _ClassVar[int]
    BYTES_ATTR_FIELD_NUMBER: _ClassVar[int]
    string_attr: str
    bool_attr: bool
    int_attr: int
    double_attr: float
    array_attr: ArrayAttrValue
    kvlist_attr: KeyValueList
    bytes_attr: bytes
    def __init__(self, string_attr: _Optional[str] = ..., bool_attr: bool = ..., int_attr: _Optional[int] = ..., double_attr: _Optional[float] = ..., array_attr: _Optional[_Union[ArrayAttrValue, _Mapping]] = ..., kvlist_attr: _Optional[_Union[KeyValueList, _Mapping]] = ..., bytes_attr: _Optional[bytes] = ...) -> None: ...

class ArrayAttrValue(_message.Message):
    __slots__ = ("attrs",)
    ATTRS_FIELD_NUMBER: _ClassVar[int]
    attrs: _containers.RepeatedCompositeFieldContainer[AttrValue]
    def __init__(self, attrs: _Optional[_Iterable[_Union[AttrValue, _Mapping]]] = ...) -> None: ...

class KeyValueList(_message.Message):
    __slots__ = ("attributes",)
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    def __init__(self, attributes: _Optional[_Iterable[_Union[Attribute, _Mapping]]] = ...) -> None: ...

class Attribute(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: AttrValue
    def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[AttrValue, _Mapping]] = ...) -> None: ...

class Metric(_message.Message):
    __slots__ = ("attribute", "start_timestamp", "timestamp", "gauge", "counter", "distribution", "summary")
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    GAUGE_FIELD_NUMBER: _ClassVar[int]
    COUNTER_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    attribute: Attribute
    start_timestamp: _timestamp_pb2.Timestamp
    timestamp: _timestamp_pb2.Timestamp
    gauge: Gauge
    counter: Counter
    distribution: Distribution
    summary: Summary
    def __init__(self, attribute: _Optional[_Union[Attribute, _Mapping]] = ..., start_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., gauge: _Optional[_Union[Gauge, _Mapping]] = ..., counter: _Optional[_Union[Counter, _Mapping]] = ..., distribution: _Optional[_Union[Distribution, _Mapping]] = ..., summary: _Optional[_Union[Summary, _Mapping]] = ...) -> None: ...

class TPUMetric(_message.Message):
    __slots__ = ("name", "description", "metrics")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    metrics: _containers.RepeatedCompositeFieldContainer[Metric]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., metrics: _Optional[_Iterable[_Union[Metric, _Mapping]]] = ...) -> None: ...

class MetricRequest(_message.Message):
    __slots__ = ("metric_name", "skip_node_aggregation")
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    SKIP_NODE_AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    metric_name: str
    skip_node_aggregation: bool
    def __init__(self, metric_name: _Optional[str] = ..., skip_node_aggregation: bool = ...) -> None: ...

class MetricResponse(_message.Message):
    __slots__ = ("metric",)
    METRIC_FIELD_NUMBER: _ClassVar[int]
    metric: TPUMetric
    def __init__(self, metric: _Optional[_Union[TPUMetric, _Mapping]] = ...) -> None: ...

class ListSupportedMetricsRequest(_message.Message):
    __slots__ = ("filter",)
    FILTER_FIELD_NUMBER: _ClassVar[int]
    filter: str
    def __init__(self, filter: _Optional[str] = ...) -> None: ...

class SupportedMetric(_message.Message):
    __slots__ = ("metric_name",)
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    metric_name: str
    def __init__(self, metric_name: _Optional[str] = ...) -> None: ...

class ListSupportedMetricsResponse(_message.Message):
    __slots__ = ("supported_metric",)
    SUPPORTED_METRIC_FIELD_NUMBER: _ClassVar[int]
    supported_metric: _containers.RepeatedCompositeFieldContainer[SupportedMetric]
    def __init__(self, supported_metric: _Optional[_Iterable[_Union[SupportedMetric, _Mapping]]] = ...) -> None: ...

class GetTpuRuntimeStatusRequest(_message.Message):
    __slots__ = ("include_hlo_info",)
    INCLUDE_HLO_INFO_FIELD_NUMBER: _ClassVar[int]
    include_hlo_info: bool
    def __init__(self, include_hlo_info: bool = ...) -> None: ...

class GetTpuRuntimeStatusResponse(_message.Message):
    __slots__ = ("host_name", "core_states")
    class CoreStatesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: _tpu_telemetry_pb2.CurrentCoreStateSummary
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[_tpu_telemetry_pb2.CurrentCoreStateSummary, _Mapping]] = ...) -> None: ...
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    CORE_STATES_FIELD_NUMBER: _ClassVar[int]
    host_name: str
    core_states: _containers.MessageMap[int, _tpu_telemetry_pb2.CurrentCoreStateSummary]
    def __init__(self, host_name: _Optional[str] = ..., core_states: _Optional[_Mapping[int, _tpu_telemetry_pb2.CurrentCoreStateSummary]] = ...) -> None: ...
