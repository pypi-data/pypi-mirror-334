import time

import grpc

from google.protobuf.json_format import MessageToDict
from google.protobuf.empty_pb2 import Empty
from .types import LeversException
from .types import SearchResults
from .types import MutableResult
from .types import GetResult
from .types import ListResult
from .types import DescribeResult
from .types import StatsResult
from .types import Status
from .types import ConnectResult
from .types import ClientInfo

from .types import common_pb2
from .types import levers_pb2
from .types import levers_pb2_grpc
from .. import __version__


class BaseHandler:
    @staticmethod
    def _parse_response(pb_or_txt):
        pb = pb_or_txt
        if isinstance(pb, common_pb2.Status):
            return Status.from_pb(pb)
        status = Status(pb.status.error_code, pb.status.reason)
        if not status.ok():
            return status, None
        rsp = MessageToDict(pb, always_print_fields_with_no_presence=True)
        return status, rsp

    @staticmethod
    def _parse_status(pb_status):
        return Status.from_pb(pb_status)


class GrpcHandler(BaseHandler):
    def __init__(self, host, port):
        # hostname
        self._host = host
        # port
        self._port = port
        self._channel = None
        self.new_channel()

    def new_channel(self):
        spec = f'{self._host}:{self._port}'
        if self._channel:
            self.close()
        self._channel = grpc.insecure_channel(spec)
        self._stub = levers_pb2_grpc.LeversServiceStub(self._channel)

    def connect(
        self,
        user="",
        password="",
        db_name=""
    ):
        client_info = ClientInfo(
            sdk_type='python',
            sdk_version=__version__,
            local_time=str(time.time()),
            user=user,
            password=password,
            db_name=db_name,
            host=self._host)
        req = levers_pb2.ConnectRequest()
        req.client_info.CopyFrom(client_info.to_pb())
        pb_rsp = self._stub.Connect(req)
        rsp = ConnectResult.from_pb(pb_rsp)
        return rsp.status, rsp.results

    def create_database(self, database_schema):
        req = levers_pb2.CreateDatabaseRequest()
        pb_database_schema = database_schema.to_pb()
        req.schema.CopyFrom(pb_database_schema)
        rsp = self._stub.CreateDatabase(req)
        return Status.from_pb(rsp)

    def drop_database(self, db_name):
        req = levers_pb2.DropDatabaseRequest()
        req.db_name = db_name
        rsp = self._stub.DropDatabase(req)
        return Status.from_pb(rsp)

    def list_databases(self):
        pb_rsp = self._stub.ListDatabase(Empty())
        return Status.from_pb(pb_rsp.status), pb_rsp.db_names

    def create_collection(self, db_name, collection_schema):
        req = levers_pb2.CreateCollectionRequest()
        pb_collection_schema = collection_schema.to_pb()
        req.schema.CopyFrom(pb_collection_schema)
        req.db_name = db_name
        rsp = self._stub.CreateCollection(req)
        return Status.from_pb(rsp)

    def drop_collection(self, db_name, collection_name):
        req = levers_pb2.DropCollectionRequest()
        req.collection_name = collection_name
        req.db_name = db_name
        rsp = self._stub.DropCollection(req)
        return Status.from_pb(rsp)

    def list_collections(self, db_name):
        req = levers_pb2.ListCollectionsRequest()
        req.db_name = db_name
        pb_rsp = self._stub.ListCollections(req)
        rsp = ListResult.from_pb(pb_rsp)
        return rsp.status, rsp.results

    def describe_collection(self, db_name, collection_name):
        req = levers_pb2.DescribeCollectionRequest()
        req.collection_name = collection_name
        req.db_name = db_name
        pb_rsp = self._stub.DescribeCollection(req)
        rsp = DescribeResult.from_pb(pb_rsp)
        return rsp.status, rsp.results

    def stats_collection(self, db_name, collection_name):
        req = levers_pb2.StatsCollectionRequest()
        req.collection_name = collection_name
        req.db_name = db_name
        pb_rsp = self._stub.StatsCollection(req)
        rsp = StatsResult.from_pb(pb_rsp)
        return rsp.status, rsp.results

    def insert(self, db_name, collection_name, entity_metas, entity_datas):
        if collection_name is None or len(collection_name) == 0:
            raise LeversException("collection name is not valid")

        if len(entity_metas) == 0:
            raise LeversException("no entity meta")

        if len(entity_datas) > 1000:
            raise LeversException("insert entity data size is too large")

        for index, entity_data in enumerate(entity_datas):
            try:
                entity_data._valid_check()
            except LeversException:
                raise LeversException("entity data " + str(index) + " not valid")

        pb_insert_request = levers_pb2.InsertRequest()
        pb_insert_request.collection_name = collection_name
        pb_insert_request.entity_metas.extend(
            entity_meta.to_pb() for entity_meta in entity_metas)
        pb_insert_request.entity_datas.extend(
            entity_data.to_pb(entity_metas) for entity_data in entity_datas)
        pb_insert_request.db_name = db_name
        pb_rsp = self._stub.Insert(pb_insert_request)
        rsp = MutableResult.from_pb(pb_rsp)
        return rsp.status, rsp

    def update(self, db_name, collection_name, entity_metas, entity_datas):
        if collection_name is None or len(collection_name) == 0:
            raise LeversException("collection name is not valid")

        if len(entity_metas) == 0:
            raise LeversException("no entity meta")

        for index, entity_data in enumerate(entity_datas):
            try:
                entity_data._valid_check()
            except LeversException:
                raise LeversException("entity data " + str(index) + " not valid")

        pb_update_request = levers_pb2.UpdateRequest()
        pb_update_request.collection_name = collection_name
        pb_update_request.entity_metas.extend(
            entity_meta.to_pb() for entity_meta in entity_metas)
        pb_update_request.entity_datas.extend(
            entity_data.to_pb(entity_metas) for entity_data in entity_datas)
        pb_update_request.db_name = db_name
        pb_rsp = self._stub.Update(pb_update_request)
        rsp = MutableResult.from_pb(pb_rsp)
        return rsp.status, rsp


    def delete(self, db_name, collection_name, pks, expr):
        if collection_name is None or len(collection_name) == 0:
            raise LeversException("collection name is not valid")

        if pks is None and expr is None:
            raise LeversException("no delete condition")
        if pks is not None and expr is not None:
            raise LeversException("both pks and expr exist")
               
        if pks is not None:
            for index, pk in enumerate(pks):
                if not isinstance(pk, int):
                    raise LeversException("entity pk " + str(index) + " not valid")

        pb_delete_request = levers_pb2.DeleteRequest()
        pb_delete_request.collection_name = collection_name
        if pks:
            pb_delete_request.pks.pk.extend(pks)
        elif expr:
            pb_delete_request.expr = expr
        pb_delete_request.db_name = db_name
        pb_rsp = self._stub.Delete(pb_delete_request)
        rsp = MutableResult.from_pb(pb_rsp)
        return rsp.status, rsp

    def search(self, db_name, collection_name, knn_param, topk, filter, output_fields, extra_params, score_limit):
        if collection_name is None or len(collection_name) == 0:
            raise LeversException("collection name is not valid")
        if score_limit is not None and not isinstance(score_limit, float):
            raise LeversException("score_limit is not valid")

        pb_search_request = levers_pb2.SearchRequest()
        pb_search_request.collection_name = collection_name
        if knn_param is not None:
            pb_search_request.knn_param.CopyFrom(knn_param.to_pb())
        pb_search_request.topk = topk
        if filter:
            pb_search_request.filter = filter
        pb_search_request.output_fields.extend(output_fields)
        if isinstance(extra_params, dict) and extra_params:
            _extra_params = {}
            for _param_k, _param_v in extra_params.items():
                if isinstance(_param_v, str):
                    _extra_params[_param_k] = _param_v
                else:
                    _extra_params[_param_k] = str(_param_v)
            pb_search_request.extra_params.update(_extra_params)
        pb_search_request.db_name = db_name
        pb_rsp = self._stub.Search(pb_search_request)
        rsp = SearchResults.from_pb(pb_rsp, score_limit)
        return rsp.status, rsp.results

    def get(self, db_name, collection_name, pk, output_fields, extra_params):
        if collection_name is None or len(collection_name) == 0:
            raise LeversException("collection name is not valid")

        pb_get_request = levers_pb2.GetRequest()
        pb_get_request.collection_name = collection_name
        pb_get_request.pk = pk
        pb_get_request.output_fields.extend(output_fields)
        if extra_params is not None:
            pb_get_request.extra_params.update(extra_params)
        pb_get_request.db_name = db_name
        pb_rsp = self._stub.Get(pb_get_request)
        rsp = GetResult.from_pb(pb_rsp)
        return rsp.status, rsp.entity_data

    def close(self):
        self._channel.close()
