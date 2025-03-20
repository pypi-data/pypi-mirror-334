from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from htmp.container import Container


class Comment:

    _IS_HTML_CODE = True

    def __init__(self, content: Container):
        self.content = content
        return

    def source(self, indent: int = 3):
        open_tag = "<!--"
        close_tag = "-->"
        content = self.content.source(indent=indent)
        if indent < 0:
            sep = " "
        else:
            sep = "\n"
            if indent > 0:
                content = "\n".join([f"{indent * ' '}{line}" for line in content.split("\n")])
        return f"{open_tag}{sep}{content}{sep}{close_tag}"

    def __str__(self):
        return self.source(indent=-1)
