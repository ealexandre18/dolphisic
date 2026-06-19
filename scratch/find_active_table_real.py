with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js.bak", "r", encoding="utf-8") as f:
    content = f.read()

idx_active_table = 239844
with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\scratch\active_table_real.txt", "w", encoding="utf-8") as f:
    f.write(content[idx_active_table-1000:idx_active_table+1500])

print("Dumped real active table context to scratch/active_table_real.txt")
