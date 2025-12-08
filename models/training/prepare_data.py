"""
Data Preparation Script
Organizes raw images into train/validation/test splits
"""

import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
import json

RAW_DATA_DIR = '../../data/raw'
PROCESSED_DATA_DIR = '../../data/processed'
TRAIN_DIR = os.path.join(PROCESSED_DATA_DIR, 'train')
VAL_DIR = os.path.join(PROCESSED_DATA_DIR, 'val')
TEST_DIR = os.path.join(PROCESSED_DATA_DIR, 'test')

TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15


def organize_data():
    """Organize raw data into train/val/test splits"""
    
    print("=" * 50)
    print("Data Preparation for HK Urban Ecological Identification")
    print("=" * 50)
    
    if not os.path.exists(RAW_DATA_DIR):
        print(f"Error: Raw data directory not found at {RAW_DATA_DIR}")
        print("\nPlease organize your raw images in the following structure:")
        print("data/raw/")
        print("  ├── class1/")
        print("  │   ├── image1.jpg")
        print("  │   └── ...")
        print("  ├── class2/")
        print("  └── ...")
        return
    
    # Get all class directories
    classes = [d for d in os.listdir(RAW_DATA_DIR) 
               if os.path.isdir(os.path.join(RAW_DATA_DIR, d))]
    
    if not classes:
        print(f"No class directories found in {RAW_DATA_DIR}")
        return
    
    print(f"\nFound {len(classes)} classes:")
    for cls in classes:
        print(f"  - {cls}")
    
    # Create output directories
    for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        os.makedirs(split_dir, exist_ok=True)
        for cls in classes:
            os.makedirs(os.path.join(split_dir, cls), exist_ok=True)
    
    # Process each class
    dataset_info = {
        'total_images': 0,
        'classes': {},
        'splits': {
            'train': 0,
            'val': 0,
            'test': 0
        }
    }
    
    for cls in classes:
        class_dir = os.path.join(RAW_DATA_DIR, cls)
        images = [f for f in os.listdir(class_dir) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        
        if not images:
            print(f"Warning: No images found in {cls}")
            continue
        
        # Split images
        train_images, temp_images = train_test_split(
            images, test_size=(1 - TRAIN_RATIO), random_state=42
        )
        val_images, test_images = train_test_split(
            temp_images, test_size=(TEST_RATIO / (VAL_RATIO + TEST_RATIO)), random_state=42
        )
        
        # Copy images to respective directories
        for img in train_images:
            src = os.path.join(class_dir, img)
            dst = os.path.join(TRAIN_DIR, cls, img)
            shutil.copy2(src, dst)
        
        for img in val_images:
            src = os.path.join(class_dir, img)
            dst = os.path.join(VAL_DIR, cls, img)
            shutil.copy2(src, dst)
        
        for img in test_images:
            src = os.path.join(class_dir, img)
            dst = os.path.join(TEST_DIR, cls, img)
            shutil.copy2(src, dst)
        
        # Update dataset info
        dataset_info['classes'][cls] = {
            'total': len(images),
            'train': len(train_images),
            'val': len(val_images),
            'test': len(test_images)
        }
        dataset_info['total_images'] += len(images)
        dataset_info['splits']['train'] += len(train_images)
        dataset_info['splits']['val'] += len(val_images)
        dataset_info['splits']['test'] += len(test_images)
        
        print(f"\n{cls}:")
        print(f"  Total: {len(images)}")
        print(f"  Train: {len(train_images)} ({len(train_images)/len(images)*100:.1f}%)")
        print(f"  Val: {len(val_images)} ({len(val_images)/len(images)*100:.1f}%)")
        print(f"  Test: {len(test_images)} ({len(test_images)/len(images)*100:.1f}%)")
    
    # Save dataset info
    info_path = os.path.join(PROCESSED_DATA_DIR, 'dataset_info.json')
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(dataset_info, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 50)
    print("Data Preparation Complete!")
    print("=" * 50)
    print(f"Total images: {dataset_info['total_images']}")
    print(f"Train: {dataset_info['splits']['train']}")
    print(f"Validation: {dataset_info['splits']['val']}")
    print(f"Test: {dataset_info['splits']['test']}")
    print(f"\nDataset info saved to {info_path}")
    print(f"\nProcessed data structure:")
    print(f"  {PROCESSED_DATA_DIR}/")
    print(f"    ├── train/")
    print(f"    ├── val/")
    print(f"    └── test/")


if __name__ == '__main__':
    organize_data()

