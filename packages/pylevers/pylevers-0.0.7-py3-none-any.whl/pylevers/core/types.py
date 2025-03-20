from enum import Enum
from enum import IntEnum

import re
import time
import struct
import numpy as np

from proto import levers_pb2
from proto import schema_pb2
from proto import common_pb2
from proto import levers_pb2_grpc


def _parse_enum_value_or_string(enum_type, pb_enum_type, value, pb_enum_prefix=''):
    """
    Convert `value` to corresponding enum value.

    Args:
        enum_type: enum type.
        pb_enum_type: Protobuf enum type.
        value (int, str or enum_type): enum value

    Returns:
        enum type instance.

    Raises:
        LeversException on invalid enum.
    """
    try:
        if isinstance(value, str):
            assert pb_enum_type.Value(pb_enum_prefix + value) == enum_type[value].value
            return enum_type[value]
        if isinstance(value, enum_type):
            assert pb_enum_type.Name(value.value) == pb_enum_prefix + value.name
            return value
        assert pb_enum_type.Name(value) == pb_enum_prefix + enum_type(value).name
        return enum_type(value)
    except ValueError as e:
        raise LeversException(str(e))
    except AssertionError as e:
        raise LeversException(f"Enum definition mismatch:{str(e)}")


def _default_if_none(value, default_value):
    return value if value is not None else default_value


def _parse_bytes_to_float(byte_data):
    num_floats = len(byte_data) // 4
    float_values = []
    for i in range(num_floats):
        float_value = struct.unpack('f', byte_data[i * 4:(i + 1) * 4])[0]
        float_values.append(float_value)
    return float_values


def _check_name(name):
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    if not re.match(r'^[a-zA-Z0-9_][a-zA-Z0-9_-]*$', name):
        raise ValueError("name must only contain a-zA-Z0-9 - _, and cannot start with -")
    if len(name) > 255:
        raise ValueError("name must be less than 256 characters")


def _stringify(self):
    return f'{type(self).__name__}{vars(self)}'


class LeversException(Exception):
    pass


class DataType(IntEnum):
    """
    Data type.
    """
    NONE = 0
    BOOL = 1
    INT32 = 2
    INT64 = 3
    FLOAT = 4
    DOUBLE = 5
    STRING = 6

    FLOAT_VECTOR = 100
    INT8_VECTOR = 101


class IndexType(Enum):
    """
    Index type.
    """
    NONE = 0
    SPANN = 1
    HNSW = 2
    STL = 3
    TRIE = 4
    BITMAP = 5


class IndexMetrics(Enum):
    """
    Index metrics.
    """
    NONE = 0
    L2 = 1
    COSINE = 2
    IP = 3


class IndexQuantType(Enum):
    """
    Index quantization type.
    """
    NONE = 0
    PQ = 1
    SQ = 2


class CollectionState(Enum):
    """
    Collection state.
    """
    coll_none = 0
    creating = 1
    clean = 2
    deleting = 3
    deleted = 4
    loading = 5
    loaded = 6
    releasing = 7


class IndexState(Enum):
    """
    Index state.
    """
    index_state_none = 0
    index_state_indexing = 1
    index_state_indexed = 2
    index_state_indexing_failed = 3


class SegmentState(Enum):
    """
    Segment state.
    """
    init = 0
    rawdata = 1
    columning = 2
    columing_failed = 3
    columned = 4
    growing = 5
    sealed = 6
    flushing = 7
    flushed = 8
    indexing = 9
    indexed = 10
    indexing_failed = 11
    err = 12


class _Printable:
    def __str__(self):
        return _stringify(self)

    def __repr__(self):
        return _stringify(self)

    def to_dict(self):
        def convert_to_dict(obj):
            if isinstance(obj, _Printable):
                return obj.to_dict()
            elif isinstance(obj, Enum):
                return obj.value
            elif isinstance(obj, dict):
                return {k: convert_to_dict(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_dict(item) for item in obj]
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, bytes):
                return list(obj)
            else:
                return obj

        return {k: convert_to_dict(v) for k, v in self.__dict__.items()}


