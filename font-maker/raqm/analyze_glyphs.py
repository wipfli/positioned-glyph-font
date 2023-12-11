import json

with open('all_glyphs_downscaled.json') as f:
    glyphs = json.load(f)

font_count = {}
unique_glyph_indexes = {}

for glyph in glyphs:
    font = glyph[0]
    if font in font_count:
        font_count[font] += 1
    else:
        font_count[font] = 1

    index = glyph[1]
    if font in unique_glyph_indexes:
        unique_glyph_indexes[font].add(index)
    else:
        unique_glyph_indexes[font] = set([index])

font_count = dict(sorted(font_count.items(), key=lambda item: -item[1]))

sum_glyphs = 0
sum_glyph_indexes = 0
for font in font_count:
    sum_glyphs += font_count[font]
    sum_glyph_indexes += len(unique_glyph_indexes[font])
    print('|', font[9:], ' | ', font_count[font], ' | ', len(unique_glyph_indexes[font]), '|', '{:.2f}'.format(font_count[font] / len(unique_glyph_indexes[font])), '|') 

print('| Total | ', sum_glyphs, ' | ', sum_glyph_indexes, '|', '{:.2f}'.format(sum_glyphs / sum_glyph_indexes) ,'|') 
