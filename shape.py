import subprocess
import json

def shape(font_path, text):
    command = f'hb-shape --no-glyph-names --output-format=json {font_path} {text}'
    result = json.loads(subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout.decode())
    glyphs = []
    for item in result:
        glyphs.append({
            'index': item['g'],
            'x_offset': item['dx'],
            'y_offset': item['dy'],
            'x_advance': item['ax'],
            'y_advance': item['ay'],
            'cluster': item['cl'],
        })
    return glyphs
