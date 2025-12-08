"""
Test if model can be loaded and used for prediction
"""
import os
import json
import numpy as np
import tensorflow as tf
from PIL import Image
from datetime import datetime
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Path configuration
MODEL_DIR = '../../models/trained'
MODEL_PATH = os.path.join(MODEL_DIR, 'model.h5')
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, 'class_names.json')

print("=" * 60)
print("Model Loading Test")
print("=" * 60)

# 1. Check if files exist
print("\n[1/4] Checking if files exist...")
if os.path.exists(MODEL_PATH):
    file_size = os.path.getsize(MODEL_PATH) / (1024 * 1024)  # MB
    mod_time = datetime.fromtimestamp(os.path.getmtime(MODEL_PATH))
    print(f"  [OK] Model file exists: {MODEL_PATH}")
    print(f"    - Size: {file_size:.2f} MB")
    print(f"    - Last modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    print(f"  [ERROR] Model file not found: {MODEL_PATH}")
    exit(1)

if os.path.exists(CLASS_NAMES_PATH):
    print(f"  [OK] Class names file exists: {CLASS_NAMES_PATH}")
else:
    print(f"  [ERROR] Class names file not found: {CLASS_NAMES_PATH}")
    exit(1)

# 2. Load class names
print("\n[2/4] Loading class names...")
try:
    with open(CLASS_NAMES_PATH, 'r', encoding='utf-8') as f:
        class_names = json.load(f)
    print(f"  [OK] Successfully loaded {len(class_names)} classes")
    print(f"    - First 5 classes: {class_names[:5]}")
    print(f"    - Last 5 classes: {class_names[-5:]}")
except Exception as e:
    print(f"  [ERROR] Failed to load class names: {e}")
    exit(1)

# 3. Load model
print("\n[3/4] Loading model...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"  [OK] Model loaded successfully!")
    print(f"    - Model type: {type(model)}")
    
    # Display model summary info
    print("\n  Model structure info:")
    print(f"    - Input shape: {model.input_shape}")
    print(f"    - Output shape: {model.output_shape}")
    print(f"    - Total parameters: {model.count_params():,}")
    
    # Check if model is compiled
    if hasattr(model, 'optimizer') and model.optimizer is not None:
        print(f"    - Optimizer: {type(model.optimizer).__name__}")
    else:
        print(f"    - Warning: Model not compiled (may need recompilation)")
        
except Exception as e:
    print(f"  [ERROR] Failed to load model: {e}")
    print(f"    Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    exit(1)

# 4. Test prediction function
print("\n[4/4] Testing prediction function...")
try:
    # Create a random test image (224x224x3)
    test_image = np.random.randint(0, 255, size=(224, 224, 3), dtype=np.uint8)
    
    # Preprocess image (normalize to 0-1 range)
    test_image_normalized = test_image.astype('float32') / 255.0
    
    # Add batch dimension
    test_image_batch = np.expand_dims(test_image_normalized, axis=0)
    
    print(f"  - Test image shape: {test_image_batch.shape}")
    
    # Make prediction
    predictions = model.predict(test_image_batch, verbose=0)
    
    print(f"  [OK] Prediction successful!")
    print(f"    - Prediction output shape: {predictions.shape}")
    print(f"    - Prediction sum: {predictions.sum():.6f} (should be 1.0)")
    
    # Get top-3 predictions
    top3_indices = np.argsort(predictions[0])[-3:][::-1]
    top3_probs = predictions[0][top3_indices]
    
    print(f"\n  Top-3 predictions:")
    for i, (idx, prob) in enumerate(zip(top3_indices, top3_probs), 1):
        class_name = class_names[idx] if idx < len(class_names) else f"Class{idx}"
        print(f"    {i}. {class_name}: {prob*100:.2f}%")
    
    # Verify prediction output is correct
    if predictions.shape[1] == len(class_names):
        print(f"  [OK] Output class count matches ({predictions.shape[1]} == {len(class_names)})")
    else:
        print(f"  [WARNING] Output class count mismatch ({predictions.shape[1]} != {len(class_names)})")
    
    if abs(predictions.sum() - 1.0) < 0.01:
        print(f"  [OK] Prediction probability sum is correct (close to 1.0)")
    else:
        print(f"  [WARNING] Prediction probability sum is abnormal ({predictions.sum():.6f})")
        
except Exception as e:
    print(f"  [ERROR] Prediction test failed: {e}")
    print(f"    Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("[SUCCESS] All tests passed! Model can be used normally.")
print("=" * 60)

