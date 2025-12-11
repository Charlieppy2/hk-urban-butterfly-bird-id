"""
创建测试训练数据（从Colab notebook提取）
用于快速测试训练流程

Usage:
    python create_test_data.py
"""

import pandas as pd
import os

def create_test_data(output_file='training_data_interpretation_en.csv', num_samples=20):
    """
    创建测试训练数据
    
    Args:
        output_file: 输出文件名
        num_samples: 测试样本数量
    """
    print("📝 创建测试训练资料...")
    
    test_data = []
    categories = ["migration", "singing", "feeding", "resting", "fighting"]
    
    # 创建测试样本
    for i in range(1, num_samples + 1):
        test_data.append({
            "species_en": f"Species_{i}",
            "category": categories[i % len(categories)],
            "interpretation_text": f"This is test interpretation #{i} for behavior analysis."
        })
    
    df = pd.DataFrame(test_data)
    df.to_csv(output_file, index=False)
    
    print(f"✅ 已创建: {output_file}")
    print(f"📊 资料行数: {len(df)}")
    print("\n📋 前3行预览:")
    print(df.head(3))
    
    # 确认文件存在
    print("\n🔍 文件检查:")
    print("文件路径:", os.path.abspath(output_file))
    print("文件大小:", os.path.getsize(output_file), "bytes")
    
    return df

if __name__ == "__main__":
    create_test_data()
    print("\n🎯 现在你可以执行 train_model() 了！")

