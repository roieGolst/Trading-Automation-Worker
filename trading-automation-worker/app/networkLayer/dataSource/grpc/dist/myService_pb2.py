"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'myService.proto')
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from . import types_pb2 as types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fmyService.proto\x12\tMyService\x1a\x19google/protobuf/any.proto\x1a\x0btypes.proto2\xb3\x01\n\tMyService\x124\n\nActivation\x12\x15.Types.ActivationTask\x1a\x0f.Types.Response\x128\n\x0cDeactivation\x12\x17.Types.DeactivationTask\x1a\x0f.Types.Response\x126\n\x0bTransaction\x12\x16.Types.TransactionTask\x1a\x0f.Types.Responseb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'myService_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_MYSERVICE']._serialized_start = 71
    _globals['_MYSERVICE']._serialized_end = 250