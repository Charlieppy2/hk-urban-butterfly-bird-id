#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复图片路径格式：将 ../data/raw/... 改为 data/raw/...
这样在部署环境中路径解析更可靠
"""

import json
import os
import sys

# 设置 UTF-8 编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def fix_image_paths(json_file_path):
    """修复 JSON 文件中的图片路径"""
    print(f"正在处理: {json_file_path}")
    
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
    
    # 修复图片路径
    # data 是字典结构，键是物种名称，值是物种信息对象
    fixed_count = 0
    for species_key, species in data.items():
        if isinstance(species, dict) and 'image_path' in species and species['image_path']:
            original_path = species['image_path']
            # 移除 ../ 前缀
            if original_path.startswith('../'):
                new_path = original_path.replace('../', '', 1)
                species['image_path'] = new_path
                fixed_count += 1
                if fixed_count <= 5:  # 只打印前5个，避免输出太多
                    print(f"  ✓ {species.get('common_name', species_key)}: {original_path} -> {new_path}")
            elif original_path.startswith('./'):
                new_path = original_path.replace('./', '', 1)
                species['image_path'] = new_path
                fixed_count += 1
                if fixed_count <= 5:  # 只打印前5个，避免输出太多
                    print(f"  ✓ {species.get('common_name', species_key)}: {original_path} -> {new_path}")
    
    if fixed_count > 5:
        print(f"  ... 还有 {fixed_count - 5} 个路径已修复")
    
    # 保存修复后的 JSON
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 已修复 {fixed_count} 个图片路径")
        return True
    except Exception as e:
        print(f"❌ 保存文件失败: {e}")
        return False

if __name__ == '__main__':
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 处理鸟类和蝴蝶的 JSON 文件
    bird_file = os.path.join(script_dir, 'bird_info_template.json')
    butterfly_file = os.path.join(script_dir, 'butterfly_info_template.json')
    
    print("=" * 60)
    print("修复图片路径格式")
    print("=" * 60)
    
    success = True
    if os.path.exists(bird_file):
        success = fix_image_paths(bird_file) and success
    else:
        print(f"⚠️ 文件不存在: {bird_file}")
    
    print()
    
    if os.path.exists(butterfly_file):
        success = fix_image_paths(butterfly_file) and success
    else:
        print(f"⚠️ 文件不存在: {butterfly_file}")
    
    print()
    print("=" * 60)
    if success:
        print("✅ 所有文件处理完成！")
    else:
        print("❌ 处理过程中出现错误")
    print("=" * 60)

