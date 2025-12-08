"""
更新物種數據中的圖片路徑，從 data/processed/train 改為 data/raw
"""

import json
import os
import sys

# 設置 UTF-8 編碼
sys.stdout.reconfigure(encoding='utf-8')

def update_image_paths_to_raw(file_path):
    """更新JSON文件中的圖片路徑，從 processed/train 改為 raw"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for species_key, species_info in data.items():
        if 'image_path' in species_info and species_info['image_path']:
            old_path = species_info['image_path']
            # 將 processed/train 或 processed/val 或 processed/test 替換為 raw
            if 'processed/train' in old_path:
                new_path = old_path.replace('processed/train', 'raw')
                species_info['image_path'] = new_path
                updated_count += 1
                print(f"✓ Updated: {species_key}")
                print(f"  {old_path}")
                print(f"  → {new_path}")
            elif 'processed/val' in old_path:
                new_path = old_path.replace('processed/val', 'raw')
                species_info['image_path'] = new_path
                updated_count += 1
                print(f"✓ Updated: {species_key}")
                print(f"  {old_path}")
                print(f"  → {new_path}")
            elif 'processed/test' in old_path:
                new_path = old_path.replace('processed/test', 'raw')
                species_info['image_path'] = new_path
                updated_count += 1
                print(f"✓ Updated: {species_key}")
                print(f"  {old_path}")
                print(f"  → {new_path}")
            elif 'raw' in old_path:
                print(f"○ Already using raw: {species_key}")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return updated_count

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    bird_info_path = os.path.join(script_dir, 'bird_info_template.json')
    butterfly_info_path = os.path.join(script_dir, 'butterfly_info_template.json')
    
    print("=" * 60)
    print("Updating image paths from processed/train to raw")
    print("=" * 60)
    
    print("\n[1/2] Processing birds...")
    bird_count = update_image_paths_to_raw(bird_info_path)
    
    print("\n[2/2] Processing butterflies...")
    butterfly_count = update_image_paths_to_raw(butterfly_info_path)
    
    print("\n" + "=" * 60)
    print(f"✅ Complete! Updated {bird_count} bird paths and {butterfly_count} butterfly paths")
    print("=" * 60)

