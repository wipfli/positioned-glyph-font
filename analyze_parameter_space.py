
def get_parameter_space(source):
    parameter_space_path = f'parameter_space/{source}-devanagari-parameter-space.csv'

    parameter_space = set()
    downsampled_parameter_space = set()
    downsampled_counts = dict()

    with open(parameter_space_path) as f:
        # skip csv header
        line = f.readline()
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            index, x_offset, y_offset, x_advance, y_advance, count = [int(num) for num in line.split(',')]
            
            parameter_space.add((index, x_offset, y_offset, x_advance, y_advance))
            
            downsampled_glyph = (
                index, 
                int(x_offset / 64), 
                int(y_offset / 64), 
                int(x_advance / 64), 
                int(y_advance / 64)
            )
            downsampled_parameter_space.add(downsampled_glyph)

            if downsampled_glyph in downsampled_counts:
                downsampled_counts[downsampled_glyph] += count
            else:
                downsampled_counts[downsampled_glyph] = count

    return parameter_space, downsampled_parameter_space, downsampled_counts

def write_downsampled(downsampled_counts, source):
    glyph_counts_sorted = dict(sorted(downsampled_counts.items(), key=lambda item: item[1]))

    downsampled_parameter_space_path = f'parameter_space/{source}-devanagari-downsampled-parameter-space.csv'

    print(f'writing {downsampled_parameter_space_path}...')
    with open(downsampled_parameter_space_path, 'w') as f:
        f.write(f'index,x_offset,y_offset,x_advance,y_advance,count\n')
        for item in glyph_counts_sorted.items():
            f.write(f'{item[0][0]},{item[0][1]},{item[0][2]},{item[0][3]},{item[0][4]},{item[1]}\n')

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
print('osm - wikidata', parameter_space_osm.difference(parameter_space_wikidata))

print('osm is subset of wikipedia', parameter_space_osm.issubset(parameter_space_wikipedia))
print('osm - wikipedia', parameter_space_osm.difference(parameter_space_wikipedia))

print('wikidata is subset of wikipedia', parameter_space_wikidata.issubset(parameter_space_wikipedia))
print('wikidata - wikipedia', parameter_space_wikidata.difference(parameter_space_wikipedia))

print()
print('downsampled...')

print('wikidata size', len(downsampled_parameter_space_wikidata))
print('osm size', len(downsampled_parameter_space_osm))
print('wikipedia size', len(downsampled_parameter_space_wikipedia))

print('osm is subset of wikidata', downsampled_parameter_space_osm.issubset(downsampled_parameter_space_wikidata))
print('osm - wikidata', downsampled_parameter_space_osm.difference(downsampled_parameter_space_wikidata))

print('osm is subset of wikipedia', downsampled_parameter_space_osm.issubset(downsampled_parameter_space_wikipedia))
print('osm - wikipedia', downsampled_parameter_space_osm.difference(downsampled_parameter_space_wikipedia))

print('wikidata is subset of wikipedia', downsampled_parameter_space_wikidata.issubset(downsampled_parameter_space_wikipedia))
print('wikidata - wikipedia', downsampled_parameter_space_wikidata.difference(downsampled_parameter_space_wikipedia))

