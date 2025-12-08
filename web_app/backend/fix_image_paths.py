"""
修復圖片路徑，確保從 data/raw 中找到正確的圖片文件
"""

import json
import os
import sys

# 設置 UTF-8 編碼
sys.stdout.reconfigure(encoding='utf-8')

def find_first_image_in_dir(directory):
    """在目錄中找到第一張圖片"""
    if not os.path.exists(directory):
        return None
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    for file in os.listdir(directory):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            return file
    return None

def fix_image_paths(file_path, data_dir):
    """修復JSON文件中的圖片路徑"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    not_found_count = 0
    
    for species_key, species_info in data.items():
        # 構建 raw 目錄路徑
        raw_dir = os.path.join(data_dir, 'raw', species_key)
        
        # 查找第一張圖片
        image_file = find_first_image_in_dir(raw_dir)
        
        if image_file:
            # 構建相對路徑（相對於項目根目錄）
            rel_path = os.path.relpath(
                os.path.join(raw_dir, image_file),
                os.path.dirname(os.path.dirname(file_path))
            )
            new_path = rel_path.replace('\\', '/')
            
            # 更新路徑
            species_info['image_path'] = new_path
            updated_count += 1
            print(f"✓ {species_key}: {image_file}")
        else:
            not_found_count += 1
            print(f"✗ {species_key}: No image found in {raw_dir}")
            # 如果找不到，移除圖片路徑
            if 'image_path' in species_info:
                del species_info['image_path']
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return updated_count, not_found_count

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    bird_info_path = os.path.join(script_dir, 'bird_info_template.json')
    butterfly_info_path = os.path.join(script_dir, 'butterfly_info_template.json')
    data_dir = os.path.join(os.path.dirname(os.path.dirname(script_dir)), 'data')
    
    print("=" * 60)
    print("Fixing image paths from data/raw")
    print("=" * 60)
    
    print("\n[1/2] Processing birds...")
    bird_updated, bird_not_found = fix_image_paths(bird_info_path, data_dir)
    
    print("\n[2/2] Processing butterflies...")
    butterfly_updated, butterfly_not_found = fix_image_paths(butterfly_info_path, data_dir)
    
    print("\n" + "=" * 60)
    print(f"✅ Complete!")
    print(f"   Birds: {bird_updated} updated, {bird_not_found} not found")
    print(f"   Butterflies: {butterfly_updated} updated, {butterfly_not_found} not found")
    print("=" * 60)

