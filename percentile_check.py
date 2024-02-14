import json

fname = 'parameter_space/wikipedia-devanagari-downsampled-parameter-space-clustered.jsonl'

entries = []
total_count = 0
with open(fname, 'r') as f:
    for line in f:
        e = json.loads(line.strip())
        total_count += e['count']
        entries.append(e)

print(f'{total_count=}')
current_count = 0
cumulative = []
for e in reversed(entries):
    count = e['count']
    current_count += count
    cumulative.append(current_count/total_count)

for pval in [0.99, 0.999, 0.9999]:
    for i,c in enumerate(cumulative):
        if c >= pval:
            print(f'Entries within {pval*100} percentile: {i+1}')
            break


