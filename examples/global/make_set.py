import json

labels = set([])
i = 0
with open('labels.txt') as f:
    for line in f:
        labels.add(line.strip())
        i += 1
        if i % 1000000 == 0:
            print(i, len(labels))

print(i, len(labels))

with open('labels.json', 'w') as f:
    json.dump(list(labels), f, indent=2)
