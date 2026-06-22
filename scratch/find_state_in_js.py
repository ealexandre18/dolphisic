import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\assets\index-DyRupmtp.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

targets = [
    "[n,r]=(0,_.useState)(``)",
    "[c,l]=(0,_.useState)(`BIP`)",
    "Le=async()=>{h(!0);try{let e=await fetch(`/api/centres`),n=await e.json();e.ok&&(t(n),n.length>0&&r(n[0]))}",
    "Le=async()=>{h(!0);try{let e=await fetch(`/api/centres`),n=await e.json();e.ok&&(t(n),n.length>0&&r(",
    "Le=async()=>{"
]

for t in targets:
    pos = content.find(t)
    if pos != -1:
        print(f"FOUND: '{t}' at {pos}")
        print("  Context:", content[pos-50:pos+150])
    else:
        print(f"NOT FOUND: '{t}'")
