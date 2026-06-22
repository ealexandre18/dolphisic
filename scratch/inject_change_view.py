import os

html_paths = [
    r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\legacy\index.html",
    r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\index.html"
]

target_str = "const observer = new MutationObserver(installEnhancements);"

injection = """        window.changeLegacyView = function(viewId) {
          if (viewId === 'dashboard') {
            openExtension('dashboard');
          } else if (viewId === 'settings') {
            openExtension('settings');
          } else {
            closeExtension();
            if (typeof window.setLegacyPage === 'function') {
              window.setLegacyPage(viewId);
            }
          }
        };

        const observer = new MutationObserver(installEnhancements);"""

for path in html_paths:
    print("Modifying:", path)
    if not os.path.exists(path):
        print("  File not found!")
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if target_str in content:
        if "window.changeLegacyView" in content:
            print("  Already injected!")
            continue
        new_content = content.replace(target_str, injection)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("  Successfully injected changeLegacyView!")
    else:
        print("  Target observer script not found!")
