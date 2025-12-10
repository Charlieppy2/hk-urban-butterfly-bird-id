"""
Test script for bird sound model
Creates a dummy input and tests the model prediction
"""

import os
import sys
import numpy as np
import json

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from run_bird_sound_model import load_model, predict

def main():
    print("=" * 60)
    print("🧪 Testing Bird Sound Model")
    print("=" * 60)
    
    # Load model
    print("\n1️⃣ Loading model...")
    model = load_model()
    if model is None:
        return
    
    # Load class names
    print("\n2️⃣ Loading class names...")
    model_dir = os.path.dirname(os.path.abspath(__file__))
    class_names_path = os.path.join(model_dir, 'class_names.json')
    
    if os.path.exists(class_names_path):
        with open(class_names_path, 'r', encoding='utf-8') as f:
            class_names = json.load(f)
        print(f"✅ Loaded {len(class_names)} bird classes:")
        for i, name in enumerate(class_names, 1):
            print(f"   {i:2d}. {name}")
    else:
        print("⚠️ class_names.json not found")
        class_names = [f"Class_{i}" for i in range(16)]
    
    # Create dummy input (128x128 spectrogram-like data)
    print("\n3️⃣ Creating test input...")
    # Model expects input shape: (batch_size, 128, 128, 1) for spectrogram
    test_input = np.random.rand(1, 128, 128, 1).astype(np.float32)
    print(f"   Input shape: {test_input.shape}")
    
    # Run prediction
    print("\n4️⃣ Running prediction...")
    try:
        predictions = predict(model, test_input)
        
        if predictions is not None:
            print(f"✅ Prediction successful!")
            print(f"   Output shape: {predictions.shape}")
            
            # Get top prediction
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            predicted_class = class_names[predicted_class_idx] if predicted_class_idx < len(class_names) else f"Class_{predicted_class_idx}"
            
            print(f"\n📊 Prediction Results:")
            print(f"   Predicted: {predicted_class}")
            print(f"   Confidence: {confidence:.2%}")
            
            # Show top 3 predictions
            top_3_indices = np.argsort(predictions[0])[-3:][::-1]
            print(f"\n🏆 Top 3 Predictions:")
            for i, idx in enumerate(top_3_indices, 1):
                conf = float(predictions[0][idx])
                class_name = class_names[idx] if idx < len(class_names) else f"Class_{idx}"
                print(f"   {i}. {class_name}: {conf:.2%}")
        else:
            print("❌ Prediction returned None")
    
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ Test completed!")

if __name__ == '__main__':
    main()

