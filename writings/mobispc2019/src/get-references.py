import sys
import re

for line in sys.stdin.readlines():
    line = line.strip()
    m = re.search(r'@.*{\s*(\S+)\s*,', line)
    if m:
        ref = m.group(1)
        print("\cite{%s}" % ref)
