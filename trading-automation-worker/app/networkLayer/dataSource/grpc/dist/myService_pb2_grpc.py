"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from . import types_pb2 as types__pb2
GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in myService_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class MyServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Activation = channel.unary_unary('/MyService.MyService/Activation', request_serializer=types__pb2.ActivationTask.SerializeToString, response_deserializer=types__pb2.Response.FromString, _registered_method=True)
        self.Deactivation = channel.unary_unary('/MyService.MyService/Deactivation', request_serializer=types__pb2.DeactivationTask.SerializeToString, response_deserializer=types__pb2.Response.FromString, _registered_method=True)
        self.Transaction = channel.unary_unary('/MyService.MyService/Transaction', request_serializer=types__pb2.TransactionTask.SerializeToString, response_deserializer=types__pb2.Response.FromString, _registered_method=True)

class MyServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Activation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Deactivation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Transaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_MyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'Activation': grpc.unary_unary_rpc_method_handler(servicer.Activation, request_deserializer=types__pb2.ActivationTask.FromString, response_serializer=types__pb2.Response.SerializeToString), 'Deactivation': grpc.unary_unary_rpc_method_handler(servicer.Deactivation, request_deserializer=types__pb2.DeactivationTask.FromString, response_serializer=types__pb2.Response.SerializeToString), 'Transaction': grpc.unary_unary_rpc_method_handler(servicer.Transaction, request_deserializer=types__pb2.TransactionTask.FromString, response_serializer=types__pb2.Response.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('MyService.MyService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('MyService.MyService', rpc_method_handlers)

class MyService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Activation(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MyService.MyService/Activation', types__pb2.ActivationTask.SerializeToString, types__pb2.Response.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def Deactivation(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MyService.MyService/Deactivation', types__pb2.DeactivationTask.SerializeToString, types__pb2.Response.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def Transaction(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MyService.MyService/Transaction', types__pb2.TransactionTask.SerializeToString, types__pb2.Response.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)