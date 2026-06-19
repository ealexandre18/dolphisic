with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js.bak", "r", encoding="utf-8") as f:
    content = f.read()

def find_exact(name, start_pat, end_pat):
    start_idx = content.find(start_pat)
    if start_idx == -1:
        print(f"Could not find start for {name}")
        return
    
    # Find the matching end anchor after start
    end_idx = content.find(end_pat, start_idx)
    if end_idx == -1:
        print(f"Could not find end for {name}")
        return
    
    exact_str = content[start_idx:end_idx + len(end_pat)]
    print(f"Exact {name} (len={len(exact_str)}):")
    print(repr(exact_str))
    print("-" * 30)

# Body 2
find_exact("Body 2", "[...u.filter(e=>e.date_maj_cle&&e.date_maj_cle.trim()!==``)].sort", ",e.id))})")

# Body 3
find_exact("Body 3", "u.filter(e=>!e.date_maj_cle||e.date_maj_cle.trim()===``).map", ",e.id))})")

# Body 4
find_exact("Body 4", "o.map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`600`},children:e.cis||`N/A`})", ",e.id))})")