class ClientInfo(_Printable):
    """
    Client info.
    """

    def __init__(self,
                 sdk_type,
                 sdk_version,
                 local_time,
                 user,
                 password,
                 db_name,
                 host,
                 reserved=None):
        self.sdk_type = sdk_type
        self.sdk_version = sdk_version
        self.local_time = local_time
        self.user = user
        self.password = password
        self.db_name = db_name
        self.host = host
        self.reserved = _default_if_none(reserved, {})

    def _valid_check(self):
        if not isinstance(self.sdk_type, str):
            raise TypeError("sdk_type must be a string")
        if not isinstance(self.sdk_version, str):
            raise TypeError("sdk_version must be a string")
        if not isinstance(self.local_time, str):
            raise TypeError("local_time must be a string")
        if not isinstance(self.user, str):
            raise TypeError("user must be a string")
        if not isinstance(self.host, str):
            raise TypeError("host must be a string")

    def to_pb(self):
        client_info = common_pb2.ClientInfo()
        client_info.sdk_type = self.sdk_type
        client_info.sdk_version = self.sdk_version
        client_info.local_time = self.local_time
        client_info.user = self.user
        client_info.password = self.password
        client_info.db_name = self.db_name
        client_info.host = self.host
        client_info.reserved.update(self.reserved)
        return client_info


class ServerInfo(_Printable):
    """
    Server info.
    """

    def __init__(self, build_tags, build_timestamp, reserved=None):
        self.build_tags = build_tags
        self.build_timestamp = build_timestamp
        self.reserved = _default_if_none(reserved, {})

    @staticmethod
    def from_pb(pb_server_info):
        server_info = ServerInfo(pb_server_info.build_tags, pb_server_info.build_timestamp, pb_server_info.reserved)
        return server_info


class ConnectResult(_Printable):
    """
    Server info.
    """

    def __init__(self, status, results):
        self.status = status
        self.results = results

    @staticmethod
    def from_pb(pb_result):
        if pb_result.status.error_code != 0:
            return ConnectResult(Status.from_pb(pb_result.status), None)
        return ConnectResult(Status.from_pb(pb_result.status), ServerInfo.from_pb(pb_result.server_info))


class DatabaseSchema(_Printable):
    """
    Database schema.
    """

    def __init__(self, db_name, extra_params=None):
        self.db_name = db_name
        self.extra_params = _default_if_none(extra_params, {})
        self._valid_check()

    def _valid_check(self):
        if not isinstance(self.db_name, str):
            raise TypeError("db_name must be a string")
        if not isinstance(self.extra_params, dict):
            raise TypeError("extra_params must be a dictionary")

    def to_pb(self):
        database_schema = schema_pb2.DatabaseSchema()
        database_schema.db_name = self.db_name
        database_schema.extra_params.update(self.extra_params)
        return database_schema

