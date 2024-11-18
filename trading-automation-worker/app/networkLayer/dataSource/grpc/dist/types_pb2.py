"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'types.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0btypes.proto\x12\x05Types"(\n\x08BaseTask\x12\x1c\n\x07task_id\x18\x02 \x01(\x0b2\x0b.Types.UUID"\x15\n\x04UUID\x12\r\n\x05value\x18\x01 \x01(\t":\n\x08Response\x12\x1d\n\x06status\x18\x01 \x01(\x0e2\r.Types.Status\x12\x0f\n\x07message\x18\x02 \x01(\t"\xa1\x01\n\x0eActivationTask\x12"\n\tbase_task\x18\x01 \x01(\x0b2\x0f.Types.BaseTask\x12#\n\tbrokerage\x18\x02 \x01(\x0e2\x10.Types.Brokerage\x12\x1f\n\naccount_id\x18\x03 \x01(\x0b2\x0b.Types.UUID\x12%\n\x05creds\x18\x04 \x01(\x0b2\x16.Types.ActivationCreds"\xc5\x02\n\x0fActivationCreds\x12\x15\n\x08username\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x15\n\x08password\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x12\n\x05email\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x19\n\x0caccess_token\x18\x04 \x01(\tH\x03\x88\x01\x01\x12\x16\n\tdevice_id\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x18\n\x0btrading_pin\x18\x06 \x01(\tH\x05\x88\x01\x01\x12\x10\n\x03otp\x18\x07 \x01(\tH\x06\x88\x01\x01\x12\x1f\n\x12phone_verification\x18\x08 \x01(\tH\x07\x88\x01\x01B\x0b\n\t_usernameB\x0b\n\t_passwordB\x08\n\x06_emailB\x0f\n\r_access_tokenB\x0c\n\n_device_idB\x0e\n\x0c_trading_pinB\x06\n\x04_otpB\x15\n\x13_phone_verification"W\n\x10DeactivationTask\x12"\n\tbase_task\x18\x01 \x01(\x0b2\x0f.Types.BaseTask\x12\x1f\n\naccount_id\x18\x02 \x01(\x0b2\x0b.Types.UUID"\x7f\n\x0fTransactionTask\x12"\n\tbase_task\x18\x01 \x01(\x0b2\x0f.Types.BaseTask\x12(\n\x06method\x18\x02 \x01(\x0e2\x18.Types.TransactionMethod\x12\x0e\n\x06amount\x18\x03 \x01(\x05\x12\x0e\n\x06ticker\x18\x04 \x01(\t*\xd9\x01\n\tBrokerage\x12\x08\n\x04BBAE\x10\x00\x12\t\n\x05Chase\x10\x01\x12\t\n\x05DSPAC\x10\x02\x12\n\n\x06Fennel\x10\x03\x12\x0c\n\x08Fidelity\x10\x04\x12\r\n\tFirstrade\x10\x05\x12\n\n\x06Public\x10\x06\x12\r\n\tRobinhood\x10\x07\x12\n\n\x06Schwab\x10\x08\x12\x08\n\x04SoFi\x10\t\x12\x0b\n\x07Tornado\x10\n\x12\x0b\n\x07Tradier\x10\x0b\x12\x0e\n\nTastytrade\x10\x0c\x12\n\n\x06Webull\x10\r\x12\x0c\n\x08Vanguard\x10\x0e\x12\x0e\n\nWellsFargo\x10\x0f*"\n\x06Status\x12\x0b\n\x07Success\x10\x00\x12\x0b\n\x07Failure\x10\x01*&\n\x11TransactionMethod\x12\x08\n\x04Sell\x10\x00\x12\x07\n\x03Buy\x10\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'types_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_BROKERAGE']._serialized_start = 858
    _globals['_BROKERAGE']._serialized_end = 1075
    _globals['_STATUS']._serialized_start = 1077
    _globals['_STATUS']._serialized_end = 1111
    _globals['_TRANSACTIONMETHOD']._serialized_start = 1113
    _globals['_TRANSACTIONMETHOD']._serialized_end = 1151
    _globals['_BASETASK']._serialized_start = 22
    _globals['_BASETASK']._serialized_end = 62
    _globals['_UUID']._serialized_start = 64
    _globals['_UUID']._serialized_end = 85
    _globals['_RESPONSE']._serialized_start = 87
    _globals['_RESPONSE']._serialized_end = 145
    _globals['_ACTIVATIONTASK']._serialized_start = 148
    _globals['_ACTIVATIONTASK']._serialized_end = 309
    _globals['_ACTIVATIONCREDS']._serialized_start = 312
    _globals['_ACTIVATIONCREDS']._serialized_end = 637
    _globals['_DEACTIVATIONTASK']._serialized_start = 639
    _globals['_DEACTIVATIONTASK']._serialized_end = 726
    _globals['_TRANSACTIONTASK']._serialized_start = 728
    _globals['_TRANSACTIONTASK']._serialized_end = 855