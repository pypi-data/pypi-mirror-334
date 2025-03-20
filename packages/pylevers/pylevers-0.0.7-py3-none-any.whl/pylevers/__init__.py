import grpc
# hack to import proto
import sys
import os.path
sys.path.insert(0, os.path.dirname(__file__))
# sys.path.append(os.path.join(os.path.dirname(__file__), 'proto'))

from .version import __version__

from .core.client import Client
from .core.types import DataType
from .core.types import IndexType
from .core.types import IndexMetrics
from .core.types import IndexQuantType
from .core.types import IndexSchema
from .core.types import KnnParam
from .core.types import ClientInfo
from .core.types import FieldSchema
from .core.types import CollectionSchema

sys.path.pop(0)
del sys
del os
