from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import html as _py_html

import htmp

if _TYPE_CHECKING:
    from htmp.container import Container
    from htmp.protocol import AttrsType, ContentInputType


class Element:

    _IS_HTML_CODE = True

    def __init__(self, name: str, void: bool, attrs: AttrsType | None = None):
        self.name = name
        self.attrs = attrs or {}
        self.void = void
        return

    def tag(self, indent: int = 3, length_threshold: int = 80) -> str:
        """Get the HTML syntax of the element's opening tag."""
        attrs = []
        for key, val in sorted(self.attrs.items()):
            if not val:
                continue
            if isinstance(val, bool) and val:
                attrs.append(f"{key}")
            elif isinstance(val, (tuple, list)):
                attrs.append(f'{key}="{" ".join(_py_html.escape(str(v)) for v in val)}"')
            elif isinstance(val, dict):
                attrs.append(
                    f'{key}="{"; ".join(f"{_py_html.escape(str(k))}: {_py_html.escape(str(v))}" for k, v in val.items())}"'
                )
            else:
                attrs.append(f'{key}="{_py_html.escape(str(val))}"')
        tag_start = f"<{self.name}"
        tag_end = f"{' /' if self.void else ''}>"
        if not attrs:
            return f"{tag_start}{tag_end}"
        oneliner = f"{tag_start} {' '.join(attrs)}{tag_end}"
        if (
            indent < 0
            or length_threshold <= 0
            or len(oneliner) <= length_threshold
        ):
            return oneliner
        attrs_str = "\n".join([f"{indent * ' '}{attr}" for attr in attrs])
        return f"{tag_start}\n{attrs_str}{tag_end}"

    def display(self, ipython: bool = False, as_md: bool = False) -> None:
        """Display the element in an IPython notebook."""
        if ipython:
            return htmp.display.ipython(str(self), as_md=as_md)
        return htmp.display.browser(str(self))

    def __str__(self):
        """HTML syntax of the element as a one-line string."""
        return self.source(indent=-1)

    def source(self, indent: int = 3, tag_length_threshold: int = 80) -> str:
        """Get the HTML syntax of the element."""
        ...


class VoidElement(Element):

    def __init__(self, name: str, attrs: AttrsType | None = None):
        super().__init__(name=name, void=True, attrs=attrs)
        return

    def source(self, indent: int = 3, length_threshold: int = 80) -> str:
        return self.tag(indent=indent, length_threshold=length_threshold)

    def __repr__(self):
        class_open = f"{self.name.upper()}("
        if not self.attrs:
            return f"{class_open})"
        indent = 3 * " "
        lines = [class_open, f"{indent}attrs={{"]
        for key, val in self.attrs.items():
            lines.append(f'{2 * indent}"{key}": "{val}",')
        lines.append(f"{indent}}}")
        lines.append(")")
        return "\n".join(lines)


class ContentElement(Element):

    def __init__(self, name: str, content: Container, attrs: AttrsType | None = None):
        super().__init__(name=name, void=False, attrs=attrs)
        self.content = content
        return

    def source(self, indent: int = 3, length_threshold: int = 80) -> str:
        content = self.content.source(indent=indent)
        if indent < 0:
            sep = ""
        else:
            sep = "\n"
            if indent > 0:
                content = "\n".join([f"{indent * ' '}{line}" for line in content.split("\n")])
        start_tag = self.tag(indent=indent, length_threshold=length_threshold)
        end_tag = f"</{self.name}>"
        return f"{start_tag}{sep}{content}{sep}{end_tag}"

    def __repr__(self):
        indent = 3 * " "
        lines = [f"{self.name.upper()}("]
        if self.content:
            lines.append(f"{indent}content={{")
            for content_id, content in self.content.items():
                content_repr = repr(content).strip()
                content_repr_lines = content_repr.splitlines()
                for line in content_repr_lines[:-1]:
                    lines.append(f"{2 * indent}{line}")
                lines.append(f"{2 * indent}{content_repr_lines[-1]},")
            lines.append(f"{indent}}},")
        if self.attrs:
            lines.append(f"{indent}attrs={{")
            for key, val in self.attrs.items():
                lines.append(f'{2 * indent}"{key}": "{val}",')
            lines.append(f"{indent}}},")
        lines.append(")")
        return "\n".join(lines)


class A(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="a", content=content, attrs=attrs)
        return


class ABBR(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="abbr", content=content, attrs=attrs)
        return


class ACRONYM(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="acronym", content=content, attrs=attrs)
        return


class ADDRESS(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="address", content=content, attrs=attrs)
        return


