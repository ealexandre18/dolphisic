import difflib

with open(r"server.py", "r", encoding="utf-8") as f:
    main_server = f.readlines()

with open(r"dolphisic_redesign/backend/server.py", "r", encoding="utf-8") as f:
    redesign_server = f.readlines()

diff = difflib.unified_diff(main_server, redesign_server, fromfile="server.py", tofile="dolphisic_redesign/backend/server.py")
diff_lines = list(diff)
print(f"Diff lines count: {len(diff_lines)}")
print("".join(diff_lines[:150]))
