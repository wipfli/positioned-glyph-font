from glob import glob

from itertools import chain

from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

import json
import ctypes

lib = ctypes.CDLL('./run_raqm.so')

lib.runRaqm.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
lib.runRaqm.restype = None

def get_glyphs(font_path, text):
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
    glyphs = [line_to_glyph(line) for line in output.splitlines()]
    if 0 in [glyph["index"] for glyph in glyphs]:
        return None
    return glyphs


def line_to_glyph(line):
    index, x_offset, y_offset, x_advance, y_advance, cluster = [int(num) for num in line.split()]
    return {
        "index": index,
        "x_offset": x_offset,
        "y_offset": y_offset,
        "x_advance": x_advance,
        "y_advance": y_advance,
        "cluster": cluster,
    }

def build_unicode_to_font_path(fonts_directory):
    result = {
        # unicode codepoint decimal number: list of font path strings
    }

    font_paths = []
    font_paths.extend(glob(f"{fonts_directory}/*", recursive=True))

    for font_path in font_paths:
        print('reading', font_path)
        with TTFont(
            font_path, 0, allowVID=0, ignoreDecompileErrors=True, fontNumber=-1
        ) as ttf:
            chars = chain.from_iterable(
                [y + (Unicode[y[0]],) for y in x.cmap.items()] for x in ttf["cmap"].tables
            )
            for c in chars:
                if c[0] in result:
                    if font_path not in result[c[0]]:
                        result[c[0]].append(font_path)
                else:
                    result[c[0]] = [font_path]

    return result
    
def split_to_encode(text, ignore_codepoints):
    parts = [] # [{'text': 'B', 'to_encode': True}, {'text': 'asel', 'to_encode': False}, ...]
    if len(text) == 0:
        return parts
    
    letter = text[0]
    part = {
        'text': letter,
        'to_encode': not ignore_codepoints[ord(letter)]
    }
    for letter in text[1:]:
        to_encode = not ignore_codepoints[ord(letter)]
        if to_encode != part['to_encode']:
            parts.append(part)
            part = {
                'text': letter,
                'to_encode': to_encode
            }
        else:
            part['text'] += letter
    parts.append(part)
    return parts

def get_first_font(letter, unicode_to_font_path):
    if ord(letter) not in unicode_to_font_path:
        print(f'ERROR: Could not find font for Unicode codepoint {ord(letter)} ({letter}) in text {text}.')
        exit()
    return unicode_to_font_path[ord(letter)][0]
    
def split_font_parts(text, unicode_to_font_path):
    parts = []
    
    if len(text) == 0:
        return parts
    
    letter = text[0]

    part = {
        'text': letter,
        'font': get_first_font(letter, unicode_to_font_path)
    }
    for letter in text[1:]:
        font = get_first_font(letter, unicode_to_font_path)
        if font != part['font']:
            parts.append(part)
            part = {
                'text': letter,
                'font': font
            }
        else:
            part['text'] += letter
    parts.append(part)
    return parts


def shape_label(text, ignore_codepoints, unicode_to_font_path):
    to_encode_parts = split_to_encode(text, ignore_codepoints)
    parts = []
    for to_encode_part in to_encode_parts:
        if to_encode_part['to_encode']:
            font_parts = split_font_parts(to_encode_part['text'], unicode_to_font_path)
            for font_part in font_parts:
                glyphs = get_glyphs(font_part['font'], font_part['text'])
                part = {
                    'to_encode': to_encode_part['to_encode'],
                    'glyphs': glyphs,
                    'font': font_part['font']
                }
                parts.append(part)
        else:
            part = {
                'to_encode': to_encode_part['to_encode'],
                'text': to_encode_part['text']
            }
            parts.append(part)
    return parts
    

def shape_labels(labels, ignore_codepoints, unicode_to_font_path):
    shaped_labels = []

    for label in labels:
        label_parts = shape_label(label, ignore_codepoints, unicode_to_font_path)
        shaped_labels.append({
            'text': label,
            'label_parts': label_parts
        })
    return shaped_labels

def get_next_available_codepoint(current_codepoint, ignore_codepoints):
    i = current_codepoint + 1

    while i < 2 ** 16 and ignore_codepoints[i]:
        i += 1
    
    if i == 2 ** 16:
        print('Error: Did not find any free codepoint.')
        exit()
    
    return i

