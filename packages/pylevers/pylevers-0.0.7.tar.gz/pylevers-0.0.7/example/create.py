#!/usr/bin/python3

import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir+"/..")
import json

from pylevers import *
from pylevers.core.types import *

from example import *

if __name__ == '__main__':
    print('test')
    HOST = '127.0.0.1'
    GRPC_PORT = 8099
    client = Client(HOST, GRPC_PORT)
    collection_name = "test"

    print('test connect')
    client.connect("1","2","3")

    field1_indexed_segment_schema = IndexSchema(
        index_type=IndexType.STL)
    field2_indexed_segment_schema = IndexSchema(
        index_type=IndexType.SPANN,
        index_metrics=IndexMetrics.L2,
        index_quant_type=IndexQuantType.NONE,
        extra_params={'M': '30', 'efConstruction': '360', 'forTest': 'test_str'})

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
            extra_params={'shard_num': '1'})

    status = client.create_collection(collection_schema)
    print(status)