class APPLET(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="applet", content=content, attrs=attrs)
        return


class AREA(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="area", attrs=attrs)
        return


class ARTICLE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="article", content=content, attrs=attrs)
        return


class ASIDE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="aside", content=content, attrs=attrs)
        return


class AUDIO(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="audio", content=content, attrs=attrs)
        return


class B(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="b", content=content, attrs=attrs)
        return


class BASE(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="base", attrs=attrs)
        return


class BASEFONT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="basefont", content=content, attrs=attrs)
        return


class BDI(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="bdi", content=content, attrs=attrs)
        return


class BDO(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="bdo", content=content, attrs=attrs)
        return


class BGSOUND(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="bgsound", content=content, attrs=attrs)
        return


class BIG(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="big", content=content, attrs=attrs)
        return


class BLINK(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="blink", content=content, attrs=attrs)
        return


class BLOCKQUOTE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="blockquote", content=content, attrs=attrs)
        return


class BODY(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="body", content=content, attrs=attrs)
        return


class BR(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="br", attrs=attrs)
        return


class BUTTON(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="button", content=content, attrs=attrs)
        return


class CANVAS(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="canvas", content=content, attrs=attrs)
        return


class CAPTION(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="caption", content=content, attrs=attrs)
        return


class CENTER(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="center", content=content, attrs=attrs)
        return


class CITE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="cite", content=content, attrs=attrs)
        return


class CODE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="code", content=content, attrs=attrs)
        return


class COL(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="col", attrs=attrs)
        return


class COLGROUP(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="colgroup", content=content, attrs=attrs)
        return


class CONTENT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="content", content=content, attrs=attrs)
        return


class DATA(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="data", content=content, attrs=attrs)
        return


class DATALIST(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="datalist", content=content, attrs=attrs)
        return


class DD(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="dd", content=content, attrs=attrs)
        return


class DEL(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="del", content=content, attrs=attrs)
        return


class DETAILS(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="details", content=content, attrs=attrs)
        return


class DFN(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="dfn", content=content, attrs=attrs)
        return


class DIALOG(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="dialog", content=content, attrs=attrs)
        return


class DIR(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="dir", content=content, attrs=attrs)
        return


class DIV(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="div", content=content, attrs=attrs)
        return


class DL(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="dl", content=content, attrs=attrs)
        return


class DT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="dt", content=content, attrs=attrs)
        return


class EM(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="em", content=content, attrs=attrs)
        return


class EMBED(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="embed", attrs=attrs)
        return


class FIELDSET(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="fieldset", content=content, attrs=attrs)
        return


class FIGCAPTION(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="figcaption", content=content, attrs=attrs)
        return


class FIGURE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="figure", content=content, attrs=attrs)
        return


class FONT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="font", content=content, attrs=attrs)
        return


class FOOTER(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="footer", content=content, attrs=attrs)
        return


class FORM(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="form", content=content, attrs=attrs)
        return


class FRAME(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="frame", content=content, attrs=attrs)
        return


class FRAMESET(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="frameset", content=content, attrs=attrs)
        return


class H1(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="h1", content=content, attrs=attrs)
        return


class H2(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="h2", content=content, attrs=attrs)
        return


class H3(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="h3", content=content, attrs=attrs)
        return


class H4(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="h4", content=content, attrs=attrs)
        return


class H5(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="h5", content=content, attrs=attrs)
        return


class H6(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="h6", content=content, attrs=attrs)
        return


class HEAD(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="head", content=content, attrs=attrs)
        return


class HEADER(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="header", content=content, attrs=attrs)
        return


class HGROUP(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="hgroup", content=content, attrs=attrs)
        return


class HR(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="hr", attrs=attrs)
        return


class HTML(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="html", content=content, attrs=attrs)
        return


class I(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="i", content=content, attrs=attrs)
        return


class IFRAME(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="iframe", content=content, attrs=attrs)
        return


class IMAGE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="image", content=content, attrs=attrs)
        return


class IMG(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="img", attrs=attrs)
        return


class INPUT(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="input", attrs=attrs)
        return


class INS(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="ins", content=content, attrs=attrs)
        return


class ISINDEX(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="isindex", content=content, attrs=attrs)
        return


class KBD(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="kbd", content=content, attrs=attrs)
        return


class KEYGEN(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="keygen", attrs=attrs)
        return


class LABEL(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="label", content=content, attrs=attrs)
        return


class LEGEND(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="legend", content=content, attrs=attrs)
        return


class LI(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="li", content=content, attrs=attrs)
        return


class LINK(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="link", attrs=attrs)
        return


