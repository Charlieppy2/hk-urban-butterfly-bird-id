"""
Model Training Script for HK Urban Ecological Identification
Trains a CNN model to classify plants and birds in Hong Kong
"""

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.metrics import TopKCategoricalAccuracy
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# Configuration
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 100
LEARNING_RATE = 0.0001
VALIDATION_SPLIT = 0.2
TEST_SPLIT = 0.1

# Paths
DATA_DIR = '../../data/processed'
TRAIN_DIR = os.path.join(DATA_DIR, 'train')
MODEL_SAVE_DIR = '../../models/trained'
os.makedirs(MODEL_SAVE_DIR, exist_ok=True)


def create_data_generators():
    """Create data generators with augmentation"""
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=VALIDATION_SPLIT
    )
    
    # Only rescaling for validation and test
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=VALIDATION_SPLIT
    )
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Validation generator
    val_generator = val_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    return train_generator, val_generator


def build_model(num_classes):
    """Build the model using transfer learning"""
    
    # Load pre-trained MobileNetV2
    base_model = MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Build model
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=[
            'accuracy',
            TopKCategoricalAccuracy(k=3, name='top_3_accuracy')
        ]
    )
    
    return model


def train_model():
    """Main training function"""
    
    print("=" * 50)
    print("HK Urban Ecological Identification - Model Training")
    print("=" * 50)
    
    # Check if data directory exists
    if not os.path.exists(TRAIN_DIR):
        print(f"Error: Training data directory not found at {TRAIN_DIR}")
        print("Please organize your images in the following structure:")
        print("data/processed/train/")
        print("  ├── class1/")
        print("  ├── class2/")
        print("  └── ...")
        return
    
    # Create data generators
    print("\n[1/5] Creating data generators...")
    train_generator, val_generator = create_data_generators()
    
    # Get class names
    class_names = list(train_generator.class_indices.keys())
    num_classes = len(class_names)
    
    print(f"\nFound {num_classes} classes:")
    for i, class_name in enumerate(class_names):
        print(f"  {i+1}. {class_name}")
    
    # Save class names
    class_names_path = os.path.join(MODEL_SAVE_DIR, 'class_names.json')
    with open(class_names_path, 'w', encoding='utf-8') as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)
    print(f"\nClass names saved to {class_names_path}")
    
    # Build model
    print("\n[2/5] Building model...")
    model = build_model(num_classes)
    model.summary()
    
    # Callbacks
    checkpoint = ModelCheckpoint(
        os.path.join(MODEL_SAVE_DIR, 'model.h5'),
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=15,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=0.00001,
        verbose=1
    )
    
    # Train model
    print("\n[3/5] Training model...")
    print(f"Training for {EPOCHS} epochs with batch size {BATCH_SIZE}")
    
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=[checkpoint, early_stopping, reduce_lr],
        verbose=1
    )
    
    # Fine-tuning: Unfreeze some layers
    print("\n[4/5] Fine-tuning model...")
    base_model = model.layers[0]
    base_model.trainable = True
    
    # Freeze first 100 layers
    for layer in base_model.layers[:100]:
        layer.trainable = False
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE / 10),
        loss='categorical_crossentropy',
        metrics=[
            'accuracy',
            TopKCategoricalAccuracy(k=3, name='top_3_accuracy')
        ]
    )
    
    # Continue training
    history_finetune = model.fit(
        train_generator,
        epochs=20,
        validation_data=val_generator,
        callbacks=[checkpoint, early_stopping, reduce_lr],
        verbose=1,
        initial_epoch=len(history.history['loss'])
    )
    
    # Evaluate model
    print("\n[5/5] Evaluating model...")
    val_loss, val_accuracy, val_top3 = model.evaluate(val_generator, verbose=1)
    
    print("\n" + "=" * 50)
    print("Training Results:")
    print("=" * 50)
    print(f"Validation Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")
    print(f"Validation Top-3 Accuracy: {val_top3:.4f} ({val_top3*100:.2f}%)")
    print(f"Validation Loss: {val_loss:.4f}")
    
    # Generate predictions for classification report
    val_generator.reset()
    predictions = model.predict(val_generator, verbose=1)
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = val_generator.classes
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(true_classes, predicted_classes, 
                                target_names=class_names))
    
    # Plot training history
    plot_training_history(history, history_finetune)
    
    # Plot confusion matrix
    plot_confusion_matrix(true_classes, predicted_classes, class_names)
    
    print(f"\nModel saved to {os.path.join(MODEL_SAVE_DIR, 'model.h5')}")
    print("=" * 50)


def plot_training_history(history, history_finetune=None):
    """Plot training history"""
    
    # Combine histories
    if history_finetune:
        for key in history.history.keys():
            history.history[key].extend(history_finetune.history[key])
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Accuracy plot
    axes[0].plot(history.history['accuracy'], label='Training Accuracy')
    axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
    axes[0].set_title('Model Accuracy')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(True)
    
    # Loss plot
    axes[1].plot(history.history['loss'], label='Training Loss')
    axes[1].plot(history.history['val_loss'], label='Validation Loss')
    axes[1].set_title('Model Loss')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_SAVE_DIR, 'training_history.png'), dpi=300)
    print(f"\nTraining history plot saved to {os.path.join(MODEL_SAVE_DIR, 'training_history.png')}")


def plot_confusion_matrix(true_classes, predicted_classes, class_names):
    """Plot confusion matrix"""
    
    cm = confusion_matrix(true_classes, predicted_classes)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_SAVE_DIR, 'confusion_matrix.png'), dpi=300)
    print(f"Confusion matrix plot saved to {os.path.join(MODEL_SAVE_DIR, 'confusion_matrix.png')}")


if __name__ == '__main__':
    # Set GPU memory growth
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)
    
    train_model()

