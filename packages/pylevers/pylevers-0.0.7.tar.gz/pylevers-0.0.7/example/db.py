
from pylevers import *
from pylevers.core.types import *

def create_database():
    print('create_database')
    db_schema = DatabaseSchema(
        db_name=db_name,
        extra_params={}
    )
    status = client.create_database(db_schema)
    print(status)

def drop_database():
    print('drop_database')
    status = client.drop_database(db_name)
    print(status)

def list_databases():
    print('list_databases')
    status, db_name_list = client.list_databases()
    print(status)
    print(db_name_list)

if __name__ == '__main__':
    print('test')
    # HOST = '127.0.0.1'
    HOST = '10.121.206.4'
    GRPC_PORT = 8099
    client = Client(HOST, GRPC_PORT)
    db_name = "test_db"

    client.connect(
        user="admin",
        password="admin",
    )
    create_database()
    drop_database()
    list_databases()