"""
測試圖片API是否正常工作
"""

import requests
import json

# 讀取蝴蝶數據
with open('butterfly_info_template.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 測試 ADONIS 的圖片路徑
adonis = data.get('ADONIS', {})
image_path = adonis.get('image_path', '')
print(f"ADONIS image_path: {image_path}")

# 構建測試 URL
API_URL = "http://localhost:5000"
test_url = f"{API_URL}/api/species-image/{image_path.replace('../', '')}"
print(f"\n測試 URL: {test_url}")

# 嘗試請求圖片
try:
    response = requests.get(test_url, timeout=5)
    print(f"狀態碼: {response.status_code}")
    if response.status_code == 200:
        print("✅ 圖片請求成功！")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
    else:
        print(f"❌ 圖片請求失敗: {response.text}")
except requests.exceptions.ConnectionError:
    print("❌ 無法連接到後端服務器。請確保後端正在運行。")
except Exception as e:
    print(f"❌ 錯誤: {e}")

