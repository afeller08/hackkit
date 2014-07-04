foobar = {}


def foo(template):
    lastlast = None
    last = None
    i = 0
    out = []
    while i < len(template):
        char = template[i]
        if char == '`':
            if lastlast != '\\' and last != '\\':
                (segment, i) = foobar[last](template, i)
            lastlast = None
            out += segment
            last = None
        else:
            i += 1
            out.append(char)
            lastlast = last
            last = char
    return ''.join(out)
