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

    status, results = client.get(
        collection_name,
        pk=6,
        output_fields=["id", "vector"],
        extra_params={}
    )
    print(status)
    print(results)
    print(json.dumps(results, cls=MyEncoder, indent = 4) )

    status, results = client.get(
        collection_name,
        pk=6666,
        output_fields=["id", "vector"],
        extra_params={}
    )
    print(status)
    print(results)
    print(json.dumps(results, cls=MyEncoder, indent = 4) )
