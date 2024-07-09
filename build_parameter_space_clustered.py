import json
#from pprint import pprint
from shape import shape

def build_parameter_space(source):
    font_path = 'font-maker/fonts/NotoSansDevanagari-Regular.ttf'

    corpus_path = f'corpus/{source}-devanagari-corpus.txt'
    parameter_space_path = f'parameter_space/{source}-devanagari-parameter-space-clustered.jsonl'

    def glyph_dict_to_tuple(glyph):
        return (
            glyph["index"],
            glyph["x_offset"],
            glyph["y_offset"],
            glyph["x_advance"],
            glyph["y_advance"],
        )

    glyph_cluster_counts = {}

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

            glyph_vector_clusters = {}
            for glyph in glyph_vector:
                cluster_id = glyph['cluster']
                if cluster_id not in glyph_vector_clusters:
                    glyph_vector_clusters[cluster_id] = []
                glyph_vector_clusters[cluster_id].append(glyph_dict_to_tuple(glyph))

            for glyph_cluster in glyph_vector_clusters.values():
                glyph_cluster_tuple = tuple(glyph_cluster)
                if glyph_cluster_tuple in glyph_cluster_counts:
                    glyph_cluster_counts[glyph_cluster_tuple] += 1
                else:
                    glyph_cluster_counts[glyph_cluster_tuple] = 1

    glyph_cluster_counts_sorted = dict(sorted(glyph_cluster_counts.items(), key=lambda item: item[1]))

    print(f'writing {parameter_space_path}...')
    with open(parameter_space_path, 'w') as f:
        for glyph_cluster_tuple, count in glyph_cluster_counts_sorted.items():
            glyph_cluster = [ { 'index': g[0], 'x_offset': g[1], 'y_offset': g[2], 'x_advance': g[3], 'y_advance': g[4] } for g in glyph_cluster_tuple ] 
            item = { 'count': count, 'cluster': glyph_cluster }
            f.write(json.dumps(item))
            f.write('\n')

build_parameter_space(source='osm')
build_parameter_space(source='wikipedia')
build_parameter_space(source='wikidata')
