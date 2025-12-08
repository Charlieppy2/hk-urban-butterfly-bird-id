"""
測試圖片路徑是否正確
"""

import json
import os

# 讀取蝴蝶數據
with open('butterfly_info_template.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 測試 ADONIS
adonis = data.get('ADONIS', {})
image_path = adonis.get('image_path', '')
print(f"ADONIS image_path: {image_path}")

# 構建完整路徑
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if image_path.startswith('../'):
    full_path = os.path.join(base_dir, image_path.replace('../', ''))
else:
    full_path = os.path.join(base_dir, image_path)

full_path = os.path.normpath(full_path)
print(f"Base dir: {base_dir}")
print(f"Full path: {full_path}")
print(f"File exists: {os.path.exists(full_path)}")

if os.path.exists(full_path):
    print(f"✅ Image file found!")
else:
    # 嘗試查找實際文件
    raw_dir = os.path.join(base_dir, 'data', 'raw', 'ADONIS')
    print(f"\nChecking raw directory: {raw_dir}")
    if os.path.exists(raw_dir):
        files = [f for f in os.listdir(raw_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"Files in ADONIS directory: {files[:5]}")
        if files:
            correct_path = os.path.join(raw_dir, files[0])
            rel_path = os.path.relpath(correct_path, base_dir)
            print(f"\n✅ Correct path should be: {rel_path}")
            print(f"   Current path in JSON: {image_path}")

