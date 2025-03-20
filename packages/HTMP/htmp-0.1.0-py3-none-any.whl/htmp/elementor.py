from __future__ import annotations

import re as _re
from typing import TYPE_CHECKING as _TYPE_CHECKING

import htmp
import htmp.element as _el
from htmp.markdown import Markdown as _Markdown

if _TYPE_CHECKING:
    from typing import Literal
    from htmp.protocol import ContentInputType, AttrsInputType, Stringable, TableRowsContent


def custom_element(
    name: str,
    content: ContentInputType = None,
    attrs: AttrsInputType = None,
    void: bool = False,
) -> _el.ContentElement | _el.VoidElement:
    if void:
        return _el.VoidElement(name=name, attrs=attrs)
    return _el.ContentElement(
        name=name,
        content=htmp.container_from_object(content),
        attrs=attrs,
    )


def markdown(content: Stringable) -> _Markdown:
    return _Markdown(content)


def heading(
    level: Literal[1, 2, 3, 4, 5, 6],
    content: ContentInputType = None,
    attrs: AttrsInputType = None,
) -> _el.H1 | _el.H2 | _el.H3 | _el.H4 | _el.H5 | _el.H6:
    """Create a heading element (`<h1>`, `<h2>`, etc.) with the given level."""
    h_map = {1: _el.h1, 2: _el.h2, 3: _el.h3, 4: _el.h4, 5: _el.h5, 6: _el.h6}
    return h_map[level](content, attrs)


def paragraph(
    text: Stringable,
    style: dict[str, dict] | None = None,
    align: Literal["left", "center", "right", "justify"] = None,
    attrs: AttrsInputType = None,
) -> _el.P:
    text = str(text)
    for word, word_style in (style or {}).items():
        text = text_style(text=text, word=word, **word_style)
    attrs = attrs or {}
    if align:
        attrs["align"] = align
    return _el.p(text, attrs)


def picture_color_scheme(
    src_light: Stringable,
    src_dark: Stringable,
    attrs_img: AttrsInputType = None,
    attrs_picture: AttrsInputType = None,
    attrs_source_light: AttrsInputType = None,
    attrs_source_dark: AttrsInputType = None,
    default_light: bool = True,
) -> _el.PICTURE:
    """Create a <picture> element with a <source> element for light and dark color schemes.

    Parameters
    ----------
    src_light : Stringable
        The URI of the image for the light color scheme.
    src_dark : Stringable
        The URI of the image for the dark color scheme.
    attrs_picture : ElementAttributesDictType, optional
        Attributes for the <picture> element.
    attrs_source_light : ElementAttributesDictType, optional
        Attributes for the <source> element for the light color scheme.
    attrs_source_dark : ElementAttributesDictType, optional
        Attributes for the <source> element for the dark color scheme.
    attrs_img : ElementAttributesDictType, optional
        Attributes for the <img> element.
    default_light: bool, optional
        If True, the 'src' attribute of the <img> element will be set to `src_light`,
        when 'src' is not provided. If False, it will be set to `src_dark`.

    Returns
    -------
    Picture
        A <picture> element with a <source> element for light and dark color schemes.
    """
    args = locals()
    sources_attributes = []
    for theme in ("light", "dark"):
        src = args[f"src_{theme}"]
        src_attrs = (args[f"attrs_source_{theme}"] or {}) | {
            "srcset": src,
            "media": f"(prefers-color-scheme: {theme})",
        }
        sources_attributes.append(src_attrs)
    img_attributes_full = {
        "src": args["src_light" if default_light else "src_dark"]
    } | (attrs_img or {})
    return picture_from_sources(src=src_light, attrs_sources=sources_attributes, attrs_picture=attrs_picture, attrs_img=img_attributes_full)


