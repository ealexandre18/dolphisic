import os

file_paths = [
    r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\legacy\assets\index-DyRupmtp.js",
    r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js"
]

target = "[i,a]=(0,_.useState)(`standard`)"

for path in file_paths:
    print("Checking:", path)
    if not os.path.exists(path):
        print("  File not found!")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    pos = content.find(target)
    if pos != -1:
        print(f"  FOUND target at position {pos}!")
        print("  Context:", content[pos-50:pos+100])
    else:
        print("  Target NOT found!")
