# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: image_search.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12image_search.proto\"#\n\x0cImageRequest\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\"6\n\rImageResponse\x12\x12\n\nimage_data\x18\x01 \x01(\x0c\x12\x11\n\timage_url\x18\x02 \x01(\t2;\n\x0bImageSearch\x12,\n\x0bSearchImage\x12\r.ImageRequest\x1a\x0e.ImageResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'image_search_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_IMAGEREQUEST']._serialized_start=22
  _globals['_IMAGEREQUEST']._serialized_end=57
  _globals['_IMAGERESPONSE']._serialized_start=59
  _globals['_IMAGERESPONSE']._serialized_end=113
  _globals['_IMAGESEARCH']._serialized_start=115
  _globals['_IMAGESEARCH']._serialized_end=174
# @@protoc_insertion_point(module_scope)
