# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: viral.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='viral.proto',
  package='viral_wars',
  syntax='proto2',
  serialized_pb=_b('\n\x0bviral.proto\x12\nviral_wars\"\x1a\n\tGameBoard\x12\r\n\x05\x62oard\x18\x01 \x02(\t')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_GAMEBOARD = _descriptor.Descriptor(
  name='GameBoard',
  full_name='viral_wars.GameBoard',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='board', full_name='viral_wars.GameBoard.board', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=53,
)

DESCRIPTOR.message_types_by_name['GameBoard'] = _GAMEBOARD

GameBoard = _reflection.GeneratedProtocolMessageType('GameBoard', (_message.Message,), dict(
  DESCRIPTOR = _GAMEBOARD,
  __module__ = 'viral_pb2'
  # @@protoc_insertion_point(class_scope:viral_wars.GameBoard)
  ))
_sym_db.RegisterMessage(GameBoard)


# @@protoc_insertion_point(module_scope)