def picture_from_sources(
    src: Stringable,
    attrs_sources: list[AttrsInputType],
    attrs_picture: AttrsInputType = None,
    attrs_img: AttrsInputType = None,
) -> _el.PICTURE:
    """Create a <picture> element with multiple <source> elements and an <img> element.

    Parameters
    ----------
    src : Stringable
        The URI of the image for the <img> element.
    attrs_sources : list[ElementAttributesDictType]
        A list of attributes for each <source> element.
    attrs_picture : ElementAttributesDictType, optional
        Attributes for the <picture> element.
    attrs_img : ElementAttributesDictType, optional
        Attributes for the <img> element other than 'src'.

    Returns
    -------
    Picture
        A <picture> element with multiple <source> elements and an <img> element.
    """
    sources = [_el.source(attrs) for attrs in attrs_sources]
    attrs_img = (attrs_img or {}) | {"src": src}
    return _el.picture(sources + [_el.img(attrs_img)], attrs_picture)


def table_from_rows(
    rows_body: TableRowsContent,
    rows_head: TableRowsContent | None = None,
    rows_foot: TableRowsContent | None = None,
    as_figure: bool = False,
    caption: Stringable = None,
    num_cols_stub: int = 0,
    attrs_figure: AttrsInputType = None,
    attrs_caption: AttrsInputType = None,
    attrs_table: AttrsInputType = None,
    attrs_body: AttrsInputType = None,
    attrs_head: AttrsInputType = None,
    attrs_foot: AttrsInputType = None,
    attrs_tr: AttrsInputType = None,
    attrs_th: AttrsInputType = None,
    attrs_td: AttrsInputType = None,
    attrs_body_tr: AttrsInputType = None,
    attrs_body_th: AttrsInputType = None,
    attrs_body_td: AttrsInputType = None,
    attrs_head_tr: AttrsInputType = None,
    attrs_head_th: AttrsInputType = None,
    attrs_head_td: AttrsInputType = None,
    attrs_foot_tr: AttrsInputType = None,
    attrs_foot_th: AttrsInputType = None,
    attrs_foot_td: AttrsInputType = None,
) -> _el.TABLE | _el.FIGURE:
    """Create a <table> element (optionally inside a <figure>) from rows of data.

    Parameters
    ----------
    rows_body : TableRowsContentType
        A list of rows for the table body.
        Each row is a list of cells,
        where each cell is either a content or a tuple of content and attributes.
        A cell content can be `markitup.html.Element` or `markitup.protocol.Stringable`
        (i.e., any object that can be converted to a string).
        If a cell content is a `markitup.html.element.Th` or `markitup.html.element.Td` element,
        it is used as is, otherwise it will be used to create one (see also `first_cell_header`).
    rows_head : TableRowsContentType, optional
        A list of rows for the table head.
        Same as `body_rows`, but each cell will be rendered as a `<th scope="col">` element.
    rows_foot : TableRowsContentType, optional
        A list of rows for the table foot; same as `body_rows`.
    as_figure : bool, optional
        If True, the table will be wrapped in a `<figure>` element.
        Also, if provided, the `caption` parameter will be used
        as a `<figcaption>` element inside the `<figure>`
        instead of a `<caption>` element inside the `<table>`.
    caption : ElementContentType, optional
        The caption for the table or figure.
        If it is a `markitup.html.element.Caption` or `markitup.html.element.Figcaption` element,
        it will be used as is,
        otherwise it will be used to create a `<caption>` or `<figcaption>` element (cf. `as_figure`).
    num_cols_stub : int, default: 0
        Number of cells in each row to be rendered as `<th>` instead of `<td>` elements.
        This parameter is ignored for the head rows.
    attrs_figure : ElementAttributesDictType, optional
        Attributes for the `<figure>` element, if `as_figure` is set to `True`.
    attrs_caption : ElementAttributesDictType, optional
        Attributes for the `<caption>` or `<figcaption>` element, if provided.
    attrs_table : ElementAttributesDictType, optional
        Attributes for the `<table>` element.
    attrs_body : ElementAttributesDictType, optional
        Attributes for the `<tbody>` element.
    attrs_head : ElementAttributesDictType, optional
        Attributes for the `<thead>` element.
    attrs_foot : ElementAttributesDictType, optional
        Attributes for the `<tfoot>` element.
    attrs_tr : ElementAttributesDictType, optional
        Attributes for all `<tr>` elements.
        These have the lowest priority and can be overridden by specific row attributes
        (cf. `body_rows`, `head_rows`, `foot_rows`),
        or by the row attributes of the corresponding section
        (cf. `body_tr_attributes`, `head_tr_attributes`, `foot_tr_attributes`).
    attrs_th : ElementAttributesDictType, optional
        Attributes for all `<th>` elements.
        These have the lowest priority and can be overridden by specific cell attributes
        (cf. `body_rows`, `head_rows`, `foot_rows`),
        or by the row attributes of the corresponding section
        (cf. `body_th_attributes`, `head_th_attributes`, `foot_th_attributes`).
    attrs_td : ElementAttributesDictType, optional
        Attributes for all `<td>` elements.
        These have the lowest priority and can be overridden by specific cell attributes,
        (cf. `body_rows`, `head_rows`, `foot_rows`),
        or by the row attributes of the corresponding section
        (cf. `body_td_attributes`, `head_td_attributes`, `foot_td_attributes`).
    attrs_body_tr : ElementAttributesDictType, optional
        Attributes for all `<tr>` elements (i.e., rows) in the table body (cf. `body_rows`)
        These have the second lowest priority and can be overridden by specific row attributes,
        but not by `tr_attributes`.
    attrs_body_th : ElementAttributesDictType, optional
        Attributes for all `<th>` elements (i.e., cells) in the table body (cf. `body_rows`)
        These have the second lowest priority and can be overridden by specific cell attributes,
        but not by `th_attributes`.
    attrs_body_td : ElementAttributesDictType, optional
        Attributes for all `<td>` elements (i.e., cells) in the table body (cf. `body_rows`)
        These have the second lowest priority and can be overridden by specific cell attributes,
        but not by `td_attributes`.
    attrs_head_tr : ElementAttributesDictType, optional
        Like `body_tr_attributes`, but for the table head (cf. `head_rows`).
    attrs_head_th : ElementAttributesDictType, optional
        Like `body_th_attributes`, but for the table head (cf. `head_rows`).
    attrs_head_td : ElementAttributesDictType, optional
        Like `body_td_attributes`, but for the table head (cf. `head_rows`).
    attrs_foot_tr : ElementAttributesDictType, optional
        Like `body_tr_attributes`, but for the table foot (cf. `foot_rows`).
    attrs_foot_th : ElementAttributesDictType, optional
        Like `body_th_attributes`, but for the table foot (cf. `foot_rows`).
    attrs_foot_td : ElementAttributesDictType, optional
        Like `body_td_attributes`, but for the table foot (cf. `foot_rows`).

    Returns
    -------
    Table | Figure
        A `<table>` or `<figure>` element with the given rows.
    """
    args = locals()
    attrs_tr = attrs_tr or {}
    attrs_th = attrs_th or {}
    attrs_td = attrs_td or {}
    table_content = []
    for section in ("head", "body", "foot"):
        rows = args[f"rows_{section}"]
        if not rows:
            continue
        section_func = {"head": _el.thead, "body": _el.tbody, "foot": _el.tfoot}[section]
        section_attrs = args[f"attrs_{section}"] or {}
        section_tr_attrs = args[f"attrs_{section}_tr"] or {}
        section_th_attrs = args[f"attrs_{section}_th"] or {}
        section_td_attrs = args[f"attrs_{section}_td"] or {}
        section_content = []
        for row in rows:
            if isinstance(row, tuple):
                cells, row_attrs = row
            else:
                cells = row
                row_attrs = {}
            row_attrs = attrs_tr | section_tr_attrs | row_attrs
            row_content = []
            for cell_idx, cell in enumerate(cells):
                if isinstance(cell, (_el.TH, _el.TR)):
                    row_content.append(cell)
                    continue
                if isinstance(cell, tuple):
                    cell_content, cell_attrs = cell
                else:
                    cell_content = cell
                    cell_attrs = {}
                if section == "head" or (cell_idx < num_cols_stub):
                    cell_attrs = attrs_th | section_th_attrs | cell_attrs
                    cell_func = _el.th
                else:
                    cell_attrs = attrs_td | section_td_attrs | cell_attrs
                    cell_func = _el.td
                row_content.append(cell_func(cell_content, cell_attrs))
            section_content.append(_el.tr(row_content, row_attrs))
        table_content.append(section_func(section_content, section_attrs))
    if caption and not isinstance(caption, (_el.CAPTION, _el.FIGCAPTION)):
        attrs_caption = attrs_caption or {}
        caption_func_name = "figcaption" if as_figure else "caption"
        caption_func = getattr(_el, caption_func_name)
        caption = caption_func(caption, attrs_caption)
    if as_figure:
        fig_content = [caption] if caption else []
        fig_content.append(_el.table(table_content, attrs_table))
        return _el.figure(fig_content, attrs_figure)
    if caption:
        table_content.insert(0, caption)
    return _el.table(table_content, attrs_table)


