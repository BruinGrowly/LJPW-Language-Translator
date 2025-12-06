from striprtf.striprtf import rtf_to_text
from pathlib import Path

rtf_file = Path('experiments/nwt_E.rtf/nwt_41_Mr_E.rtf')
with open(rtf_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

text = rtf_to_text(content)

with open('debug_mark_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Dumped {len(text)} chars to debug_mark_text.txt")
