import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\legacy\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "refreshStandardView" in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print the next 40 lines
        for j in range(idx+1, min(len(lines), idx+41)):
            print(f"  Line {j+1}: {lines[j].rstrip()}")
