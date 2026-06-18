with open("dist/assets/index-DyRupmtp.js", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find('option`,{value:`Point Haut`')
print("Index:", idx)
if idx != -1:
    print(content[idx-500:idx+500])
