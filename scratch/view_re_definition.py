import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\assets\index-DyRupmtp.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find("Ve=async e=>{")
if pos != -1:
    print("Found Ve context:")
    print(content[pos-1000:pos+300])
else:
    print("Not found")
