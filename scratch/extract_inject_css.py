import json
import os

log_file = r"C:\Users\Ewan Alexandre\.gemini\antigravity-ide\brain\9262fca8-60c6-4bd3-8c3c-edeaf408d03c\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if '"type":"VIEW_FILE"' in line and "inject_css.py" in line:
                try:
                    obj = json.loads(line)
                    print(f"--- Found inject_css.py on line {i} ---")
                    # Extract file content
                    content = obj.get('content', '')
                    print(content)
                except Exception as e:
                    print("Error:", e)
else:
    print("Log not found")