class IndexSchema(_Printable):
    """
    Index schema.
    """

    def __init__(self, index_type, index_metrics=None, index_quant_type=None, extra_params=None):

        self.index_type = _parse_enum_value_or_string(IndexType,
                                                      schema_pb2.IndexType,
                                                      index_type, 'IT_')

        self.index_metrics = index_metrics
        self.index_quant_type = index_quant_type
        self.extra_params = _default_if_none(extra_params, {})
        self._valid_check()

    def _valid_check(self):
        if not isinstance(self.index_type, IndexType):
            raise TypeError("index_type must be a IndexType")
        if not isinstance(self.extra_params, dict):
            raise TypeError("extra_params must be adict")
        if self.index_type in [IndexType.SPANN, IndexType.HNSW]:
            if  self.index_metrics not in [IndexMetrics.L2, IndexMetrics.COSINE, IndexMetrics.IP]:
                raise TypeError("index type in spann or hnsw, index_metrics must be l2,cosine or ip")
            if self.index_quant_type and self.index_quant_type != IndexQuantType.NONE:
                if not isinstance(self.index_quant_type, IndexQuantType):
                    raise TypeError("index_quant_type must be a IndexQuantType")
                if self.index_metrics != IndexMetrics.L2 and self.index_type != IndexType.SPANN:
                    raise TypeError("index_quant_type pq, index type must be spann and index metrics must be l2")
        else:
            if self.index_metrics in [IndexMetrics.L2, IndexMetrics.COSINE, IndexMetrics.IP]:
                raise TypeError("other index type, index_metrics can not in l2,cosine,ip")

    def to_pb(self):
        index = schema_pb2.IndexSchema()
        index.index_type = self.index_type.value
        if self.index_metrics:
            self.index_metrics = _parse_enum_value_or_string(IndexMetrics,
                                                             schema_pb2.IndexMetrics,
                                                             self.index_metrics, 'IM_')
            index.index_metrics = self.index_metrics.value
        if self.index_quant_type:
            self.index_quant_type = _parse_enum_value_or_string(IndexQuantType,
                                                                schema_pb2.IndexQuantType,
                                                                self.index_quant_type, 'IQ_')
            index.index_quant_type = self.index_quant_type.value
        index.extra_params.update(self.extra_params)
        return index

    @staticmethod
    def from_pb(pb_index_schema):
        index = IndexSchema(IndexType(pb_index_schema.index_type),
                            IndexMetrics(pb_index_schema.index_metrics),
                            IndexQuantType(pb_index_schema.index_quant_type))

        index.extra_params = dict(pb_index_schema.extra_params) if pb_index_schema.extra_params else {}

        return index


class FieldSchema(_Printable):
    """
    Field schema.
    """

    def __init__(self,
                 name,
                 data_type,
                 dimension=0,
                 mutable_segment_schema=None,
                 indexed_segment_schema=None,
                 extra_params=None):

        self.name = name
        self.data_type = _parse_enum_value_or_string(DataType,
                                                     schema_pb2.DataType,
                                                     data_type, 'DT_')
        self.dimension = dimension
        self.mutable_segment_schema = mutable_segment_schema
        self.indexed_segment_schema = indexed_segment_schema
        self.extra_params = extra_params
        self._valid_check()

    def _valid_check(self):
        _check_name(self.name)
        if not isinstance(self.dimension, int) or self.dimension < 0:
            raise ValueError("dimension must be a positive integer")
        if self.extra_params is None:
            self.extra_params = {}
        elif not isinstance(self.extra_params, dict):
            raise TypeError("extra_params must be a dictionary")

        # check schema
        if self.mutable_segment_schema:
            if not isinstance(self.mutable_segment_schema, IndexSchema):
                raise TypeError("mutable_segment_schema must be an IndexSchema")
        if self.indexed_segment_schema:
            if not isinstance(self.indexed_segment_schema, IndexSchema):
                raise TypeError("indexed_segment_schema must be an IndexSchema")

        # check data type and dimension
        if self.data_type in [DataType.FLOAT_VECTOR, DataType.INT8_VECTOR]:
            if self.dimension < 4 or self.dimension > 10000:
                raise ValueError("vector filed dimension must in 4-10000")
            if self.indexed_segment_schema and self.indexed_segment_schema.index_type != IndexType.NONE:
                if self.indexed_segment_schema.index_type not in [IndexType.SPANN, IndexType.HNSW]:
                    raise ValueError("vector filed indexed_segment_schema index_type must in spann or hnsw")
                if self.data_type == DataType.INT8_VECTOR:
                    if self.indexed_segment_schema.index_metrics == IndexMetrics.COSINE:
                        raise ValueError("int8vector filed indexed_segment_schema index_metrics can't be cosine")

        else:
            if self.dimension != 0:
                raise ValueError("other filed dimension must be 0")
            if self.indexed_segment_schema:
                if self.indexed_segment_schema.index_type in [IndexType.SPANN, IndexType.HNSW]:
                    raise ValueError("other filed indexed_segment_schema index_type must not in spann or hnsw")

    def to_pb(self):
        field = schema_pb2.FieldSchema()
        field.name = self.name
        field.data_type = self.data_type.value
        field.dimension = self.dimension
        if self.mutable_segment_schema:
            field.mutable_segment_schema.CopyFrom(self.mutable_segment_schema.to_pb())
        if self.indexed_segment_schema:
            field.indexed_segment_schema.CopyFrom(self.indexed_segment_schema.to_pb())
        field.extra_params.update(self.extra_params)
        return field

    @staticmethod
    def from_pb(pb_field):
        field = FieldSchema(pb_field.name,
                            DataType(pb_field.data_type),
                            pb_field.dimension,
                            IndexSchema.from_pb(pb_field.mutable_segment_schema),
                            IndexSchema.from_pb(pb_field.indexed_segment_schema),
                            )

        field.extra_params = dict(pb_field.extra_params) if pb_field.extra_params else {}

        return field


