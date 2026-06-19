import subprocess

with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js", "r", encoding="utf-8") as f:
    content = f.read()

# Let's locate the modified tbody segments in the generated file
# 1. BIP tbody
idx_bip = content.find("u.map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`}")
idx_bip_end = content.find(",e.id))})", idx_bip) + 9 if idx_bip != -1 else -1

# 2. Active tbody
idx_active = content.find("[...u.filter(e=>e.date_maj_cle")
idx_active_end = content.find(",e.id))})", idx_active) + 9 if idx_active != -1 else -1

# 3. Pending tbody
idx_pending = content.find("u.filter(e=>!e.date_maj_cle")
idx_pending_end = content.find(",e.id))})", idx_pending) + 9 if idx_pending != -1 else -1

# 4. All tbody
idx_all = content.find("o.map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`600`}")
idx_all_end = content.find(",e.id))})", idx_all) + 9 if idx_all != -1 else -1

def test_syntax(label, code):
    if not code:
        print(f"Skipping {label} (not found)")
        return
    # Wrap it
    mock_header = "const u = [], o = [], P = {jsx: (t, p) => {}, jsxs: (t, p, k) => {}}, F = {actionsCell: {}, actionBtn: {}}, I = {actionsCell: {}, actionBtn: {}}, Ve = () => {}, He = () => {}, Se = () => {}, w = () => {}, S = () => {}, Ne = {}, me = {}, re = {}, ne = {}, Ye = () => 1, Xe = () => {}, I_func = () => ''; "
    clean_code = code.strip()
    if clean_code.endswith("})"):
        clean_code = clean_code[:-2]
    full_code = mock_header + "const test = (0,P.jsx)('tbody', { children: " + clean_code + " });"
    res = subprocess.run(["node", "--eval", full_code], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"SYNTAX ERROR in {label}:")
        print(res.stderr)
    else:
        print(f"{label} syntax is OK!")

if idx_bip != -1:
    test_syntax("BIP Tbody", content[idx_bip:idx_bip_end])
else:
    print("BIP Tbody not found in generated file!")

if idx_active != -1:
    test_syntax("Active Tbody", content[idx_active:idx_active_end])
else:
    print("Active Tbody not found in generated file!")

if idx_pending != -1:
    test_syntax("Pending Tbody", content[idx_pending:idx_pending_end])
else:
    print("Pending Tbody not found in generated file!")

if idx_all != -1:
    test_syntax("All Tbody", content[idx_all:idx_all_end])
else:
    print("All Tbody not found in generated file!")
