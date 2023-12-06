import json

ignore_codepoints = {}

for i in range(2 ** 16):
    ignore_codepoints[i] = True

    # Main blocks for Indic scripts and Sinhala
    if 0x0900 <= i <= 0x0DFF:
        ignore_codepoints[i] = False

    # Main blocks for Tibetan and Myanmar
    if 0x0F00 <= i <= 0x109F:
        ignore_codepoints[i] = False
    
    # Khmer
    if 0x1780 <= i <= 0x17FF:
        ignore_codepoints[i] = False

with open('ignore_codepoints.json', 'w') as f:
    json.dump(ignore_codepoints, f, indent=2)
