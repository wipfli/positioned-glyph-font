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
        'to_encode': ord(letter) < 2**16 and not ignore_codepoints[ord(letter)]
    }
    for letter in text[1:]:
        to_encode = ord(letter) < 2**16 and not ignore_codepoints[ord(letter)]
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
        print(f'ERROR: Could not find font for Unicode codepoint U+{hex(ord(letter))[2:].upper().zfill(4)} ({letter}).')
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


def get_glyphs_of_text(text, ignore_codepoints, unicode_to_font_path):
    to_encode_parts = split_to_encode(text, ignore_codepoints)
    all_glyphs = set([])
    all_glyphs_downscaled = set([])
    ignore_text = True
    for to_encode_part in to_encode_parts:
        if to_encode_part['to_encode']:
            ignore_text = False
            font_parts = split_font_parts(to_encode_part['text'], unicode_to_font_path)
            for font_part in font_parts:
                glyphs = get_glyphs(font_part['font'], font_part['text'])
                for glyph in glyphs:
                    item = (
                        font_part['font'], 
                        glyph['index'], 
                        int(glyph['x_offset']), 
                        int(glyph['y_offset']),
                        int(glyph['x_advance']),
                    )
                    all_glyphs.add(item)
                    item_downscaled = (
                        font_part['font'], 
                        glyph['index'], 
                        int(glyph['x_offset'] / 64), 
                        int(glyph['y_offset'] / 64),
                        int(glyph['x_advance'] / 64),
                    )
                    all_glyphs_downscaled.add(item_downscaled)
    return all_glyphs, all_glyphs_downscaled, ignore_text
    

def get_glyphs_of_labels(labels, ignore_codepoints, unicode_to_font_path):

    i = 0
    num_ignored_labels = 0
    all_glyphs = set([])
    all_glyphs_downscaled = set([])
    labels_requiring_encoding = []
    for label in labels:
        i += 1
        if i % 100000 == 0:
            print(i, 'harfbuzz glyphs', len(all_glyphs), 'maplibre downscaled sdf glyphs', len(all_glyphs_downscaled), 'num ignored labels', num_ignored_labels)
        glyphs, glyphs_downscaled, ignore_text = get_glyphs_of_text(label, ignore_codepoints, unicode_to_font_path)
        for glyph in glyphs:
            all_glyphs.add(glyph)
        for glyph_downscaled in glyphs_downscaled:
            all_glyphs_downscaled.add(glyph_downscaled)
        if ignore_text:
            num_ignored_labels += 1
        else:
            labels_requiring_encoding.append(label)
    print('num labels', len(labels), 'num ignored labels', num_ignored_labels)
    return all_glyphs, all_glyphs_downscaled, labels_requiring_encoding


fonts_directory = '../fonts/'

with open('ignore_codepoints.json') as f:
    ignore_codepoints = json.load(f)
    ignore_codepoints = {int(key): ignore_codepoints[key] for key in ignore_codepoints}

unicode_to_font_path = build_unicode_to_font_path(fonts_directory)

with open('labels.json') as f:
    labels = json.load(f)

all_glyphs, all_glyphs_downscaled, labels_requiring_encoding = get_glyphs_of_labels(labels, ignore_codepoints, unicode_to_font_path)

print(len(all_glyphs), len(all_glyphs_downscaled))

with open('all_glyphs.json', 'w') as f:
    json.dump(list(all_glyphs), f, indent=2)

with open('all_glyphs_downscaled.json', 'w') as f:
    json.dump(list(all_glyphs_downscaled), f, indent=2)

with open('labels_requiring_encoding.json', 'w') as f:
    json.dump(labels_requiring_encoding, f, indent=2)
