#!/usr/bin/env python3
import re

with open('comprehensive_manuscript_editor.py', 'r') as f:
    content = f.read()

# Fix the specific indentation issues - normalize all excessive indentation to 8 spaces
lines = content.split('\n')
fixed_lines = []

for line in lines:
    # If line starts with excessive whitespace (more than 12 spaces), normalize to 8
    if re.match(r'^[ ]{12,}', line):
        # Count leading spaces
        leading_spaces = len(line) - len(line.lstrip())
        if leading_spaces > 12:
            # Normalize to 8 spaces for method content
            line = '        ' + line.lstrip()
    fixed_lines.append(line)

with open('comprehensive_manuscript_editor.py', 'w') as f:
    f.write('\n'.join(fixed_lines))

print('Fixed indentation issues') 