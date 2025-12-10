"""
Bird Sound Model Runner
Load and run the trained bird sound identification model
"""

import os
import sys
import numpy as np

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

def load_model():
    """Load the bird sound model"""
    model_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try to find model file
    model_files = []
    for ext in ['.h5', '.pkl', '.pt', '.pth', '.pb', '.onnx']:
        for file in os.listdir(model_dir):
            if file.endswith(ext) and 'bird_sound' in file.lower():
                model_files.append(os.path.join(model_dir, file))
    
    if not model_files:
        print("❌ Error: No bird_sound model file found in:", model_dir)
        print("📁 Please place your model file in this directory.")
        print("   Supported formats: .h5, .pkl, .pt, .pth, .pb, .onnx")
        return None
    
    model_path = model_files[0]
    print(f"📂 Found model file: {os.path.basename(model_path)}")
    
    # Try to load based on file extension
    file_ext = os.path.splitext(model_path)[1].lower()
    
    try:
        if file_ext == '.h5':
            # Keras/TensorFlow H5 format
            import tensorflow as tf
            print("🔄 Loading Keras/TensorFlow model...")
            model = tf.keras.models.load_model(model_path)
            print("✅ Model loaded successfully!")
            return model
        
        elif file_ext in ['.pt', '.pth']:
            # PyTorch format
            import torch
            print("🔄 Loading PyTorch model...")
            model = torch.load(model_path, map_location='cpu')
            print("✅ Model loaded successfully!")
            return model
        
        elif file_ext == '.pkl':
            # Pickle format
            import pickle
            print("🔄 Loading Pickle model...")
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print("✅ Model loaded successfully!")
            return model
        
        elif file_ext == '.pb':
            # TensorFlow SavedModel
            import tensorflow as tf
            print("🔄 Loading TensorFlow SavedModel...")
            model = tf.saved_model.load(model_path)
            print("✅ Model loaded successfully!")
            return model
        
        elif file_ext == '.onnx':
            # ONNX format
            import onnxruntime as ort
            print("🔄 Loading ONNX model...")
            model = ort.InferenceSession(model_path)
            print("✅ Model loaded successfully!")
            return model
        
        else:
            print(f"❌ Unsupported file format: {file_ext}")
            return None
    
    except ImportError as e:
        print(f"❌ Error: Required library not installed: {e}")
        print("💡 Please install the required library:")
        if file_ext == '.h5' or file_ext == '.pb':
            print("   pip install tensorflow")
        elif file_ext in ['.pt', '.pth']:
            print("   pip install torch")
        elif file_ext == '.onnx':
            print("   pip install onnxruntime")
        return None
    
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return None


def predict(model, input_data):
    """Run prediction on input data"""
    try:
        # Get model file extension to determine format
        model_dir = os.path.dirname(os.path.abspath(__file__))
        model_files = [f for f in os.listdir(model_dir) if f.endswith(('.h5', '.pkl', '.pt', '.pth', '.pb', '.onnx')) and 'bird_sound' in f.lower()]
        
        if not model_files:
            print("❌ Model file not found")
            return None
        
        file_ext = os.path.splitext(model_files[0])[1].lower()
        
        if file_ext == '.h5':
            # Keras/TensorFlow
            predictions = model.predict(input_data, verbose=0)
            return predictions
        
        elif file_ext in ['.pt', '.pth']:
            # PyTorch
            import torch
            if isinstance(input_data, np.ndarray):
                input_data = torch.from_numpy(input_data).float()
            model.eval()
            with torch.no_grad():
                predictions = model(input_data)
            return predictions.numpy() if isinstance(predictions, torch.Tensor) else predictions
        
        elif file_ext == '.pkl':
            # Pickle (could be sklearn, etc.)
            if hasattr(model, 'predict'):
                return model.predict(input_data)
            elif callable(model):
                return model(input_data)
            else:
                print("❌ Model object doesn't have predict method")
                return None
        
        elif file_ext == '.pb':
            # TensorFlow SavedModel
            # This is more complex, depends on model signature
            print("⚠️ TensorFlow SavedModel prediction requires specific input format")
            print("   Please check your model's input signature")
            return None
        
        elif file_ext == '.onnx':
            # ONNX
            input_name = model.get_inputs()[0].name
            output = model.run(None, {input_name: input_data})
            return output[0]
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function"""
    print("=" * 60)
    print("🦅 Bird Sound Model Runner")
    print("=" * 60)
    
    # Load model
    model = load_model()
    if model is None:
        return
    
    # Display model info
    print("\n📊 Model Information:")
    print(f"   Model type: {type(model).__name__}")
    
    if hasattr(model, 'summary'):
        print("\n📋 Model Summary:")
        model.summary()
    elif hasattr(model, '__class__'):
        print(f"   Class: {model.__class__.__name__}")
    
    print("\n✅ Model is ready to use!")
    print("\n💡 To use this model in your application:")
    print("   1. Import this script or the load_model function")
    print("   2. Load the model: model = load_model()")
    print("   3. Run predictions: predictions = predict(model, input_data)")
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()

