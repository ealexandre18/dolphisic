with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js", "r", encoding="utf-8") as f:
    content = f.read()

m = 252788
start = max(0, m - 1800)
end = min(len(content), m + 1200)
print(content[start:end])
