from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

import htmp
import htmp.element as _el

if _TYPE_CHECKING:
    from htmp.container import Container
    from htmp.protocol import AttrsInputType


class Document:
    """HTML Document."""

    def __init__(
        self,
        content_head: Container,
        content_body: Container,
        attrs_head: AttrsInputType = None,
        attrs_body: AttrsInputType = None,
        attrs_html: AttrsInputType = None,
        doctype: str = "html",
    ):
        self.content_head = content_head
        self.content_body = content_body
        self.attrs_body = attrs_body or {}
        self.attrs_head = attrs_head or {}
        self.attrs_html = attrs_html or {}
        self.doctype = doctype
        return

    def source(self, indent: int = 3) -> str:
        sep = "" if indent < 0 else "\n"
        return sep.join([f"<!DOCTYPE {self.doctype}>", self.html.source(indent=indent)])

    @property
    def html(self) -> _el.HTML:
        return _el.html([part for part in [self.head, self.body] if part], self.attrs_html)

    @property
    def head(self) -> _el.HEAD | None:
        if self.content_head or self.attrs_head:
            return _el.head(self.content_head, self.attrs_head)
        return

    @property
    def body(self) -> _el.BODY | None:
        if self.content_body or self.attrs_body:
            return _el.body(self.content_body, self.attrs_body)
        return

    def __str__(self):
        return self.source(indent=-1)

    def add_highlight_js(
        self,
        version: str = "11.10.0",
        style: str = "default",
        languages: list[str] = None,
        key_stylesheet: str = "highlight_js_stylesheet",
        key_scripts: str = "highlight_js_scripts",
    ) -> None:
        """Use [highlight.js](https://highlightjs.org/) to highlight code blocks.

        This automatically adds the necessary CSS stylesheets and JavaScript scripts to the document.
        The stylesheet is added to the `<head>` element under the key `highlight_js_stylesheet`,
        and the scripts are added to the `<body>` element under the keys `highlight_js_script_languages`,
        `highlight_js_script_{language}` (for additional languages) and `highlight_js_script_load`.

        Parameters
        ----------
        version: string, default: "11.10.0"
            The version of highlight.js to use.

            See the [highlight.js GitHub repository](https://github.com/highlightjs/highlight.js)
            for available versions.
        style: string, default: "default"
            Name of the highlight.js stylesheet to use.

            This should be the filename (without the '.min.css' extension)
            of one of the available stylesheets in the specified version
            at [cdnjs](https://cdnjs.com/libraries/highlight.js).
            The full URL is constructed using `version` and `style` as follows:
            `https://cdnjs.cloudflare.com/ajax/libs/highlight.js/{version}/styles/{style}.min.css`
        languages: list of strings, optional
            List of additional languages to load.

            These should be the filenames (without the '.min.js' extension)
            of the language scripts in the specified version
            at [cdnjs](https://cdnjs.com/libraries/highlight.js).
            The full URL is constructed using `version` and the language name as follows:
            `https://cdnjs.cloudflare.com/ajax/libs/highlight.js/{version}/languages/{language}.min.js`

        Notes
        -----
        - highlight.js tries to automatically detect the language of each `<pre><code>` element.
          However, you can also specifically define the language of each element by adding a
          class named `language-{NAME}` to the `<code>` element,
          where `NAME` is an alias of one of the
          [supported languages by highlight.js](https://github.com/highlightjs/highlight.js/blob/main/SUPPORTED_LANGUAGES.md).
          For example, to set the language of a code block to HTML:
          `<pre><code class="language-html">...</code></pre>`

        References
        ----------
        - [highlight.js Website](https://highlightjs.org/)
        - [highlight.js Documentation](https://highlightjs.readthedocs.io/en/stable/index.html)
        - [highlight.js cdnjs Repository](https://cdnjs.com/libraries/highlight.js)
        """
        base_url = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js"
        style_href = f"{base_url}/{version}/styles/{style}.min.css"
        self.content_head[key_stylesheet] = _el.link(rel="stylesheet", href=style_href)

        scripts = [
            _el.script(src=f"{base_url}/{version}/highlight.min.js")
        ]
        for language in languages or []:
            scripts.append(_el.script(src=f"{base_url}/{version}/languages/{language}.min.js"))
        scripts.append(_el.script("hljs.highlightAll();"))
        self.content_body[key_scripts] = htmp.container_from_object(scripts)
        return
