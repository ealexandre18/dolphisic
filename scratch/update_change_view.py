import os

html_paths = [
    r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\legacy\index.html",
    r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\index.html"
]

target_str = """        window.changeLegacyView = function(viewId) {
          if (viewId === 'dashboard') {"""

replacement_str = """        window.changeLegacyView = function(viewId) {
          if (activeView === viewId) return;
          if (viewId === 'dashboard') {"""

for path in html_paths:
    print("Modifying:", path)
    if not os.path.exists(path):
        print("  File not found!")
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if target_str in content:
        new_content = content.replace(target_str, replacement_str)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("  Successfully updated changeLegacyView with activeView check!")
    else:
        print("  Target not found (might already be updated or format differs)!")