class LISTING(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="listing", content=content, attrs=attrs)
        return


class MAIN(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="main", content=content, attrs=attrs)
        return


class MAP(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="map", content=content, attrs=attrs)
        return


class MARK(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="mark", content=content, attrs=attrs)
        return


class MARQUEE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="marquee", content=content, attrs=attrs)
        return


class MATH(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="math", content=content, attrs=attrs)
        return


class MENU(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="menu", content=content, attrs=attrs)
        return


class MENUITEM(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="menuitem", content=content, attrs=attrs)
        return


class META(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="meta", attrs=attrs)
        return


class METER(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="meter", content=content, attrs=attrs)
        return


class MULTICOL(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="multicol", content=content, attrs=attrs)
        return


class NAV(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="nav", content=content, attrs=attrs)
        return


class NEXTID(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="nextid", content=content, attrs=attrs)
        return


class NOBR(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="nobr", content=content, attrs=attrs)
        return


class NOEMBED(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="noembed", content=content, attrs=attrs)
        return


class NOFRAMES(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="noframes", content=content, attrs=attrs)
        return


class NOSCRIPT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="noscript", content=content, attrs=attrs)
        return


class OBJECT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="object", content=content, attrs=attrs)
        return


class OL(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="ol", content=content, attrs=attrs)
        return


class OPTGROUP(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="optgroup", content=content, attrs=attrs)
        return


class OPTION(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="option", content=content, attrs=attrs)
        return


class OUTPUT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="output", content=content, attrs=attrs)
        return


class P(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="p", content=content, attrs=attrs)
        return


class PARAM(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="param", attrs=attrs)
        return


class PICTURE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="picture", content=content, attrs=attrs)
        return


class PLAINTEXT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="plaintext", content=content, attrs=attrs)
        return


class PORTAL(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="portal", content=content, attrs=attrs)
        return


class PRE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="pre", content=content, attrs=attrs)
        return


class PROGRESS(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="progress", content=content, attrs=attrs)
        return


class Q(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="q", content=content, attrs=attrs)
        return


class RB(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="rb", content=content, attrs=attrs)
        return


class RP(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="rp", content=content, attrs=attrs)
        return


class RT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="rt", content=content, attrs=attrs)
        return


class RTC(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="rtc", content=content, attrs=attrs)
        return


class RUBY(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="ruby", content=content, attrs=attrs)
        return


class S(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="s", content=content, attrs=attrs)
        return


class SAMP(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="samp", content=content, attrs=attrs)
        return


class SCRIPT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="script", content=content, attrs=attrs)
        return


class SEARCH(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="search", content=content, attrs=attrs)
        return


class SECTION(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="section", content=content, attrs=attrs)
        return


class SELECT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="select", content=content, attrs=attrs)
        return


class SHADOW(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="shadow", content=content, attrs=attrs)
        return


class SLOT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="slot", content=content, attrs=attrs)
        return


class SMALL(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="small", content=content, attrs=attrs)
        return


class SOURCE(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="source", attrs=attrs)
        return


class SPACER(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="spacer", content=content, attrs=attrs)
        return


class SPAN(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="span", content=content, attrs=attrs)
        return


class STRIKE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="strike", content=content, attrs=attrs)
        return


class STRONG(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="strong", content=content, attrs=attrs)
        return


class STYLE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="style", content=content, attrs=attrs)
        return


class SUB(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="sub", content=content, attrs=attrs)
        return


class SUMMARY(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="summary", content=content, attrs=attrs)
        return


class SUP(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="sup", content=content, attrs=attrs)
        return


class SVG(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="svg", content=content, attrs=attrs)
        return


class TABLE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="table", content=content, attrs=attrs)
        return


class TBODY(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="tbody", content=content, attrs=attrs)
        return


class TD(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="td", content=content, attrs=attrs)
        return


class TEMPLATE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="template", content=content, attrs=attrs)
        return


class TEXTAREA(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="textarea", content=content, attrs=attrs)
        return


class TFOOT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="tfoot", content=content, attrs=attrs)
        return


class TH(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="th", content=content, attrs=attrs)
        return


class THEAD(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="thead", content=content, attrs=attrs)
        return


class TIME(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="time", content=content, attrs=attrs)
        return


class TITLE(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="title", content=content, attrs=attrs)
        return


class TR(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="tr", content=content, attrs=attrs)
        return


class TRACK(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="track", attrs=attrs)
        return


class TT(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="tt", content=content, attrs=attrs)
        return


class U(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="u", content=content, attrs=attrs)
        return


