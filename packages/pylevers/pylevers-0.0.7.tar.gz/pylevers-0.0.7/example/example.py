#!/usr/bin/python3  

import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir+"/..")

import time
import numpy as np
from collections.abc import Iterable
import json

from pylevers import *
from pylevers.core.types import *


def connect():
    status, server_info = client.connect("test_user", "test_passwd", "test_db")
    print(status, server_info)

def create_collection():
    field1_indexed_segment_schema = IndexSchema(
        index_type=IndexType.STL)
    field2_indexed_segment_schema = IndexSchema(
        index_type=IndexType.SPANN,
        index_metrics=IndexMetrics.L2,
        index_quant_type=IndexQuantType.NONE,
        extra_params={'M': '30', 'efConstruction': '360'})

    fields = [
        FieldSchema(name='id',
                    data_type=DataType.INT64,
                    dimension=0,
                    indexed_segment_schema=field1_indexed_segment_schema),
        FieldSchema(name='vector',
                    data_type=DataType.FLOAT_VECTOR,
                    dimension=8,
                    indexed_segment_schema=field2_indexed_segment_schema
                    )
    ]

    collection_schema = CollectionSchema(
            name=collection_name,
            description="This is a sample collection",
            fields=fields,
            extra_params={'shard_num':'1'})

    status = client.create_collection(collection_schema)
    print(status)

def describe_collection():
    status, schema = client.describe_collection(collection_name)
    print(status)
    print(schema)

def drop_collection():
    status = client.drop_collection(collection_name)
    print(status)

def list_collections():
    status, collection_name_list = client.list_collections()
    print(status)
    print(collection_name_list)

def stats_collection():
    status, stats = client.stats_collection(collection_name)
    print(status)
    print(stats)

def insert():
    entity_datas = []
    for i in range(100):
        array = np.random.rand(8).astype(np.float32)
        field_values = [i, array.tobytes()]
        entity_datas.append(EntityData(pk = i+1, field_values = field_values))
    
    entity_metas = [
        EntityMeta('id', DataType.INT64),
        EntityMeta('vector', DataType.FLOAT_VECTOR)
    ]
    
    status, result = client.insert(collection_name, entity_metas, entity_datas)
    print(status)
    print(result)

def insert_auto_pk():
    entity_datas = []
    for i in range(100):
        array = np.random.rand(8).astype(np.float32)
        field_values = [i, array.tobytes()]
        entity_datas.append(EntityData(pk = 0, field_values = field_values))

    entity_metas = [
        EntityMeta('id', DataType.INT64),
        EntityMeta('vector', DataType.FLOAT_VECTOR)
    ]

    status, result = client.insert(collection_name, entity_metas, entity_datas)
    print(status)
    print(result)

def update():
    entity_datas = []
    for i in range(100):
        array = np.random.rand(8).astype(np.float32)
        field_values = [i+100, array.tobytes()]
        entity_datas.append(EntityData(pk = i+1, field_values = field_values))
    
    entity_metas = [
        EntityMeta('id', DataType.INT64),
        EntityMeta('vector', DataType.FLOAT_VECTOR)
    ]

    status, result = client.update(collection_name, entity_metas, entity_datas)
    print(status)
    print(result)

def delete():
    status, results = client.delete(collection_name, pks = [1])
    print(status)
    print(results)
    # status, results = client.delete(collection_name, expr = "id < 10")
    # print(status)
    # print(results)

def search():
    array = np.array([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]],
                     dtype=np.float32)

    knn_params = KnnParam(
        field_name='vector',
        vectors=array.tobytes(),
        batch_count=1,
        is_bruteforce=False
    )
    status, results = client.search(
        collection_name,
        knn_param=knn_params,
        topk=10,
        output_fields=["id", "vector"],
        extra_params={}
    )
    print(status)
    print(results)

def get():
    status, results = client.get(
        collection_name,
        pk=5,
        output_fields=["id", "vector"],
        extra_params={}
    )
    print(status)
    print(results)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (CollectionStats,ShardStats,SegmentStats)):
            return obj.__dict__
        if isinstance(obj, CollectionSchema):
            return obj.__dict__
        if isinstance(obj, FieldSchema):
            return obj.__dict__
        if isinstance(obj, IndexSchema):
            return obj.__dict__.values()
        if isinstance(obj, EntityResult):
            return obj.__dict__
        if isinstance(obj, FieldData):
            return str(obj)
        if hasattr(obj, 'items') and callable(obj.items):
            return str(obj)
        if isinstance(obj, Iterable):
            return ", " . join([str(item) for item in obj])
        if isinstance(obj, Enum):
            return str(obj)
        return super(MyEncoder, self).default(obj)


if __name__ == '__main__':
    print('test')
    HOST = '127.0.0.1'
    GRPC_PORT = 8099
    client = Client(HOST, GRPC_PORT)
    collection_name = "test"

    print('test connect')
    connect()

    print('test create_collection')
    create_collection()

    print('test describe_collection')
    describe_collection()

    print('test list_collections')
    list_collections()

    print('test insert')
    insert()

    print('test insert auto pk')
    insert_auto_pk()

    print('test update')
    update()

    print('test delete')
    delete()

    print('test search')
    search()

    print('test get')
    get()
    time.sleep(3)
    print('test stats_collection')
    stats_collection()

    print('test drop_collection')
    drop_collection()

    time.sleep(1)

    client.close()
