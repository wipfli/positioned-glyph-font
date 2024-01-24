from shape import shape

def build_parameter_space(source):
    font_path = 'font-maker/fonts/NotoSansDevanagari-Regular.ttf'

    corpus_path = f'corpus/{source}-devanagari-corpus.txt'
    parameter_space_path = f'parameter_space/{source}-devanagari-parameter-space.csv'

    def glyph_dict_to_tuple(glyph):
        return (
            glyph["index"],
            glyph["x_offset"],
            glyph["y_offset"],
            glyph["x_advance"],
            glyph["y_advance"],
        )

    glyph_counts = {}

    print(f'reading {corpus_path}...')
    with open(corpus_path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            glyph_vector = shape(font_path, line)
            if not glyph_vector:
                continue
            for glyph in glyph_vector:
                glyph_tuple = glyph_dict_to_tuple(glyph)
                if glyph_tuple in glyph_counts:
                    glyph_counts[glyph_tuple] += 1
                else:
                    glyph_counts[glyph_tuple] = 1

    glyph_counts_sorted = dict(sorted(glyph_counts.items(), key=lambda item: item[1]))

    print(f'writing {parameter_space_path}...')
    with open(parameter_space_path, 'w') as f:
        f.write(f'index,x_offset,y_offset,x_advance,y_advance,count\n')
        for item in glyph_counts_sorted.items():
            f.write(f'{item[0][0]},{item[0][1]},{item[0][2]},{item[0][3]},{item[0][4]},{item[1]}\n')

build_parameter_space(source='osm')
build_parameter_space(source='wikipedia')
build_parameter_space(source='wikidata')
