def drop_false(element):
    """Drop False values from a list or tuple or dict."""
    if type(element) in (list, tuple):
        return type(element)(drop_false(e) for e in element if e)

    for key, value in element.items():
        if value is False:
            element[key] = str("")
    return element
