import json
import os

log_file = r"C:\Users\Ewan Alexandre\.gemini\antigravity-ide\brain\9262fca8-60c6-4bd3-8c3c-edeaf408d03c\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_file):
    print("Log file found. Searching for 'v2-design-pro' or 'inject_css'...")
    with open(log_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if "v2-design-pro" in line or "inject_css" in line:
                try:
                    obj = json.loads(line)
                    print(f"Line {i} - Type: {obj.get('type')}, Status: {obj.get('status')}")
                    # Print snippet of tool_calls or content
                    content = str(obj.get('content', ''))
                    if len(content) > 200:
                        content = content[:200] + "..."
                    print(f"  Content: {content}")
                    tool_calls = obj.get('tool_calls', [])
                    if tool_calls:
                        print(f"  Tool Calls: {tool_calls[0].get('toolName')} -> {str(tool_calls[0].get('args'))[:150]}")
                except Exception as e:
                    print(f"Error parsing line {i}: {e}")
else:
    print("Log file not found.")