class UL(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="ul", content=content, attrs=attrs)
        return


class VAR(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="var", content=content, attrs=attrs)
        return


class VIDEO(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="video", content=content, attrs=attrs)
        return


class WBR(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="wbr", attrs=attrs)
        return


class XMP(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="xmp", content=content, attrs=attrs)
        return


def a(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> A:
    return A(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def abbr(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> ABBR:
    return ABBR(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def acronym(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> ACRONYM:
    return ACRONYM(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def address(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> ADDRESS:
    return ADDRESS(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def applet(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> APPLET:
    return APPLET(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def area(attrs: AttrsType | None = None, /, **keyword_attrs) -> AREA:
    return AREA((attrs or {}) | keyword_attrs)


def article(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> ARTICLE:
    return ARTICLE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def aside(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> ASIDE:
    return ASIDE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def audio(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> AUDIO:
    return AUDIO(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def b(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> B:
    return B(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def base(attrs: AttrsType | None = None, /, **keyword_attrs) -> BASE:
    return BASE((attrs or {}) | keyword_attrs)


def basefont(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> BASEFONT:
    return BASEFONT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def bdi(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> BDI:
    return BDI(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def bdo(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> BDO:
    return BDO(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def bgsound(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> BGSOUND:
    return BGSOUND(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def big(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> BIG:
    return BIG(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def blink(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> BLINK:
    return BLINK(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def blockquote(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> BLOCKQUOTE:
    return BLOCKQUOTE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def body(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> BODY:
    return BODY(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def br(attrs: AttrsType | None = None, /, **keyword_attrs) -> BR:
    return BR((attrs or {}) | keyword_attrs)


def button(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> BUTTON:
    return BUTTON(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def canvas(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> CANVAS:
    return CANVAS(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def caption(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> CAPTION:
    return CAPTION(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def center(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> CENTER:
    return CENTER(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def cite(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> CITE:
    return CITE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def code(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> CODE:
    return CODE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def col(attrs: AttrsType | None = None, /, **keyword_attrs) -> COL:
    return COL((attrs or {}) | keyword_attrs)


def colgroup(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> COLGROUP:
    return COLGROUP(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def content(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> CONTENT:
    return CONTENT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def data(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> DATA:
    return DATA(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def datalist(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> DATALIST:
    return DATALIST(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def dd(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> DD:
    return DD(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def del_(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> DEL:
    return DEL(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def details(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> DETAILS:
    return DETAILS(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def dfn(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> DFN:
    return DFN(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def dialog(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> DIALOG:
    return DIALOG(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def dir(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> DIR:
    return DIR(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def div(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> DIV:
    return DIV(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def dl(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> DL:
    return DL(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def dt(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> DT:
    return DT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def em(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> EM:
    return EM(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def embed(attrs: AttrsType | None = None, /, **keyword_attrs) -> EMBED:
    return EMBED((attrs or {}) | keyword_attrs)


def fieldset(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> FIELDSET:
    return FIELDSET(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def figcaption(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> FIGCAPTION:
    return FIGCAPTION(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def figure(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> FIGURE:
    return FIGURE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def font(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> FONT:
    return FONT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def footer(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> FOOTER:
    return FOOTER(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def form(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> FORM:
    return FORM(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def frame(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> FRAME:
    return FRAME(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def frameset(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> FRAMESET:
    return FRAMESET(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def h1(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> H1:
    return H1(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def h2(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> H2:
    return H2(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def h3(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> H3:
    return H3(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def h4(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> H4:
    return H4(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def h5(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> H5:
    return H5(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def h6(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> H6:
    return H6(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def head(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> HEAD:
    return HEAD(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def header(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> HEADER:
    return HEADER(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def hgroup(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> HGROUP:
    return HGROUP(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def hr(attrs: AttrsType | None = None, /, **keyword_attrs) -> HR:
    return HR((attrs or {}) | keyword_attrs)


def html(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> HTML:
    return HTML(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def i(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> I:
    return I(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def iframe(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> IFRAME:
    return IFRAME(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def image(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> IMAGE:
    return IMAGE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def img(attrs: AttrsType | None = None, /, **keyword_attrs) -> IMG:
    return IMG((attrs or {}) | keyword_attrs)


def input(attrs: AttrsType | None = None, /, **keyword_attrs) -> INPUT:
    return INPUT((attrs or {}) | keyword_attrs)


def ins(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> INS:
    return INS(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def isindex(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> ISINDEX:
    return ISINDEX(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def kbd(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> KBD:
    return KBD(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def keygen(attrs: AttrsType | None = None, /, **keyword_attrs) -> KEYGEN:
    return KEYGEN((attrs or {}) | keyword_attrs)


def label(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> LABEL:
    return LABEL(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def legend(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> LEGEND:
    return LEGEND(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def li(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> LI:
    return LI(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def link(attrs: AttrsType | None = None, /, **keyword_attrs) -> LINK:
    return LINK((attrs or {}) | keyword_attrs)


def listing(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> LISTING:
    return LISTING(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def main(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> MAIN:
    return MAIN(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def map(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> MAP:
    return MAP(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def mark(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> MARK:
    return MARK(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def marquee(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> MARQUEE:
    return MARQUEE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def math(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> MATH:
    return MATH(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def menu(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> MENU:
    return MENU(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def menuitem(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> MENUITEM:
    return MENUITEM(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def meta(attrs: AttrsType | None = None, /, **keyword_attrs) -> META:
    return META((attrs or {}) | keyword_attrs)


def meter(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> METER:
    return METER(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def multicol(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> MULTICOL:
    return MULTICOL(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def nav(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> NAV:
    return NAV(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def nextid(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> NEXTID:
    return NEXTID(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def nobr(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> NOBR:
    return NOBR(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def noembed(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> NOEMBED:
    return NOEMBED(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def noframes(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> NOFRAMES:
    return NOFRAMES(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def noscript(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> NOSCRIPT:
    return NOSCRIPT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def object(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> OBJECT:
    return OBJECT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def ol(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> OL:
    return OL(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def optgroup(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> OPTGROUP:
    return OPTGROUP(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def option(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> OPTION:
    return OPTION(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def output(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> OUTPUT:
    return OUTPUT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def p(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> P:
    return P(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def param(attrs: AttrsType | None = None, /, **keyword_attrs) -> PARAM:
    return PARAM((attrs or {}) | keyword_attrs)


def picture(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> PICTURE:
    return PICTURE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def plaintext(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> PLAINTEXT:
    return PLAINTEXT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def portal(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> PORTAL:
    return PORTAL(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def pre(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> PRE:
    return PRE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def progress(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> PROGRESS:
    return PROGRESS(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def q(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> Q:
    return Q(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def rb(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> RB:
    return RB(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def rp(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> RP:
    return RP(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def rt(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> RT:
    return RT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def rtc(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> RTC:
    return RTC(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def ruby(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> RUBY:
    return RUBY(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def s(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> S:
    return S(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def samp(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SAMP:
    return SAMP(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def script(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SCRIPT:
    return SCRIPT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def search(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SEARCH:
    return SEARCH(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def section(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SECTION:
    return SECTION(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def select(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SELECT:
    return SELECT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def shadow(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SHADOW:
    return SHADOW(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def slot(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SLOT:
    return SLOT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def small(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SMALL:
    return SMALL(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def source(attrs: AttrsType | None = None, /, **keyword_attrs) -> SOURCE:
    return SOURCE((attrs or {}) | keyword_attrs)


def spacer(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SPACER:
    return SPACER(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def span(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SPAN:
    return SPAN(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def strike(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> STRIKE:
    return STRIKE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def strong(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> STRONG:
    return STRONG(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def style(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> STYLE:
    return STYLE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def sub(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SUB:
    return SUB(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def summary(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SUMMARY:
    return SUMMARY(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def sup(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SUP:
    return SUP(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def svg(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> SVG:
    return SVG(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def table(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> TABLE:
    return TABLE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def tbody(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> TBODY:
    return TBODY(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def td(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> TD:
    return TD(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def template(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> TEMPLATE:
    return TEMPLATE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def textarea(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> TEXTAREA:
    return TEXTAREA(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def tfoot(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> TFOOT:
    return TFOOT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def th(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> TH:
    return TH(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def thead(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> THEAD:
    return THEAD(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def time(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> TIME:
    return TIME(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def title(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> TITLE:
    return TITLE(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def tr(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> TR:
    return TR(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def track(attrs: AttrsType | None = None, /, **keyword_attrs) -> TRACK:
    return TRACK((attrs or {}) | keyword_attrs)


def tt(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> TT:
    return TT(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def u(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> U:
    return U(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def ul(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> UL:
    return UL(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def var(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> VAR:
    return VAR(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def video(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> VIDEO:
    return VIDEO(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)


def wbr(attrs: AttrsType | None = None, /, **keyword_attrs) -> WBR:
    return WBR((attrs or {}) | keyword_attrs)


def xmp(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> XMP:
    return XMP(content=htmp.container_from_object(content), attrs=(attrs or {}) | keyword_attrs)