def get_glyph_tuple(font, glyph):
    return (
        font,
        glyph['index'],
        glyph['x_offset'],
        glyph['y_offset'],
        glyph['x_advance'],
        glyph['y_advance']
    )

def generate_encoding(shaped_labels, ignore_codepoints):
    unique_glyphs = set([])

    for shaped_label in shaped_labels:
        for label_part in shaped_label['label_parts']:
            if label_part['to_encode']:
                for glyph in label_part['glyphs']:
                    glyph_tuple = get_glyph_tuple(label_part['font'], glyph)
                    unique_glyphs.add(glyph_tuple)

    unique_glyphs = list(unique_glyphs)

    glyph_to_unicode_encoding = {}
    codepoint = -1
    for glyph in unique_glyphs:
        codepoint = get_next_available_codepoint(codepoint, ignore_codepoints)
        glyph_to_unicode_encoding[glyph] = codepoint

    return glyph_to_unicode_encoding

def encode_labels(shaped_labels, glyph_to_unicode_encoding):
    encoded_labels = []
    for shaped_label in shaped_labels:
        encoded_label = ''
        for label_part in shaped_label['label_parts']:
            if label_part['to_encode']:
                for glyph in label_part['glyphs']:
                    glyph_tuple = get_glyph_tuple(label_part['font'], glyph)
                    encoded_label += chr(glyph_to_unicode_encoding[glyph_tuple])
            else:
                encoded_label += label_part['text']
        encoded_labels.append(encoded_label)
    return encoded_labels


fonts_directory = '../fonts/'

with open('ignore_codepoints.json') as f:
    ignore_codepoints = json.load(f)
    ignore_codepoints = {int(key): ignore_codepoints[key] for key in ignore_codepoints}


unicode_to_font_path = build_unicode_to_font_path(fonts_directory)

with open('labels.json') as f:
    labels = json.load(f)

shaped_labels = shape_labels(labels, ignore_codepoints, unicode_to_font_path)

# print(json.dumps(shaped_labels, indent=2))

glyph_to_unicode_encoding = generate_encoding(shaped_labels, ignore_codepoints)

# print(glyph_to_unicode_encoding)

encoded_labels = encode_labels(shaped_labels, glyph_to_unicode_encoding)

print(encoded_labels)

with open('encoded_labels.json', 'w') as f:
    json.dump(encoded_labels, f, indent=2)

def create_encoding_hpp(glyph_to_unicode_encoding):
    unicode_to_glyph_encoding = {}
    for key in glyph_to_unicode_encoding:
        unicode_to_glyph_encoding[glyph_to_unicode_encoding[key]] = key
    
    str_font = 'std::map<int, std::string> encoding_unicode_to_font = {\n'
    str_index = 'std::map<int, int> encoding_unicode_to_index = {\n'
    str_x_offset = 'std::map<int, int> encoding_unicode_to_x_offset = {\n'
    str_y_offset =  'std::map<int, int> encoding_unicode_to_y_offset = {\n'
    str_x_advance = 'std::map<int, int> encoding_unicode_to_x_advance = {\n'

    for codepoint in unicode_to_glyph_encoding:
        font, index, x_offset, y_offset, x_advance, y_advance = unicode_to_glyph_encoding[codepoint]
        font = font[3:]
        str_font += f'    {{{codepoint}, "{font}"}},\n'
        str_index += f'    {{{codepoint}, {index}}},\n'
        str_x_offset += f'    {{{codepoint}, {x_offset}}},\n'
        str_y_offset += f'    {{{codepoint}, {y_offset}}},\n'
        str_x_advance += f'    {{{codepoint}, {x_advance}}},\n'
    str_font += "};\n"
    str_index += "};\n"
    str_x_offset += "};\n"
    str_y_offset += "};\n"
    str_x_advance += "};\n"
    
    encoding_hpp = '#include <map>\n#include <string>\n'
    encoding_hpp += '\n'
    encoding_hpp += str_font
    encoding_hpp += '\n'
    encoding_hpp += str_index
    encoding_hpp += '\n'
    encoding_hpp += str_x_offset
    encoding_hpp += '\n'
    encoding_hpp += str_y_offset
    encoding_hpp += '\n'
    encoding_hpp += str_x_advance

    return encoding_hpp

encoding_hpp = create_encoding_hpp(glyph_to_unicode_encoding)
with open('../encoding.hpp', 'w') as f:
    f.write(encoding_hpp)