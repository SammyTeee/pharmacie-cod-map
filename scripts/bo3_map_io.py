"""Read every iwmap entity, including older generated entities without comments."""


def parse_map_entities(text):
    found = []
    depth = 0
    quoted = False
    comment = False
    start = None
    i = 0
    while i < len(text):
        c = text[i]
        if comment:
            if c == '\n':
                comment = False
        elif c == '"':
            quoted = not quoted
        elif not quoted:
            if c == '/' and text[i:i+2] == '//':
                comment = True
                i += 1
            elif c == '{':
                if depth == 0:
                    start = i
                depth += 1
            elif c == '}':
                depth -= 1
                if depth < 0:
                    raise ValueError('Unexpected map closing brace')
                if depth == 0:
                    found.append((start, i+1, text[start:i+1]))
        i += 1
    if depth or quoted:
        raise ValueError('Unterminated map entity/string')
    return found
