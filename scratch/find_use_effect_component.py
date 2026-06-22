import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\assets\index-DyRupmtp.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find("Le=async()=>{")
if pos != -1:
    print("Found Le. Let's look at the surrounding function definition:")
    # Find the beginning of the component enclosing Le.
    # In Javascript, this is often "function name(" or "const name = ("
    # Let's search backwards for the nearest "function "
    search_back = content[max(0, pos-4000):pos]
    print(search_back)
else:
    print("Not found")
