"""
獲取鳥類詳細資料的工具
從多個來源獲取鳥類的詳細信息
"""

import json
import os
import requests
from typing import Dict, List, Optional

# 鳥類信息來源
BIRD_INFO_SOURCES = {
    'ebird': 'https://ebird.org/species/',
    'wikipedia': 'https://en.wikipedia.org/wiki/',
    'allaboutbirds': 'https://www.allaboutbirds.org/guide/',
    'audubon': 'https://www.audubon.org/field-guide/bird/'
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

def extract_bird_name(class_name: str) -> str:
    """從類別名稱中提取鳥類名稱"""
    # 格式: "001.Black_footed_Albatross" -> "Black_footed_Albatross"
    if '.' in class_name:
        return class_name.split('.', 1)[1]
    return class_name

def format_bird_name_for_url(bird_name: str, source: str) -> str:
    """格式化鳥類名稱用於 URL"""
    # 替換下劃線為空格或連字符
    formatted = bird_name.replace('_', ' ')
    
    if source == 'ebird':
        # eBird 使用科學名稱或通用名稱，需要轉換
        formatted = formatted.lower().replace(' ', '_')
    elif source == 'wikipedia':
        formatted = formatted.replace(' ', '_')
    elif source == 'allaboutbirds':
        formatted = formatted.lower().replace(' ', '_')
    elif source == 'audubon':
        formatted = formatted.lower().replace(' ', '_')
    
    return formatted

def get_bird_info_links(bird_name: str) -> Dict[str, str]:
    """獲取鳥類信息的各種鏈接"""
    formatted_name = extract_bird_name(bird_name)
    
    links = {}
    for source, base_url in BIRD_INFO_SOURCES.items():
        formatted = format_bird_name_for_url(formatted_name, source)
        links[source] = f"{base_url}{formatted}"
    
    return links

def create_bird_info_template():
    """創建鳥類信息模板文件"""
    class_names = load_class_names()
    
    # 只處理前 200 個（鳥類）
    bird_classes = [name for name in class_names[:200] if name.startswith(('0', '1', '2'))]
    
    bird_info = {}
    
    print(f"處理 {len(bird_classes)} 種鳥類...")
    print("="*60)
    
    for idx, class_name in enumerate(bird_classes, 1):
        bird_name = extract_bird_name(class_name)
        links = get_bird_info_links(class_name)
        
        bird_info[class_name] = {
            "id": idx,
            "common_name": bird_name.replace('_', ' '),
            "scientific_name": "",  # 需要手動填寫或從 API 獲取
            "description": "",  # 需要手動填寫或從 API 獲取
            "habitat": "",
            "distribution": "",
            "size": "",
            "diet": "",
            "behavior": "",
            "links": links,
            "notes": ""
        }
        
        if idx % 20 == 0:
            print(f"已處理 {idx}/{len(bird_classes)} 種鳥類...")
    
    # 保存到文件
    output_path = os.path.join(os.path.dirname(__file__), 'bird_info_template.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(bird_info, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Created template file: {output_path}")
    print(f"[OK] Contains basic info and links for {len(bird_classes)} bird species")
    print("\nNext steps:")
    print("1. Use provided links to find detailed info for each bird")
    print("2. Or use eBird API, Wikipedia API to fetch automatically")
    print("3. Fill in the blank fields in the template file")
    
    return bird_info

def search_bird_info_online(bird_name: str) -> Dict:
    """在線搜索鳥類信息（示例）"""
    # 這是一個示例函數，實際實現需要調用各種 API
    # 例如：eBird API, Wikipedia API, iNaturalist API 等
    
    info = {
        "name": bird_name,
        "sources": get_bird_info_links(bird_name),
        "suggestions": [
            f"搜索 '{bird_name.replace('_', ' ')}' 在以下網站:",
            "- eBird.org (詳細觀察記錄和分佈)",
            "- AllAboutBirds.org (康奈爾大學鳥類指南)",
            "- Wikipedia (百科全書信息)",
            "- Audubon.org (奧杜邦協會指南)"
        ]
    }
    
    return info

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'create':
        create_bird_info_template()
    elif len(sys.argv) > 1:
        bird_name = sys.argv[1]
        info = search_bird_info_online(bird_name)
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        print("用法:")
        print("  python fetch_bird_info.py create          - 創建鳥類信息模板")
        print("  python fetch_bird_info.py <bird_name>      - 搜索特定鳥類信息")
        print("\n示例:")
        print("  python fetch_bird_info.py create")
        print("  python fetch_bird_info.py Black_footed_Albatross")