class CollectionSchema(_Printable):
    """
    Collection configuration.
    """

    def __init__(self,
                 name,
                 description,
                 fields,
                 extra_params=None):

        self.name = name
        self.description = description
        self.fields = fields
        self.extra_params = _default_if_none(extra_params, {})
        self._valid_check()

    def _valid_check(self):
        _check_name(self.name)
        if not isinstance(self.description, str):
            raise TypeError("description must be a string")
        if not isinstance(self.fields, list):
            raise TypeError("fields must be a list")
        if not isinstance(self.extra_params, dict):
            raise TypeError("extra_params must be a dictionary")

        vector_fields_count = 0
        for field in self.fields:
            if not isinstance(field, FieldSchema):
                raise TypeError("fields must be a list of FieldSchema")
            if field.data_type in [DataType.FLOAT_VECTOR, DataType.INT8_VECTOR]:
                vector_fields_count += 1
        if vector_fields_count < 1:
            raise ValueError("fields must contain one vector field")

    def to_pb(self):
        """Return corresponding protobuf message."""
        collection_schema = schema_pb2.CollectionSchema()
        collection_schema.name = self.name
        collection_schema.description = self.description
        for field in self.fields:
            collection_schema.fields.append(field.to_pb())
        collection_schema.extra_params.update(self.extra_params)
        return collection_schema

    @staticmethod
    def from_pb(pb_collection_config):
        """Parse from corresponding protobuf type."""
        schema = CollectionSchema(pb_collection_config.name,
                                  pb_collection_config.description,
                                  [FieldSchema.from_pb(field) for field in pb_collection_config.fields]
                                  )
        if pb_collection_config.extra_params:
            schema.extra_params = dict(pb_collection_config.extra_params)
        return schema


class SegmentStats(_Printable):
    """
    Segment  statistics.
    """

    def __init__(self,
                 id,
                 state,
                 entity_count,
                 min_entity_id,
                 max_entity_id,
                 is_bulk_insert,
                 is_deleting,
                 is_compacting,
                 total_persist_size,
                 data_path,
                 data_files_size,
                 index_path,
                 index_files_size,
                 index_state_map):
        self.id = id
        self.state = _parse_enum_value_or_string(SegmentState,
                                                 common_pb2.SegmentState,
                                                 state, '')

        self.entity_count = entity_count
        self.min_entity_id = min_entity_id
        self.max_entity_id = max_entity_id
        self.is_bulk_insert = is_bulk_insert
        self.is_deleting = is_deleting
        self.is_compacting = is_compacting
        self.total_persist_size = total_persist_size
        self.data_path = data_path
        self.data_files_size = data_files_size
        self.index_path = index_path
        self.index_files_size = index_files_size
        self.index_state_map = index_state_map

    @staticmethod
    def from_pb(pb_segment_stats):
        """Parse from corresponding protobuf type."""
        return SegmentStats(pb_segment_stats.id,
                            pb_segment_stats.state,
                            pb_segment_stats.entity_count,
                            pb_segment_stats.min_entity_id,
                            pb_segment_stats.max_entity_id,
                            pb_segment_stats.is_bulk_insert,
                            pb_segment_stats.is_deleting,
                            pb_segment_stats.is_compacting,
                            pb_segment_stats.total_persist_size,
                            pb_segment_stats.data_path,
                            dict(pb_segment_stats.data_files_size),
                            pb_segment_stats.index_path,
                            dict(pb_segment_stats.index_files_size),
                            dict(pb_segment_stats.index_state_map)
                            )


