import os

html_paths = [
    r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\legacy\index.html",
    r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\index.html"
]

for path in html_paths:
    print("Inspecting:", path)
    if not os.path.exists(path):
        print("  File not found!")
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    pos = content.find("window.changeLegacyView")
    if pos != -1:
        print(content[pos:pos+400])
    else:
        print("  Not found!")
