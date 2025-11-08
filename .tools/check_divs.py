from pathlib import Path
import re

p = Path(r'c:\Users\abush\OneDrive\Documents\W26\core\templates\core\home.html')
text = p.read_text(encoding='utf-8')
lines = text.splitlines()

open_re = re.compile(r'<div\b[^>]*>', re.IGNORECASE)
close_re = re.compile(r'</div>', re.IGNORECASE)

stack = []
unmatched_closing = []

for i, line in enumerate(lines, start=1):
    idx = 0
    while idx < len(line):
        o = open_re.search(line, idx)
        c = close_re.search(line, idx)
        if o and (not c or o.start() < c.start()):
            stack.append((i, o.group(0).strip()))
            idx = o.end()
        elif c:
            if stack:
                stack.pop()
            else:
                unmatched_closing.append((i, c.group(0)))
            idx = c.end()
        else:
            break

print('File:', p)
print('Total opening <div>:', sum(1 for _ in open_re.finditer(text)))
print('Total closing </div>:', sum(1 for _ in close_re.finditer(text)))
print()
if unmatched_closing:
    print('Unmatched closing </div> found at lines:')
    for ln, tag in unmatched_closing:
        print(f'  line {ln}: {tag}')
else:
    print('No unmatched closing </div> found.')

if stack:
    print('\nUnclosed opening <div> tags (still on stack):')
    for ln, tag in stack:
        print(f'  opened at line {ln}: {tag}')
else:
    print('\nNo unclosed opening <div> tags; all <div> are balanced.')
