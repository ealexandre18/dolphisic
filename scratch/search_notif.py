with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js", "r", encoding="utf-8") as f:
    content = f.read()

m = 229482
start = max(0, m - 3000)
end = min(len(content), m)
print(content[start:end])