class ShardStats(_Printable):
    """
    Shard statistics.
    """

    def __init__(self,
                 id,
                 fs_name,
                 fs_shard_id,
                 fs_id,
                 entity_count,
                 segs,
                 total_persist_size):
        self.id = id
        self.fs_name = fs_name
        self.fs_shard_id = fs_shard_id
        self.fs_id = fs_id
        self.entity_count = entity_count
        self.segs = segs
        self.total_persist_size = total_persist_size

    @staticmethod
    def from_pb(pb_shard_stats):
        """Parse from corresponding protobuf type."""
        return ShardStats(pb_shard_stats.id,
                          pb_shard_stats.fs_name,
                          pb_shard_stats.fs_shard_id,
                          pb_shard_stats.fs_id,
                          pb_shard_stats.entity_count,
                          [SegmentStats.from_pb(seg) for seg in pb_shard_stats.segs],
                          pb_shard_stats.total_persist_size)


class CollectionStats(_Printable):
    """
    Collection statistics.
    """

    def __init__(self,
                 collection_name,
                 state,
                 entity_count,
                 create_timestamp,
                 shards,
                 total_persist_size):
        self.collection_name = collection_name
        self.state = _parse_enum_value_or_string(CollectionState,
                                                 common_pb2.CollectionState,
                                                 state, '')
        self.entity_count = entity_count
        self.create_timestamp = create_timestamp
        self.shards = shards
        self.total_persist_size = total_persist_size

    @staticmethod
    def from_pb(pb_collection_stats):
        """Parse from corresponding protobuf type."""

        return CollectionStats(pb_collection_stats.collection_name,
                               CollectionState(pb_collection_stats.state),
                               pb_collection_stats.entity_count,
                               pb_collection_stats.create_timestamp,
                               [ShardStats.from_pb(shard) for shard in pb_collection_stats.shards],
                               pb_collection_stats.total_persist_size
                               )


def _field_value(value, data_type):
    field_value = common_pb2.FieldValue()
    type_to_attr = {
        DataType.BOOL: 'bool_data',
        DataType.INT32: 'int_data',
        DataType.INT64: 'long_data',
        DataType.FLOAT: 'float_data',
        DataType.DOUBLE: 'double_data',
        DataType.STRING: 'string_data',
        DataType.FLOAT_VECTOR: 'bytes_data',
        DataType.INT8_VECTOR: 'bytes_data',
    }
    if data_type not in type_to_attr:
        raise LeversException(
            f"Unsupported type[{type}], supported={type_to_attr.keys()}")
    setattr(field_value, type_to_attr[data_type], value)
    return field_value


def _parse_field_value_from_pb(pb_field_value, field_type):
    field_name = pb_field_value.WhichOneof('data')
    field_value = getattr(pb_field_value, field_name)
    if field_type in [DataType.INT8_VECTOR, DataType.FLOAT_VECTOR]:
        field_value = _parse_bytes_to_float(field_value)
    return field_value


class FieldData(_Printable):
    """
    Request for field
    """

    def __init__(self,
                 name,
                 type,
                 value):
        self.name = name
        self.type = type
        self.value = value
        self._valid_check()

    def _valid_check(self):
        if len(self.name) == 0:
            raise LeversException("field data no name")
        if not isinstance(self.type, DataType):
            raise LeversException("field data has wrong type")

    def to_pb(self):
        pb_field_data = common_pb2.FieldData()
        pb_field_data.name = self.name
        pb_field_data.type = self.type
        pb_field_data.value = _field_value(self.value, type)
        return pb_field_data

    @staticmethod
    def from_pb(pb_field_data):
        type = _parse_enum_value_or_string(DataType, schema_pb2.DataType, pb_field_data.type, 'DT_')
        value = _parse_field_value_from_pb(pb_field_data.value, type)
        return FieldData(pb_field_data.name, type, value)


