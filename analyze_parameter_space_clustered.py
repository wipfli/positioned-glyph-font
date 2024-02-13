import json
import copy

def get_parameter_space(source):
    parameter_space_path = f'parameter_space/{source}-devanagari-parameter-space-clustered.jsonl'

    parameter_space = set()
    downsampled_parameter_space = set()
    downsampled_counts = dict()

    def downsample(g):
        ng = copy.copy(g)
        ng['x_offset']  = int(g['x_offset']/64)
        ng['y_offset']  = int(g['y_offset']/64)
        ng['x_advance'] = int(g['x_advance']/64)
        ng['y_advance'] = int(g['y_advance']/64)

    with open(parameter_space_path) as f:
        for line in f:
            if line.strip() == '':
                continue
            item = json.loads(line.strip())
            count = item['count']
            cluster = item['cluster']
            cluster_tuple = tuple([ (g['index'], g['x_offset'], g['y_offset'], g['x_advance'], g['y_advance']) for g in cluster ])
            
            parameter_space.add(cluster_tuple)
            
            downsampled_cluster = tuple([ (g['index'], int(g['x_offset']/64), int(g['y_offset']/64), int(g['x_advance']/64), int(g['y_advance']/64)) for g in cluster ])
            downsampled_parameter_space.add(downsampled_cluster)

            if downsampled_cluster in downsampled_counts:
                downsampled_counts[downsampled_cluster] += count
            else:
                downsampled_counts[downsampled_cluster] = count

    return parameter_space, downsampled_parameter_space, downsampled_counts

def write_downsampled(downsampled_counts, source):
    glyph_counts_sorted = dict(sorted(downsampled_counts.items(), key=lambda item: item[1]))

    downsampled_parameter_space_path = f'parameter_space/{source}-devanagari-downsampled-parameter-space-clustered.jsonl'

    print(f'writing {downsampled_parameter_space_path}...')
    with open(downsampled_parameter_space_path, 'w') as f:
        for glyph_cluster_tuple, count in glyph_counts_sorted.items():
            glyph_cluster = [ { 'index': g[0], 'x_offset': g[1], 'y_offset': g[2], 'x_advance': g[3], 'y_advance': g[4] } for g in glyph_cluster_tuple ] 
            item = { 'count': count, 'cluster': glyph_cluster }
            f.write(json.dumps(item))
            f.write('\n')

parameter_space_osm, downsampled_parameter_space_osm, downsampled_counts_osm = get_parameter_space(source='osm')
parameter_space_wikipedia, downsampled_parameter_space_wikipedia, downsampled_counts_wikipedia = get_parameter_space(source='wikipedia')
parameter_space_wikidata, downsampled_parameter_space_wikidata, downsampled_counts_wikidata = get_parameter_space(source='wikidata')

write_downsampled(downsampled_counts=downsampled_counts_osm, source='osm')
write_downsampled(downsampled_counts=downsampled_counts_wikipedia, source='wikipedia')
write_downsampled(downsampled_counts=downsampled_counts_wikidata, source='wikidata')

print()
print('original...')

print('wikidata size', len(parameter_space_wikidata))
print('osm size', len(parameter_space_osm))
print('wikipedia size', len(parameter_space_wikipedia))

print('osm is subset of wikidata', parameter_space_osm.issubset(parameter_space_wikidata))
print('len(osm - wikidata)', len(parameter_space_osm.difference(parameter_space_wikidata)))

print('osm is subset of wikipedia', parameter_space_osm.issubset(parameter_space_wikipedia))
print('len(osm - wikipedia)', len(parameter_space_osm.difference(parameter_space_wikipedia)))

print('wikidata is subset of wikipedia', parameter_space_wikidata.issubset(parameter_space_wikipedia))
print('len(wikidata - wikipedia)', len(parameter_space_wikidata.difference(parameter_space_wikipedia)))

print()
print('downsampled...')

print('wikidata size', len(downsampled_parameter_space_wikidata))
print('osm size', len(downsampled_parameter_space_osm))
print('wikipedia size', len(downsampled_parameter_space_wikipedia))

print('osm is subset of wikidata', downsampled_parameter_space_osm.issubset(downsampled_parameter_space_wikidata))
print('len(osm - wikidata)', len(downsampled_parameter_space_osm.difference(downsampled_parameter_space_wikidata)))

print('osm is subset of wikipedia', downsampled_parameter_space_osm.issubset(downsampled_parameter_space_wikipedia))
print('len(osm - wikipedia)', len(downsampled_parameter_space_osm.difference(downsampled_parameter_space_wikipedia)))

print('wikidata is subset of wikipedia', downsampled_parameter_space_wikidata.issubset(downsampled_parameter_space_wikipedia))
print('len(wikidata - wikipedia)', len(downsampled_parameter_space_wikidata.difference(downsampled_parameter_space_wikipedia)))

