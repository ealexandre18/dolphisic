import os
import filecmp

def compare_dirs(dir1, dir2):
    print(f"Comparing {dir1} and {dir2}...")
    for root, dirs, files in os.walk(dir1):
        # exclude certain directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'v2-design-pro', '.agents', 'scratch', '__pycache__', 'node_modules', '.stfolder']]
        for file in files:
            file1 = os.path.join(root, file)
            rel_path = os.path.relpath(file1, dir1)
            file2 = os.path.join(dir2, rel_path)
            if not os.path.exists(file2):
                print(f"Only in {dir1}: {rel_path}")
            else:
                if not filecmp.cmp(file1, file2, shallow=False):
                    print(f"Different content: {rel_path}")
    
    # also check files only in dir2
    for root, dirs, files in os.walk(dir2):
        dirs[:] = [d for d in dirs if d not in ['.git', 'v2-design-pro', '.agents', 'scratch', '__pycache__', 'node_modules', '.stfolder']]
        for file in files:
            file2 = os.path.join(root, file)
            rel_path = os.path.relpath(file2, dir2)
            file1 = os.path.join(dir1, rel_path)
            if not os.path.exists(file1):
                print(f"Only in {dir2}: {rel_path}")

compare_dirs(".", "v2-design-pro")
