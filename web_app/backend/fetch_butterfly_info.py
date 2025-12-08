"""
獲取蝴蝶詳細資料的工具
從多個來源獲取蝴蝶的詳細信息
"""

import json
import os
import sys
from typing import Dict, List, Optional

# 設置 UTF-8 編碼
sys.stdout.reconfigure(encoding='utf-8')

# 蝴蝶信息來源
BUTTERFLY_INFO_SOURCES = {
    'wikipedia': 'https://en.wikipedia.org/wiki/',
    'butterfliesandmoths': 'https://www.butterfliesandmoths.org/species/',
    'butterflyidentification': 'https://www.butterflyidentification.com/',
    'inaturalist': 'https://www.inaturalist.org/taxa/'
}

def load_class_names():
    """加載類別名稱"""
    class_names_path = os.path.join(
        os.path.dirname(__file__),
        '../../models/trained/class_names.json'
    )
    
    if os.path.exists(class_names_path):
        with open(class_names_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def extract_butterfly_name(class_name: str) -> str:
    """從類別名稱中提取蝴蝶名稱"""
    # 蝴蝶類別沒有編號前綴，直接返回
    return class_name

def format_butterfly_name_for_url(butterfly_name: str, source: str) -> str:
    """格式化蝴蝶名稱用於 URL"""
    # 替換空格為下劃線或連字符
    formatted = butterfly_name.replace(' ', '_')
    
    if source == 'wikipedia':
        formatted = formatted.replace('_', '_')
    elif source == 'butterfliesandmoths':
        formatted = formatted.lower().replace('_', '-')
    elif source == 'butterflyidentification':
        formatted = formatted.lower().replace('_', '-')
    elif source == 'inaturalist':
        formatted = formatted.lower().replace('_', '-')
    
    return formatted

def generate_butterfly_template():
    """生成蝴蝶信息模板"""
    class_names = load_class_names()
    
    # 提取蝴蝶類別（沒有編號前綴的）
    butterfly_classes = [c for c in class_names if not c.split('.')[0].isdigit()]
    
    print(f"找到 {len(butterfly_classes)} 種蝴蝶/蛾類")
    
    template = {}
    
    for idx, butterfly_name in enumerate(butterfly_classes, start=1):
        # 生成外部鏈接
        links = {}
        for source, base_url in BUTTERFLY_INFO_SOURCES.items():
            formatted_name = format_butterfly_name_for_url(butterfly_name, source)
            links[source] = f"{base_url}{formatted_name}"
        
        template[butterfly_name] = {
            "id": idx,
            "common_name": butterfly_name,
            "scientific_name": "",
            "description": "",
            "habitat": "",
            "distribution": "",
            "wingspan": "",
            "diet": "",
            "behavior": "",
            "lifecycle": "",
            "links": links,
            "notes": ""
        }
    
    return template

def save_template(template: Dict, output_path: str = 'butterfly_info_template.json'):
    """保存模板到文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    print(f"\n模板已保存到: {output_path}")
    print(f"共 {len(template)} 種蝴蝶/蛾類")

def main():
    """主函數"""
    print("=" * 60)
    print("生成蝴蝶信息模板")
    print("=" * 60)
    
    template = generate_butterfly_template()
    save_template(template)
    
    print("\n完成！")
    print("\n下一步：使用 batch_update_butterfly_info.py 批量添加詳細資料")

if __name__ == '__main__':
    main()

