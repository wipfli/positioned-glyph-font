import ctypes


def shape(font_path, text):

    lib = ctypes.CDLL('./run_raqm.so')
    lib.runRaqm.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
    lib.runRaqm.restype = None

    fontfile = font_path.encode('utf-8')
    text = text.encode('utf-8')
    direction = b"ltr"
    language = b"en"

    buffer_size = 2 ** 12
    buffer = ctypes.create_string_buffer(buffer_size)

    lib.runRaqm(fontfile, text, direction, language, buffer, buffer_size)
    output = buffer.value.decode('utf-8')

    if output == '\n':
        return None
    glyphs = [parse_raqm_output(line) for line in output.splitlines()]
    if 0 in [glyph["index"] for glyph in glyphs]:
        return None
    return glyphs


def parse_raqm_output(line):
    try:
        index, x_offset, y_offset, x_advance, y_advance, cluster = [int(num) for num in line.split()]
    except ValueError as e:
        print('ValueError:', format(e), 'line:', line, 'defaulting to zeros...')
        index, x_offset, y_offset, x_advance, y_advance, cluster = [0 for _ in range(6)]
    return {
        "index": index,
        "x_offset": x_offset,
        "y_offset": y_offset,
        "x_advance": x_advance,
        "y_advance": y_advance,
        "cluster": cluster,
    }
