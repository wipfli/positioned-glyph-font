import json


ignored_unicode_ranges = {
    'low codepoints': {'first_including': 0x0000, 'last_including': 0x06FF},
    'Arabic Supplement': {'first_including': 0x0750, 'last_including': 0x077F},
    'Arabic Extended-A': {'first_including': 0x08A0, 'last_including': 0x08FF},
    'Hangul Jamo': {'first_including': 0x1100, 'last_including': 0x11FF},
    'Box Drawing': {'first_including': 0x2500, 'last_including': 0x257F},
    'Block Elements': {'first_including': 0x2580, 'last_including': 0x259F},
    'Dingbats': {'first_including': 0x2700, 'last_including': 0x27BF},
    'CJK Radicals Supplement': {'first_including': 0x2E80, 'last_including': 0x2EFF},
    'Kangxi Radicals': {'first_including': 0x2F00, 'last_including': 0x2FDF},
    'Ideographic Description Characters': {'first_including': 0x2FF0, 'last_including': 0x2FFF},
    'CJK Symbols and Punctuation': {'first_including': 0x3000, 'last_including': 0x303F},
    'Hiragana': {'first_including': 0x3040, 'last_including': 0x309F},
    'Katakana': {'first_including': 0x30A0, 'last_including': 0x30FF},
    'Bopomofo': {'first_including': 0x3100, 'last_including': 0x312F},
    'Hangul Compatibility Jamo': {'first_including': 0x3130, 'last_including': 0x318F},
    'Kanbun': {'first_including': 0x3190, 'last_including': 0x319F},
    'Bopomofo Extended': {'first_including': 0x31A0, 'last_including': 0x31BF},
    'CJK Strokes': {'first_including': 0x31C0, 'last_including': 0x31EF},
    'Katakana Phonetic Extensions': {'first_including': 0x31F0, 'last_including': 0x31FF},
    'Enclosed CJK Letters and Months': {'first_including': 0x3200, 'last_including': 0x32FF},
    'CJK Compatibility': {'first_including': 0x3300, 'last_including': 0x33FF},
    'CJK Unified Ideographs Extension A': {'first_including': 0x3400, 'last_including': 0x4DBF},
    'Yijing Hexagram Symbols': {'first_including': 0x4DC0, 'last_including': 0x4DFF},
    'CJK Unified Ideographs': {'first_including': 0x4E00, 'last_including': 0x9FFF},
    'Yi Syllables': {'first_including': 0xA000, 'last_including': 0xA48F},
    'Yi Radicals': {'first_including': 0xA490, 'last_including': 0xA4CF},
    'Hangul Jamo Extended-A': {'first_including': 0xA960, 'last_including': 0xA97F},
    'Hangul Syllables': {'first_including': 0xAC00, 'last_including': 0xD7AF},
    'Hangul Jamo Extended-B': {'first_including': 0xD7B0, 'last_including': 0xD7FF},
    'Private Use Area': {'first_including': 0xE000, 'last_including': 0xF8FF},
    'CJK Compatibility Ideographs': {'first_including': 0xF900, 'last_including': 0xFAFF},
    'Alphabetic Presentation Forms': {'first_including': 0xFB00, 'last_including': 0xFB4F},
    'Arabic Presentation Forms-A': {'first_including': 0xFB50, 'last_including': 0xFDFF},
    'Variation Selectors': {'first_including': 0xFE00, 'last_including': 0xFE0F},
    'Vertical Forms': {'first_including': 0xFE10, 'last_including': 0xFE1F},
    'Small Form Variants': {'first_including': 0xFE50, 'last_including': 0xFE6F},
    'CJK Compatibility Forms': {'first_including': 0xFE30, 'last_including': 0xFE4F},
    'Arabic Presentation Forms-B': {'first_including': 0xFE70, 'last_including': 0xFEFF},
    'Halfwidth and Fullwidth Forms': {'first_including': 0xFF00, 'last_including': 0xFFEF},
}

for r in ignored_unicode_ranges:
    print(r, ignored_unicode_ranges[r]['last_including'] - ignored_unicode_ranges[r]['first_including'] - 1)

ignore_codepoints = {}

num_ignored_codepoints = 0
for i in range(2 ** 16):
    ignore_codepoints[i] = False

    for r in ignored_unicode_ranges:
        if ignored_unicode_ranges[r]['first_including'] <= i <= ignored_unicode_ranges[r]['last_including']:
            ignore_codepoints[i] = True
            num_ignored_codepoints += 1

print('ignored codepoints', num_ignored_codepoints, 'available codepoints', 2**16 - num_ignored_codepoints)

with open('ignore_codepoints.json', 'w') as f:
    json.dump(ignore_codepoints, f, indent=2)
