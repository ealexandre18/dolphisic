import os

file_paths = [
    r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\legacy\assets\index-DyRupmtp.js",
    r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js"
]

target = "[i,a]=(0,_.useState)(`standard`)"
replacement = "[i,a]=(0,_.useState)(`standard`),_unused=(window.setLegacyPage=a)"

for path in file_paths:
    print("Modifying:", path)
    if not os.path.exists(path):
        print("  File not found!")
        continue
    
    # Create a backup
    backup_path = path + ".orig.bak"
    if not os.path.exists(backup_path):
        os.rename(path, backup_path)
        print("  Created backup:", backup_path)
        read_path = backup_path
    else:
        print("  Backup already exists. Reading from backup to avoid duplicate replacements.")
        read_path = backup_path

    with open(read_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if target in content:
        new_content = content.replace(target, replacement)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("  Successfully replaced target string!")
    else:
        print("  Target NOT found in source!")
