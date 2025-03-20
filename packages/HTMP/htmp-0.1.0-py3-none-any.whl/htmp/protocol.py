from typing import Protocol as _Protocol, runtime_checkable as _runtime_checkable, Any

from protocolman import Stringable


@_runtime_checkable
class HTMLCode(_Protocol):
    """An object representing HTML code."""

    _IS_HTML_CODE: Any

    def source(self, indent: int) -> str:
        ...


@_runtime_checkable
class MDCode(_Protocol):
    """An object representing Markdown code."""

    _IS_MD_CODE: Any

    def __str__(self) -> str:
        ...



ContentType = Stringable | HTMLCode | MDCode
ContainerContentType = dict[str | int, ContentType]
ContentInputType = (
    ContainerContentType
    | list[ContentType]
    | tuple[ContentType]
    | ContentType
    | None
)

AttrsType = dict[str, Stringable | bool | list[Stringable], dict[Stringable, Stringable]]
AttrsInputType = AttrsType | None

TableCellContent = Stringable | tuple[Stringable, AttrsType]
TableRowContent = list[TableCellContent]
TableRowsContent = list[TableRowContent | tuple[TableRowContent, AttrsType]]