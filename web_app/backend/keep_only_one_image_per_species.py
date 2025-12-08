#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
为每个物种只保留一张图片，删除多余的图片
这样可以大大减少 Git LFS 需要管理的文件数量
"""

import json
import os
import sys
import shutil
from pathlib import Path

# 设置 UTF-8 编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def keep_only_one_image(data_dir, json_file_path, species_type='bird'):
    """
    为每个物种只保留一张图片，删除多余的图片
    
    Args:
        data_dir: 数据目录路径（项目根目录）
        json_file_path: JSON 文件路径
        species_type: 物种类型 ('bird' 或 'butterfly')
    """
    print(f"正在处理 {species_type} 数据...")
    print(f"数据目录: {data_dir}")
    print(f"JSON 文件: {json_file_path}")
    print("=" * 60)
    
    # 读取 JSON 文件
    if not os.path.exists(json_file_path):
        print(f"❌ JSON 文件不存在: {json_file_path}")
        return False
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 读取 JSON 文件失败: {e}")
        return False
    
    raw_dir = os.path.join(data_dir, 'data', 'raw')
    if not os.path.exists(raw_dir):
        print(f"❌ 数据目录不存在: {raw_dir}")
        return False
    
    deleted_count = 0
    kept_count = 0
    updated_json_count = 0
    
    # 处理每个物种
    for species_key, species_info in data.items():
        if not isinstance(species_info, dict):
            continue
        
        # 获取物种目录
        species_dir = os.path.join(raw_dir, species_key)
        
        if not os.path.exists(species_dir):
            # 尝试查找匹配的目录（可能名称略有不同）
            matching_dirs = [d for d in os.listdir(raw_dir) 
                           if os.path.isdir(os.path.join(raw_dir, d)) and 
                           (species_key.lower() in d.lower() or d.lower() in species_key.lower())]
            if matching_dirs:
                species_dir = os.path.join(raw_dir, matching_dirs[0])
            else:
                print(f"⚠️  目录不存在: {species_key}")
                continue
        
        # 获取所有图片文件
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        image_files = [f for f in os.listdir(species_dir) 
                      if os.path.isfile(os.path.join(species_dir, f)) and
                      any(f.lower().endswith(ext) for ext in image_extensions)]
        
        if len(image_files) == 0:
            print(f"⚠️  没有找到图片: {species_key}")
            continue
        
        if len(image_files) == 1:
            # 已经只有一张图片，更新 JSON 路径
            image_file = image_files[0]
            image_path = f"data/raw/{species_key}/{image_file}"
            if species_info.get('image_path') != image_path:
                species_info['image_path'] = image_path
                updated_json_count += 1
            kept_count += 1
            continue
        
        # 有多张图片，只保留第一张
        image_files.sort()  # 按文件名排序，确保一致性
        keep_file = image_files[0]
        delete_files = image_files[1:]
        
        # 删除多余的图片
        for file_to_delete in delete_files:
            file_path = os.path.join(species_dir, file_to_delete)
            try:
                os.remove(file_path)
                deleted_count += 1
                print(f"  🗑️  删除: {species_key}/{file_to_delete}")
            except Exception as e:
                print(f"  ❌ 删除失败 {file_to_delete}: {e}")
        
        # 更新 JSON 中的图片路径
        image_path = f"data/raw/{species_key}/{keep_file}"
        species_info['image_path'] = image_path
        updated_json_count += 1
        kept_count += 1
        print(f"  ✅ 保留: {species_key}/{keep_file} (删除了 {len(delete_files)} 张)")
    
    # 保存更新后的 JSON
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print()
        print("=" * 60)
        print(f"✅ 处理完成！")
        print(f"   - 保留了 {kept_count} 个物种的图片")
        print(f"   - 删除了 {deleted_count} 张多余的图片")
        print(f"   - 更新了 {updated_json_count} 个 JSON 条目")
        print("=" * 60)
        return True
    except Exception as e:
        print(f"❌ 保存 JSON 文件失败: {e}")
        return False

if __name__ == '__main__':
    # 获取项目根目录（脚本在 web_app/backend 目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    bird_json = os.path.join(script_dir, 'bird_info_template.json')
    butterfly_json = os.path.join(script_dir, 'butterfly_info_template.json')
    
    print("=" * 60)
    print("为每个物种只保留一张图片")
    print("=" * 60)
    print()
    
    success = True
    
    # 处理鸟类
    if os.path.exists(bird_json):
        success = keep_only_one_image(project_root, bird_json, 'bird') and success
        print()
    else:
        print(f"⚠️  文件不存在: {bird_json}")
    
    # 处理蝴蝶
    if os.path.exists(butterfly_json):
        success = keep_only_one_image(project_root, butterfly_json, 'butterfly') and success
    else:
        print(f"⚠️  文件不存在: {butterfly_json}")
    
    print()
    if success:
        print("✅ 所有处理完成！")
        print()
        print("下一步：")
        print("1. 检查删除的图片是否正确")
        print("2. 使用 'git add -A' 添加更改")
        print("3. 使用 'git commit' 提交更改")
        print("4. 使用 'git lfs prune' 清理 LFS 缓存（可选）")
    else:
        print("❌ 处理过程中出现错误")

