import os
from glob import glob

for filepath in glob('templates/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.replace('<html lang="en">', '<html lang="{{ session.get(\'lang\', \'en\') }}">')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
