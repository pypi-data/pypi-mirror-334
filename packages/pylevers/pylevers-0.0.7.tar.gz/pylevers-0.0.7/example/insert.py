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

    if len(sys.argv) == 1:
        sys.argv.append(0)
    entity_datas = []
    for i in range(999):
        array = np.random.rand(8).astype(np.float32)
        field_values = [i, array.tobytes()]
        entity_datas.append(EntityData(pk = i + int(sys.argv[1]), field_values = field_values))
    
    entity_metas = [
        EntityMeta('id', DataType.INT64),
        EntityMeta('vector', DataType.FLOAT_VECTOR)
    ]
    
    status, result = client.insert(collection_name, entity_metas, entity_datas)
    print(status)
    #print(result)
