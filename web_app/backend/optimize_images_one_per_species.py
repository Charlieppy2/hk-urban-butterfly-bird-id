#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
优化图片：每个物种只保留一张图片
这样可以大大减少需要下载的文件数量（从 24,380 个减少到 300 个）
"""

import json
import os
import sys

# 设置 UTF-8 编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def get_first_image_for_species(species_key, data_dir):
    """
    为物种找到第一张图片
    species_key: 例如 "001.Black_footed_Albatross" 或 "ADONIS"
    data_dir: 数据目录路径（项目根目录）
    """
    # 只从 data/raw 查找图片（因为这是我们要使用的）
    raw_dir = os.path.join(data_dir, 'raw')
    
    if not os.path.exists(raw_dir):
        return None
    
    # 提取类名（去掉编号前缀）
    if '.' in species_key:
        class_name = species_key.split('.', 1)[1]
    else:
        class_name = species_key
    
    # 支持的图片格式
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    # 查找类别目录
    species_dir = os.path.join(raw_dir, species_key)
    if not os.path.exists(species_dir):
        # 尝试使用类名（无编号）
        species_dir = os.path.join(raw_dir, class_name)
    
    if not os.path.exists(species_dir):
        return None
    
    # 查找第一张图片
    for file in sorted(os.listdir(species_dir)):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            # 返回相对路径（相对于项目根目录）
            rel_path = os.path.relpath(
                os.path.join(species_dir, file),
                data_dir
            )
            return rel_path.replace('\\', '/')  # 统一使用正斜杠
    
    return None

def optimize_json_images(json_file_path, data_dir):
    """优化 JSON 文件中的图片路径，确保每个物种只有一张图片"""
    print(f"\n正在处理: {json_file_path}")
    
    if not os.path.exists(json_file_path):
        print(f"❌ 文件不存在: {json_file_path}")
        return False
    
    # 读取 JSON 文件
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False
    
    # 优化图片路径
    updated_count = 0
    missing_count = 0
    kept_count = 0
    
    for species_key, species in data.items():
        if not isinstance(species, dict):
            continue
        
        current_path = species.get('image_path', '')
        
        # 如果已经有图片路径，先尝试使用它
        if current_path:
            # 确保路径格式正确（data/raw/...）
            clean_path = current_path
            if clean_path.startswith('../'):
                clean_path = clean_path.replace('../', '', 1)
            elif clean_path.startswith('./'):
                clean_path = clean_path.replace('./', '', 1)
            
            # 检查文件是否存在
            full_path = os.path.join(data_dir, clean_path)
            if os.path.exists(full_path):
                # 文件存在，使用当前路径
                species['image_path'] = clean_path
                kept_count += 1
                continue
        
        # 如果当前路径不存在或为空，尝试查找第一张图片
        image_path = get_first_image_for_species(species_key, data_dir)
        
        if image_path:
            # 确保路径格式正确（data/raw/...）
            if image_path.startswith('../'):
                image_path = image_path.replace('../', '', 1)
            elif image_path.startswith('./'):
                image_path = image_path.replace('./', '', 1)
            
            # 更新图片路径
            old_path = species.get('image_path', '')
            species['image_path'] = image_path
            
            if old_path != image_path:
                updated_count += 1
                if updated_count <= 5:  # 只打印前5个
                    print(f"  ✓ {species.get('common_name', species_key)}: {image_path}")
        else:
            missing_count += 1
            if missing_count <= 5:  # 只打印前5个缺失的
                print(f"  ⚠️ {species.get('common_name', species_key)}: 未找到图片")
            # 保留原有路径（即使文件可能不存在），让用户知道应该有什么路径
            if not current_path:
                species['image_path'] = None
    
    # 保存优化后的 JSON
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已保留 {kept_count} 个现有图片路径")
        print(f"✅ 已更新 {updated_count} 个图片路径")
        if missing_count > 0:
            print(f"⚠️  有 {missing_count} 个物种未找到图片")
        if missing_count > 5:
            print(f"   （只显示了前 5 个缺失的物种）")
        
        return True
    except Exception as e:
        print(f"❌ 保存文件失败: {e}")
        return False

def create_minimal_image_list(data_dir):
    """
    创建一个列表，包含每个物种只需要的一张图片
    这个列表可以用于 Git LFS 选择性下载
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    data_dir = os.path.join(project_root, 'data')
    
    bird_file = os.path.join(script_dir, 'bird_info_template.json')
    butterfly_file = os.path.join(script_dir, 'butterfly_info_template.json')
    
    image_list = []
    
    for json_file in [bird_file, butterfly_file]:
        if not os.path.exists(json_file):
            continue
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for species_key, species in data.items():
                if isinstance(species, dict) and species.get('image_path'):
                    image_path = species['image_path']
                    # 转换为 Git LFS 路径格式
                    if image_path.startswith('data/'):
                        image_list.append(image_path)
        except Exception as e:
            print(f"读取 {json_file} 失败: {e}")
    
    # 保存图片列表到文件
    list_file = os.path.join(script_dir, 'required_images.txt')
    try:
        with open(list_file, 'w', encoding='utf-8') as f:
            for img_path in sorted(image_list):
                f.write(f"{img_path}\n")
        print(f"\n✅ 已创建图片列表文件: {list_file}")
        print(f"   包含 {len(image_list)} 张图片（每个物种一张）")
        return list_file
    except Exception as e:
        print(f"❌ 创建图片列表失败: {e}")
        return None

if __name__ == '__main__':
    # 获取脚本所在目录和项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    data_dir = os.path.join(project_root, 'data')
    
    # 处理鸟类和蝴蝶的 JSON 文件
    bird_file = os.path.join(script_dir, 'bird_info_template.json')
    butterfly_file = os.path.join(script_dir, 'butterfly_info_template.json')
    
    print("=" * 60)
    print("优化图片：每个物种只保留一张图片")
    print("=" * 60)
    print(f"项目根目录: {project_root}")
    print(f"数据目录: {data_dir}")
    
    success = True
    
    if os.path.exists(bird_file):
        success = optimize_json_images(bird_file, project_root) and success
    else:
        print(f"⚠️ 文件不存在: {bird_file}")
    
    if os.path.exists(butterfly_file):
        success = optimize_json_images(butterfly_file, project_root) and success
    else:
        print(f"⚠️ 文件不存在: {butterfly_file}")
    
    # 创建图片列表文件（用于选择性下载）
    create_minimal_image_list(project_root)
    
    print()
    print("=" * 60)
    if success:
        print("✅ 优化完成！")
        print("   现在每个物种只有一张图片，大大减少了文件数量")
        print("   从 ~24,380 个文件减少到 ~300 个文件")
    else:
        print("❌ 优化过程中出现错误")
    print("=" * 60)

