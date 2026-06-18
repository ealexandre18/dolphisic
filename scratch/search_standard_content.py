import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js", "r", encoding="utf-8") as f:
    content = f.read()

m = content.find("Configuration des Alertes & Notifications")
if m != -1:
    print(content[m+5500:m+9500])
else:
    print("Not found")
