import re

with open("input.txt", "r") as file:
    source_code = file.read()

keywords = {'int', 'main', 'begin', 'do', 'while', 'return', 'end'}

token_specification = [
    ('KEYWORD', r'\b(int|main|begin|do|while|return|end)\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
    ('NUMBER', r'\d+'),
    ('OPERATOR', r'=|\+'),
    ('SYMBOL', r'\(|\)|;'),
    ('SKIP', r'[ \t\n]+'),
    ('MISMATCH', r'.'),
]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

tokens = []

for mo in re.finditer(tok_regex, source_code):
    kind = mo.lastgroup
    value = mo.group()

    if kind == 'SKIP':
        continue
    elif kind == 'MISMATCH':
        print("Error:", value)
    else:
        tokens.append((kind, value))

# Print tokens
print("\nTOKENS:")
for t in tokens:
    print(t)

# 🔥 Save to file
with open("token_output.txt", "w") as f:
    f.write("TOKEN TABLE:\n")
    for t in tokens:
        f.write(str(t) + "\n")

print("\nToken output saved to token_output.txt")