class EntityMeta(_Printable):
    """
    Request for entity
    """

    def __init__(self,
                 field_name,
                 type):
        self.field_name = field_name
        self.type = type
        self._valid_check()

    def _valid_check(self):
        if len(self.field_name) == 0:
            raise LeversException("entity meta field name not valid")

    def to_pb(self):
        pb_entity_meta = common_pb2.EntityMeta()
        pb_entity_meta.field_name = self.field_name
        pb_entity_meta.type = self.type
        return pb_entity_meta


class EntityData(_Printable):
    """
    Request for entity
    """

    def __init__(self,
                 pk,
                 field_values):
        self.pk = pk
        self.field_values = field_values
        self._valid_check()

    def _valid_check(self):
        if self.pk < 0:
            raise LeversException("entity data pk not valid")

        if len(self.field_values) == 0:
            raise LeversException("entity data no field data")
        for i in range(len(self.field_values)):
            if isinstance(self.field_values[i], list):
                array = np.array(self.field_values[i], dtype=np.float32)
                self.field_values[i] = array.tobytes()

    def to_pb(self, entity_metas):
        pb_entity_data = common_pb2.EntityData()
        pb_entity_data.pk = self.pk
        pb_entity_data.field_values.extend(
            _field_value(field_value, entity_metas[index].type) for index, field_value in enumerate(self.field_values))
        return pb_entity_data


class MutableResult(_Printable):
    """
    Request for delete entities
    """

    def __init__(self,
                 status,
                 succ_index,
                 err_index,
                 acknowledged,
                 insert_cnt,
                 delete_cnt,
                 update_cnt,
                 pks):
        self.status = status
        self.succ_index = succ_index
        self.err_index = err_index
        self.acknowledged = acknowledged
        self.insert_cnt = insert_cnt
        self.delete_cnt = delete_cnt
        self.update_cnt = update_cnt
        self.pks = pks

    @staticmethod
    def from_pb(pb_result):
        succ_index = []
        err_index = []
        pks = []
        succ_index.extend(index for index in pb_result.succ_index)
        err_index.extend(index for index in pb_result.err_index)
        pks.extend(pk for pk in pb_result.pks)
        return MutableResult(Status.from_pb(pb_result.status), succ_index, err_index, pb_result.acknowledged,
                             pb_result.insert_cnt, pb_result.delete_cnt, pb_result.update_cnt, pks)


class KnnParam(_Printable):
    """
    Request for knn search
    """

    def __init__(self,
                 field_name,
                 vectors,
                 batch_count=1,
                 is_bruteforce=False,
                 extra_params=None):

        self.field_name = field_name
        self.vectors = vectors
        self.batch_count = batch_count
        self.is_bruteforce = is_bruteforce
        self.extra_params = _default_if_none(extra_params, {})
        self._valid_check()

    def _valid_check(self):
        if self.field_name is None or len(self.field_name) == 0:
            raise LeversException("field name is not valid")
        if not isinstance(self.vectors, (list, bytes)) or len(self.vectors) == 0:
            raise LeversException("vectors is not valid")
        if not isinstance(self.is_bruteforce, bool):
            raise LeversException("is_bruteforce is not valid")
        if self.batch_count < 1 or self.batch_count > 10000:
            raise LeversException("batch_count is not valid, section [1, 10000]")
        if isinstance(self.vectors, list):
            for vector in self.vectors:
                if len(vector) == 0 or not isinstance(vector, list):
                    raise LeversException("vectors is not valid")
            array = np.array(self.vectors, dtype=np.float32)
            self.vectors = array.tobytes()

    def to_pb(self):
        knn_param = common_pb2.KnnParam()
        knn_param.field_name = self.field_name
        knn_param.vectors = self.vectors
        if self.batch_count:
            knn_param.batch_count = self.batch_count
        if self.is_bruteforce:
            knn_param.is_bruteforce = self.is_bruteforce
        knn_param.extra_params.update(self.extra_params)
        return knn_param


