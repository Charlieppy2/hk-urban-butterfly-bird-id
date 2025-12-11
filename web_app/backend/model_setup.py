"""
模型設置與加載模塊
用於加載中文文本生成預訓練模型

選擇的模型：GPT-2 中文版本 (uer/gpt2-chinese-cluecorpussmall)
選擇理由：
1. 專為中文設計，對中文文本生成效果好
2. 模型大小適中（約500MB），易於部署
3. 基於Transformer架構，易於微調
4. 在中文文本生成任務上表現良好
5. 有豐富的社區支持和文檔
"""

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os

def load_model_and_tokenizer(model_path=None, device='cpu'):
    """
    加載GPT-2中文模型和分詞器
    
    Args:
        model_path: 預訓練模型路徑（如果為None，則使用默認的預訓練模型）
        device: 運行設備 ('cpu' 或 'cuda')
    
    Returns:
        model: 加載的模型
        tokenizer: 分詞器
    """
    print("🔄 正在加載模型和分詞器...")
    
    # 如果提供了本地模型路徑，使用本地模型
    if model_path and os.path.exists(model_path):
        print(f"📂 從本地路徑加載模型: {model_path}")
        model = GPT2LMHeadModel.from_pretrained(model_path)
        tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    else:
        # 使用Hugging Face上的中文GPT-2模型
        # 嘗試多個模型名稱，選擇可用的
        model_names = [
            "uer/gpt2-chinese-cluecorpussmall",
            "gpt2",  # 英文GPT-2作為備選
        ]
        
        model_loaded = False
        for model_name in model_names:
            try:
                print(f"📥 嘗試從Hugging Face下載模型: {model_name}")
                tokenizer = GPT2Tokenizer.from_pretrained(model_name)
                model = GPT2LMHeadModel.from_pretrained(model_name)
                print(f"✅ 成功加載模型: {model_name}")
                model_loaded = True
                break
            except Exception as e:
                print(f"⚠️ 無法加載 {model_name}: {e}")
                continue
        
        if not model_loaded:
            print("❌ 所有模型加載失敗")
            print("💡 提示：請檢查網絡連接或手動下載模型")
            raise Exception("無法加載任何預訓練模型")
    
    # 設置pad_token（GPT-2默認沒有pad_token）
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # 將模型移到指定設備
    model = model.to(device)
    model.eval()  # 設置為評估模式
    
    print(f"✅ 模型和分詞器加載成功 (設備: {device})")
    print(f"   模型參數數量: {sum(p.numel() for p in model.parameters()):,}")
    
    return model, tokenizer

def prepare_input(species, category, tokenizer, max_length=128):
    """
    準備模型輸入
    
    Args:
        species: 物種名稱
        category: 類別（如fun_fact, behavior, habitat）
        tokenizer: 分詞器
        max_length: 最大長度
    
    Returns:
        input_ids: 編碼後的輸入ID
        attention_mask: 注意力掩碼
    """
    # 構建輸入文本：物種 + 類別
    # 格式："{species}的{category}："
    input_text = f"{species}的{category}："
    
    # 使用分詞器編碼
    encoded = tokenizer.encode_plus(
        input_text,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    
    return encoded['input_ids'], encoded['attention_mask']

if __name__ == "__main__":
    # 測試加載模型
    print("=" * 60)
    print("🧪 測試模型加載")
    print("=" * 60)
    
    try:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"使用設備: {device}")
        
        model, tokenizer = load_model_and_tokenizer(device=device)
        
        # 測試輸入準備
        print("\n🧪 測試輸入準備...")
        input_ids, attention_mask = prepare_input("臺灣藍鵲", "fun_fact", tokenizer)
        print(f"✅ 輸入準備成功")
        print(f"   輸入形狀: {input_ids.shape}")
        print(f"   輸入文本: 臺灣藍鵲的fun_fact：")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()

