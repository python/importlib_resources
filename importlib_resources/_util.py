from io import TextIOWrapper


def _wrap_file(resource, encoding, errors):
    if encoding is None:
        return resource
    return TextIOWrapper(resource, encoding=encoding, errors=errors)
