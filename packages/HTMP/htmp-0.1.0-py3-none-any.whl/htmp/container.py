from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from htmp.protocol import HTMLCode as _HTMLCode, MDCode as _MDCode
from htmp import display as _display

if _TYPE_CHECKING:
    from htmp.protocol import ContentType, ContainerContentType


class Container:

    _IS_HTML_CODE = True

    def __init__(self, content: ContainerContentType | None = None):
        self._data = content or {}
        return

    def source(self, indent: int = 3) -> str:
        str_sep = " " if indent < 0 else "\n"
        in_str = False
        contents = []
        curr_str_elements = []
        for content in self._data.values():
            if not isinstance(content, (_HTMLCode, _MDCode)):
                curr_str_elements.append(str(content))
                in_str = True
                continue
            if in_str:
                contents.append(str_sep.join(curr_str_elements))
                curr_str_elements = []
                in_str = False
            if isinstance(content, (Container, _HTMLCode)):
                contents.append(content.source(indent=indent))
            else:
                # Markdown element
                md_sep = "\n\n" if indent < 0 else "\n"
                contents.append(f"{md_sep}{str(content).strip()}{md_sep}")
        content_sep = "" if indent < 0 else "\n"
        if curr_str_elements:
            contents.append(str_sep.join(curr_str_elements))
        return content_sep.join(contents)

    def display(self, ipython: bool = False, as_md: bool = False) -> None:
        """Display the element in an IPython notebook."""
        if ipython:
            return _display.ipython(str(self), as_md=as_md)
        return _display.browser(str(self))

    def add(self, *unlabeled_contents: ContentType, **labeled_contents: ContentType) -> list[int] | None:
        if labeled_contents:
            for key, value in labeled_contents.items():
                if key in self._data:
                    raise ValueError("Key already exists in content.")
                self._data[key] = value
        if unlabeled_contents:
            first_available_int_key = max((key for key in self._data.keys() if isinstance(key, int)), default=0) + 1
            for idx, elem in enumerate(unlabeled_contents):
                self._data[first_available_int_key + idx] = elem
            return list(range(first_available_int_key, first_available_int_key + len(unlabeled_contents)))
        return

    def get(self, key: str | int, default=None):
        return self._data.get(key, default)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value
        return

    def __contains__(self, item):
        return item in self._data

    def __bool__(self):
        return bool(self._data)

    def __str__(self) -> str:
        self.source(indent=-1)
