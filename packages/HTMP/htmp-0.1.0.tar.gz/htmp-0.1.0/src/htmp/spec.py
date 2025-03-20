def element_is_void(element_name: str) -> bool:
    """Whether a given HTML element is a
    [void element](https://developer.mozilla.org/en-US/docs/Glossary/Void_element).

    Parameters
    ----------
    element_name : str
        Name of the element (case-insensitive).
    """
    return element_name.lower() in (
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "keygen", "link", "meta", "param", "source", "track", "wbr",
    )