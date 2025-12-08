#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从 JSON 文件中提取所有需要的图片路径
用于 Docker 构建时只下载需要的图片，而不是全部 24,380 张
"""

import json
import os
import sys

# 设置 UTF-8 编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def extract_image_paths(json_file_path):
    """从 JSON 文件中提取所有图片路径"""
    image_paths = []
    
    if not os.path.exists(json_file_path):
        print(f"❌ 文件不存在: {json_file_path}")
        return image_paths
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # data 是字典结构
        for species_key, species in data.items():
            if isinstance(species, dict) and 'image_path' in species and species['image_path']:
                image_path = species['image_path']
                # 移除可能的相对路径前缀
                if image_path.startswith('../'):
                    image_path = image_path.replace('../', '', 1)
                elif image_path.startswith('./'):
                    image_path = image_path.replace('./', '', 1)
                image_paths.append(image_path)
        
        print(f"✅ 从 {json_file_path} 提取了 {len(image_paths)} 个图片路径")
        return image_paths
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return []

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    bird_file = os.path.join(script_dir, 'bird_info_template.json')
    butterfly_file = os.path.join(script_dir, 'butterfly_info_template.json')
    
    all_paths = []
    
    if os.path.exists(bird_file):
        all_paths.extend(extract_image_paths(bird_file))
    
    if os.path.exists(butterfly_file):
        all_paths.extend(extract_image_paths(butterfly_file))
    
    # 输出到文件，供 Dockerfile 使用
    output_file = os.path.join(script_dir, 'required_images.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        for path in all_paths:
            f.write(f"{path}\n")
    
    print(f"\n✅ 总共提取了 {len(all_paths)} 个图片路径")
    print(f"✅ 已保存到: {output_file}")
    print(f"📊 这将大大减少需要下载的文件数量（从 24,380 个减少到 {len(all_paths)} 个）")

