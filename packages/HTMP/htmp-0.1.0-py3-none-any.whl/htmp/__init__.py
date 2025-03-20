"""Generate and process HTML content.

References
----------
- [HTML Living Standard](https://html.spec.whatwg.org/)
- [HTML elements reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)
- [HTML document structure](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started#anatomy_of_an_html_element)
"""
from __future__ import annotations
from typing import TYPE_CHECKING as _TYPE_CHECKING

from htmp.comment import Comment
from htmp.container import Container
from htmp.document import Document
from htmp.element import Element
from htmp import display, element, elementor, spec

if _TYPE_CHECKING:
    from htmp.protocol import ContentType, ContentInputType, AttrsInputType


def comment(
    *unlabeled_contents: ContentType,
    **labeled_contents: ContentType
) -> Comment:
    return Comment(content=container(*unlabeled_contents, **labeled_contents))


def container(
    *unlabeled_contents: ContentType,
    **labeled_contents: ContentType,
) -> Container:
    container_ = Container()
    container_.add(*unlabeled_contents, **labeled_contents)
    return container_


def container_from_object(content: ContentInputType = None) -> Container:
    if isinstance(content, Container):
        return content
    container_ = Container()
    if not content:
        return container_
    if isinstance(content, dict):
        container_.add(**content)
        return container_
    if isinstance(content, (list, tuple)):
        container_.add(*content)
        return container_
    container_.add(content)
    return container_


def document(
    content_head: ContentInputType = None,
    content_body: ContentInputType = None,
    attrs_head: AttrsInputType = None,
    attrs_body: AttrsInputType = None,
    attrs_html: AttrsInputType = None,
    doctype: str = "html",
) -> Document:
    return Document(
        container_from_object(content_head),
        container_from_object(content_body),
        attrs_head=attrs_head,
        attrs_body=attrs_body,
        attrs_html=attrs_html,
        doctype=doctype,
    )
