with open('c:/Users/Ewan Alexandre/Desktop/PROJET SDIS/dist/assets/index-DyRupmtp.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

pos = 691785
start = max(0, pos - 100)
end = min(len(content), pos + 1200)
snippet = content[start:end]

print("--- JS surrounding position 691785 ---")
print(snippet)
