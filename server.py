
from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse
import urllib.parse

from shape import shape

def read_encoding_csv():
    encoding = {}
    with open('encoding.csv') as f:
        # skip csv header
        line = f.readline()
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            index, x_offset, y_offset, x_advance, y_advance, codepoint = [int(num) for num in line.split(',')]
            glyph_tuple = (index, x_offset, y_offset, x_advance, y_advance)
            encoding[glyph_tuple] = codepoint
    return encoding

app = FastAPI()

font_path = 'font-maker/fonts/NotoSansDevanagari-Regular.ttf'
encoding = read_encoding_csv()

@app.get("/{text}", response_class=HTMLResponse)
async def root(text: str):
    encoded_request = urllib.parse.quote(text)
    print('requested', text, encoded_request)
    
    glyph_vector = shape(font_path, text)
    result = ''
    if not glyph_vector:
        return result
    
    for glyph in glyph_vector:
        glyph_tuple = (
            glyph['index'], 
            int(glyph['x_offset'] / 64), 
            int(glyph['y_offset'] / 64), 
            int(glyph['x_advance'] / 64), 
            int(glyph['y_advance'] / 64)
        )
        codepoint = encoding[glyph_tuple]
        result += chr(codepoint)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
