import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\legacy\assets\index-DyRupmtp.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find("let p=[{id:`standard`")
if pos != -1:
    # search backwards from pos for a React.useState call or similar
    search_area = content[max(0, pos-1000):pos]
    print("--- Search area before list ---")
    print(search_area)
else:
    print("Not found")
