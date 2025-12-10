"""
测试鸟声音识别API的完整流程
"""
import os
import sys
import numpy as np
import requests
import json

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(project_root, 'web_app', 'backend'))

def test_model_loading():
    """测试模型加载"""
    print("=" * 60)
    print("1️⃣ 测试模型加载")
    print("=" * 60)
    
    try:
        import app
        
        app.load_bird_sound_model()
        
        if app.bird_sound_model is None:
            print("❌ 模型未加载")
            return False
        
        print(f"✅ 模型已加载")
        print(f"✅ 类别数量: {len(app.bird_sound_class_names)}")
        print(f"   类别列表: {app.bird_sound_class_names[:5]}...")
        return True
    except Exception as e:
        print(f"❌ 加载模型时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_audio_processing():
    """测试音频处理"""
    print("\n" + "=" * 60)
    print("2️⃣ 测试音频处理功能")
    print("=" * 60)
    
    try:
        import app
        
        # 创建一个测试音频文件（使用numpy生成模拟音频）
        import tempfile
        import soundfile as sf
        
        # 生成3秒的测试音频（采样率22050）
        duration = 3.0
        sample_rate = 22050
        t = np.linspace(0, duration, int(sample_rate * duration))
        # 生成一个简单的正弦波（440Hz，A4音符）
        audio_data = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        
        # 保存为临时WAV文件
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            sf.write(tmp_path, audio_data, sample_rate)
        
        print(f"📁 创建测试音频文件: {tmp_path}")
        
        # 转换为频谱图
        spectrogram = app.audio_to_spectrogram(tmp_path)
        
        if spectrogram is None:
            print("❌ 音频处理失败")
            os.unlink(tmp_path)
            return False
        
        print(f"✅ 音频处理成功")
        print(f"   频谱图形状: {spectrogram.shape}")
        print(f"   数据类型: {spectrogram.dtype}")
        print(f"   数值范围: [{spectrogram.min():.4f}, {spectrogram.max():.4f}]")
        
        # 清理临时文件
        os.unlink(tmp_path)
        return True, spectrogram
        
    except ImportError as e:
        print(f"⚠️ 缺少依赖: {e}")
        print("   尝试安装: pip install soundfile")
        return False, None
    except Exception as e:
        print(f"❌ 音频处理出错: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_model_prediction(spectrogram):
    """测试模型预测"""
    print("\n" + "=" * 60)
    print("3️⃣ 测试模型预测")
    print("=" * 60)
    
    try:
        import app
        
        if app.bird_sound_model is None:
            print("❌ 模型未加载，无法测试预测")
            return False
        
        print(f"📊 运行预测...")
        predictions = app.bird_sound_model.predict(spectrogram, verbose=0)
        
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        if app.bird_sound_class_names and predicted_class_idx < len(app.bird_sound_class_names):
            predicted_class = app.bird_sound_class_names[predicted_class_idx]
        else:
            predicted_class = f"Class_{predicted_class_idx}"
        
        print(f"✅ 预测成功")
        print(f"   预测类别: {predicted_class}")
        print(f"   置信度: {confidence:.2%}")
        print(f"   输出形状: {predictions.shape}")
        
        # 显示前3个预测
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        print(f"\n🏆 前3个预测:")
        for i, idx in enumerate(top_3_indices, 1):
            conf = float(predictions[0][idx])
            class_name = app.bird_sound_class_names[idx] if idx < len(app.bird_sound_class_names) else f"Class_{idx}"
            print(f"   {i}. {class_name}: {conf:.2%}")
        
        return True
        
    except Exception as e:
        print(f"❌ 预测出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoint():
    """测试API端点"""
    print("\n" + "=" * 60)
    print("4️⃣ 测试API端点")
    print("=" * 60)
    
    try:
        # 检查健康状态
        response = requests.get('http://localhost:5001/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API健康检查通过")
            print(f"   模型加载状态: {data.get('bird_sound_model_loaded', False)}")
            print(f"   类别数量: {data.get('bird_sound_classes', 0)}")
        else:
            print(f"⚠️ API健康检查返回状态码: {response.status_code}")
        
        # 测试预测端点（需要音频文件，这里只检查端点是否存在）
        print(f"\n📡 预测端点: http://localhost:5001/api/predict-sound")
        print(f"   (需要上传音频文件才能完整测试)")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到后端服务 (http://localhost:5001)")
        print(f"   请确保后端服务正在运行")
        return False
    except Exception as e:
        print(f"❌ API测试出错: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("🧪 鸟声音识别模型诊断工具")
    print("=" * 60)
    
    # 测试1: 模型加载
    model_loaded = test_model_loading()
    if not model_loaded:
        print("\n❌ 模型加载失败，无法继续测试")
        return
    
    # 测试2: 音频处理
    audio_ok, spectrogram = test_audio_processing()
    if not audio_ok or spectrogram is None:
        print("\n❌ 音频处理失败，无法继续测试")
        return
    
    # 测试3: 模型预测
    prediction_ok = test_model_prediction(spectrogram)
    if not prediction_ok:
        print("\n❌ 模型预测失败")
        return
    
    # 测试4: API端点
    api_ok = test_api_endpoint()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 诊断总结")
    print("=" * 60)
    print(f"✅ 模型加载: {'通过' if model_loaded else '失败'}")
    print(f"{'✅' if audio_ok else '❌'} 音频处理: {'通过' if audio_ok else '失败'}")
    print(f"{'✅' if prediction_ok else '❌'} 模型预测: {'通过' if prediction_ok else '失败'}")
    print(f"{'✅' if api_ok else '❌'} API端点: {'通过' if api_ok else '失败'}")
    
    if model_loaded and audio_ok and prediction_ok:
        print("\n✅ 所有测试通过！模型应该可以正常工作。")
    else:
        print("\n⚠️ 部分测试失败，请检查上述错误信息。")

if __name__ == '__main__':
    main()

