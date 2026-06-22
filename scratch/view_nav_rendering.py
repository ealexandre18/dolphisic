import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\legacy\assets\index-DyRupmtp.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find("let p=[{id:`standard`")
if pos != -1:
    print(content[pos:pos+2500])
else:
    print("Not found")