def unordered_list(
    items: list[Stringable | tuple[Stringable, AttrsInputType]],
    type: Literal["disc", "circle", "square"] | None = None,
    attrs_li: AttrsInputType = None,
    attrs_ul: AttrsInputType = None,
) -> _el.UL:
    attrs_ul = attrs_ul or {}
    if type:
        attrs_ul["type"] = type
    return _el.ul(_create_list_items(items=items, attrs_li=attrs_li), attrs_ul)


def ordered_list(
    items: list[Stringable | tuple[Stringable, AttrsInputType]],
    type: Literal["1", "a", "A", "i", "I"] | None = None,
    start: int | None = None,
    reversed: bool = False,
    attrs_li: AttrsInputType = None,
    attrs_ol: AttrsInputType = None,
) -> _el.OL:
    attrs_ol = attrs_ol or {}
    if type:
        attrs_ol["type"] = type
    if start is not None:
        attrs_ol["start"] = start
    if reversed:
        attrs_ol["reversed"] = True
    return _el.ol(_create_list_items(items=items, attrs_li=attrs_li), attrs_ol)


def _create_list_items(
    items: list[Stringable | tuple[Stringable, AttrsInputType]],
    attrs_li: AttrsInputType = None,
) -> list[_el.LI]:
    li_elems = []
    attrs_li = attrs_li or {}
    for item in items:
        if isinstance(item, (tuple, list)):
            content, item_attrs = item
        else:
            content = item
            item_attrs = {}
        li_elems.append(_el.li(content, attrs_li | item_attrs))
    return li_elems


def text_style(
    text: str,
    word: str,
    strong: bool = False,
    bold: bool = False,
    italic: bool = False,
    emphasis: bool = False,
    underline: bool = False,
    url: str = "",
    count: int = 0,
    case_sensitive: bool = False
) -> str:
    """Apply various styles to a word in a text."""
    mod_word = word
    if strong:
        mod_word = f"<strong>{mod_word}</strong>"
    if bold:
        mod_word = f"<b>{mod_word}</b>"
    if italic:
        mod_word = f"<i>{mod_word}</i>"
    if emphasis:
        mod_word = f"<em>{mod_word}</em>"
    if underline:
        mod_word = f"<u>{mod_word}</u>"
    if url:
        mod_word = str(_el.a(mod_word, href=url))
    pattern = _re.compile(_re.escape(word), flags=0 if case_sensitive else _re.IGNORECASE)
    replaced_text = pattern.sub(mod_word, text, count=count)
    return replaced_text
