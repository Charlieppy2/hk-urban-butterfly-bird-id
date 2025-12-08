"""
Quick script to check training progress
"""
import os
import json
from datetime import datetime

MODEL_DIR = '../../models/trained'

print("=" * 50)
print("Training Progress Check")
print("=" * 50)

# Check if model exists
model_path = os.path.join(MODEL_DIR, 'model.h5')
if os.path.exists(model_path):
    import os
    file_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
    mod_time = datetime.fromtimestamp(os.path.getmtime(model_path))
    print(f"\n[OK] Model file exists!")
    print(f"   Size: {file_size:.2f} MB")
    print(f"   Last modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    print("\n[WAIT] Model file not yet created (training may be starting...)")

# Check class names
class_names_path = os.path.join(MODEL_DIR, 'class_names.json')
if os.path.exists(class_names_path):
    with open(class_names_path, 'r', encoding='utf-8') as f:
        class_names = json.load(f)
    print(f"\n[OK] Class names file exists!")
    print(f"   Number of classes: {len(class_names)}")
    print(f"   First 5 classes: {class_names[:5]}")
else:
    print("\n[WAIT] Class names file not yet created")

# Check for training history plot
history_path = os.path.join(MODEL_DIR, 'training_history.png')
if os.path.exists(history_path):
    print(f"\n[OK] Training history plot exists!")
else:
    print("\n[WAIT] Training history plot not yet created")

print("\n" + "=" * 50)
print("To see real-time training output:")
print("1. Open a new terminal/PowerShell window")
print("2. Navigate to: models/training")
print("3. Run: python train_model.py")
print("=" * 50)

