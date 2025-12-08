"""
為物種數據添加圖片路徑
從訓練數據集中找到每個物種的代表圖片
"""

import json
import os
import sys
from pathlib import Path

# 設置 UTF-8 編碼
sys.stdout.reconfigure(encoding='utf-8')

def find_species_image(species_key, data_dir):
    """
    為物種找到圖片路徑
    species_key: 例如 "001.Black_footed_Albatross" 或 "ADONIS"
    data_dir: 數據目錄路徑
    """
    # 優先從 data/raw 查找圖片
    possible_dirs = [
        os.path.join(data_dir, 'raw'),  # 優先使用 raw 目錄
        os.path.join(data_dir, 'processed', 'train'),
        os.path.join(data_dir, 'processed', 'val'),
        os.path.join(data_dir, 'processed', 'test'),
    ]
    
    # 提取類別名稱（去掉編號前綴）
    if '.' in species_key:
        class_name = species_key.split('.', 1)[1]
    else:
        class_name = species_key
    
    # 支持的圖片格式
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    # 在每個目錄中查找
    for base_dir in possible_dirs:
        if not os.path.exists(base_dir):
            continue
            
        # 查找類別目錄
        class_dir = os.path.join(base_dir, species_key)
        if not os.path.exists(class_dir):
            # 嘗試使用類別名稱（無編號）
            class_dir = os.path.join(base_dir, class_name)
        
        if os.path.exists(class_dir):
            # 查找第一張圖片
            for file in os.listdir(class_dir):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    # 返回相對路徑（相對於項目根目錄）
                    rel_path = os.path.relpath(
                        os.path.join(class_dir, file),
                        os.path.dirname(os.path.dirname(__file__))
                    )
                    return rel_path.replace('\\', '/')  # 統一使用正斜杠
    
    return None

def add_images_to_birds():
    """為鳥類數據添加圖片路徑"""
    script_dir = os.path.dirname(__file__)
    bird_info_path = os.path.join(script_dir, 'bird_info_template.json')
    data_dir = os.path.join(os.path.dirname(os.path.dirname(script_dir)), 'data')
    
    with open(bird_info_path, 'r', encoding='utf-8') as f:
        bird_data = json.load(f)
    
    updated_count = 0
    for species_key, species_info in bird_data.items():
        if not species_info.get('image_path'):
            image_path = find_species_image(species_key, data_dir)
            if image_path:
                species_info['image_path'] = image_path
                updated_count += 1
                print(f"✓ Added image for: {species_key}")
            else:
                print(f"✗ No image found for: {species_key}")
    
    with open(bird_info_path, 'w', encoding='utf-8') as f:
        json.dump(bird_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Updated {updated_count} bird species with images")
    return updated_count

def add_images_to_butterflies():
    """為蝴蝶數據添加圖片路徑"""
    script_dir = os.path.dirname(__file__)
    butterfly_info_path = os.path.join(script_dir, 'butterfly_info_template.json')
    data_dir = os.path.join(os.path.dirname(os.path.dirname(script_dir)), 'data')
    
    with open(butterfly_info_path, 'r', encoding='utf-8') as f:
        butterfly_data = json.load(f)
    
    updated_count = 0
    for species_key, species_info in butterfly_data.items():
        if not species_info.get('image_path'):
            image_path = find_species_image(species_key, data_dir)
            if image_path:
                species_info['image_path'] = image_path
                updated_count += 1
                print(f"✓ Added image for: {species_key}")
            else:
                print(f"✗ No image found for: {species_key}")
    
    with open(butterfly_info_path, 'w', encoding='utf-8') as f:
        json.dump(butterfly_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Updated {updated_count} butterfly/moth species with images")
    return updated_count

if __name__ == '__main__':
    print("=" * 60)
    print("Adding images to species data")
    print("=" * 60)
    
    print("\n[1/2] Processing birds...")
    bird_count = add_images_to_birds()
    
    print("\n[2/2] Processing butterflies...")
    butterfly_count = add_images_to_butterflies()
    
    print("\n" + "=" * 60)
    print(f"✅ Complete! Added images to {bird_count} birds and {butterfly_count} butterflies")
    print("=" * 60)

