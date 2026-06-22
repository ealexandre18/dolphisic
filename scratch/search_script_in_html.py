import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\legacy\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "<script" in line or "type=\"module\"" in line or "assets/" in line:
        print(f"Line {idx+1}: {line.strip()}")