class Status(_Printable):
    def __init__(self, code, reason=''):
        self.code = code
        self.reason = reason

    def ok(self):
        """
        Returns:
            bool: if ok.
        """
        return self.code == 0

    def __str__(self):
        if self.code == 0:
            return 'success'
        return f'{self.reason}({self.code})'

    @staticmethod
    def from_pb(pb_status):
        return Status(pb_status.error_code, pb_status.reason)


class EntityResult(_Printable):
    """
    Search result
    """

    def __init__(self,
                 pk,
                 scores,
                 field_datas):
        self.pk = pk
        self.scores = round(scores, 4)
        self.field_datas = field_datas

    @staticmethod
    def from_pb(pb_result):
        field_datas = []
        field_datas.extend(FieldData.from_pb(field_data) for field_data in pb_result.field_datas)
        return EntityResult(pb_result.pk, pb_result.scores, field_datas)


class SearchResult(_Printable):
    """
    Search result
    """

    def __init__(self,
                 status,
                 entity_results):
        self.status = status
        self.entity_results = entity_results

    @staticmethod
    def from_pb(pb_result, score_limit):
        if pb_result.status.error_code != 0:
            return SearchResult(Status.from_pb(pb_result.status), [])
        entity_results = []
        if score_limit:
            for entity_result in pb_result.entity_results:
                if round(entity_result.scores, 4) > round(score_limit, 4):
                    continue
                entity_results.append(EntityResult.from_pb(entity_result))
        else:
            entity_results.extend(EntityResult.from_pb(entity_result) for entity_result in pb_result.entity_results)
        return SearchResult(Status.from_pb(pb_result.status), entity_results)


class SearchResults(_Printable):
    """
    Search results
    """

    def __init__(self,
                 status,
                 results):
        self.status = status
        self.results = results

    @staticmethod
    def from_pb(pb_results, score_limit):
        if pb_results.status.error_code != 0:
            return SearchResults(Status.from_pb(pb_results.status), [])
        results = []
        results.extend(SearchResult.from_pb(result, score_limit) for result in pb_results.results)
        return SearchResults(Status.from_pb(pb_results.status), results)


class GetResult(_Printable):
    """
    Search result
    """

    def __init__(self,
                 status,
                 entity_data):
        self.status = status
        self.entity_data = entity_data

    @staticmethod
    def from_pb(pb_result):
        if pb_result.status.error_code != 0:
            return GetResult(Status.from_pb(pb_result.status), None)
        entity_data = EntityResult.from_pb(pb_result.result)
        return GetResult(Status.from_pb(pb_result.status), entity_data)


class ListResult(_Printable):
    """
    List result
    """

    def __init__(self,
                 status,
                 results):
        self.status = status
        self.results = results

    @staticmethod
    def from_pb(pb_result):
        if pb_result.status.error_code != 0:
            return ListResult(Status.from_pb(pb_result.status), [])
        return ListResult(Status.from_pb(pb_result.status), pb_result.collection_names)


class DescribeResult(_Printable):
    """
    Describe result
    """

    def __init__(self,
                 status,
                 results):
        self.status = status
        self.results = results

    @staticmethod
    def from_pb(pb_result):
        if pb_result.status.error_code != 0:
            return DescribeResult(Status.from_pb(pb_result.status), None)
        return DescribeResult(Status.from_pb(pb_result.status), CollectionSchema.from_pb(pb_result.schema))


class StatsResult(_Printable):
    """
    Stats result
    """

    def __init__(self,
                 status,
                 results):
        self.status = status
        self.results = results

    @staticmethod
    def from_pb(pb_result):
        if pb_result.status.error_code != 0:
            return StatsResult(Status.from_pb(pb_result.status), None)
        return StatsResult(Status.from_pb(pb_result.status), CollectionStats.from_pb(pb_result.stats))