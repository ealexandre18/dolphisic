with open("dist/assets/index-DyRupmtp.js", "r", encoding="utf-8") as f:
    js_content = f.read()

query = "container:"
# We want to find container style in the styles object F, which was around index 252801.
# Let's search backwards or starting from 250000.
idx = js_content.find(query, 250000)
print("Index of 'container:':", idx)
if idx != -1:
    print(repr(js_content[idx-50:idx+250]))
else:
    print("Not found")














