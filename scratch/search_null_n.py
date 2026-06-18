with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js", "r", encoding="utf-8") as f:
    content = f.read()

m = 228060
start = m + 1000
end = m + 3500
print(content[start:end])
