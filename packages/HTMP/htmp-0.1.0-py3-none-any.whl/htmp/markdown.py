from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from htmp.protocol import Stringable


class Markdown:
    
    _IS_MD_CODE = True
    
    def __init__(self, content: Stringable):
        self.content = content
        return
    
    def __str__(self) -> str:
        return str(self.content)