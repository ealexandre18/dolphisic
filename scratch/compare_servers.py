import difflib

with open("server.py", "r", encoding="utf-8") as f:
    main_server = f.readlines()

with open("v2-design-pro/server.py", "r", encoding="utf-8") as f:
    v2_server = f.readlines()

diff = difflib.unified_diff(v2_server, main_server, fromfile="v2-design-pro/server.py", tofile="server.py")
print("".join(list(diff)[:100]))
