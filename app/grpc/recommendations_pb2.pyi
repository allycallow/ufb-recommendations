from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IdRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class PaginatedIdRequest(_message.Message):
    __slots__ = ("id", "page", "page_size")
    ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    id: str
    page: int
    page_size: int
    def __init__(
        self,
        id: _Optional[str] = ...,
        page: _Optional[int] = ...,
        page_size: _Optional[int] = ...,
    ) -> None: ...

class StringListResponse(_message.Message):
    __slots__ = ("success", "items")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    items: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, success: _Optional[bool] = ..., items: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class PaginatedStringListResponse(_message.Message):
    __slots__ = ("success", "items", "page", "page_size", "total")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    success: bool
    items: _containers.RepeatedScalarFieldContainer[str]
    page: int
    page_size: int
    total: int
    def __init__(
        self,
        success: _Optional[bool] = ...,
        items: _Optional[_Iterable[str]] = ...,
        page: _Optional[int] = ...,
        page_size: _Optional[int] = ...,
        total: _Optional[int] = ...,
    ) -> None: ...

class StructListResponse(_message.Message):
    __slots__ = ("success", "items")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    items: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    def __init__(
        self,
        success: _Optional[bool] = ...,
        items: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ...,
    ) -> None: ...
