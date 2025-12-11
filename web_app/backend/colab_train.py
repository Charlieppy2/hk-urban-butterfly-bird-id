"""
Complete Training Script for Colab
Copy this entire file to Colab and run it

Usage in Colab:
1. Upload training_data_interpretation_en.csv to Colab
2. Run this script
"""

# ============================================================================
# STEP 1: Install Dependencies
# ============================================================================
print("=" * 60)
print("STEP 1: Installing dependencies...")
print("=" * 60)

import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])

packages = [
    "torch",
    "transformers",
    "pandas",
    "numpy",
    "tqdm",
    "nltk"
]

for pkg in packages:
    try:
        install_package(pkg)
        print(f"✅ {pkg} installed")
    except:
        print(f"⚠️ {pkg} installation failed")

# Download NLTK data
try:
    import nltk
    nltk.download('punkt', quiet=True)
    print("✅ NLTK data downloaded")
except:
    print("⚠️ NLTK data download skipped")

print("\n✅ All dependencies installed!\n")

# ============================================================================
# STEP 2: Import Libraries
# ============================================================================
print("=" * 60)
print("STEP 2: Importing libraries...")
print("=" * 60)

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, GPT2Tokenizer, get_linear_schedule_with_warmup
from torch.optim import AdamW
import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import json
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import warnings
warnings.filterwarnings('ignore')

print("✅ Libraries imported!\n")

# ============================================================================
# STEP 3: Dataset Class
# ============================================================================
print("=" * 60)
print("STEP 3: Setting up dataset class...")
print("=" * 60)

class InterpretationDataset(Dataset):
    """Dataset class for loading and processing training data"""
    
    def __init__(self, csv_path, tokenizer, max_length=256):
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Read CSV data
        df = pd.read_csv(csv_path)
        self.data = df.to_dict('records')
        
        print(f"✅ Loaded {len(self.data)} training samples")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        
        # Build input: species (English) + category + interpretation
        species_en = item['species_en']
        category = item['category']
        interpretation = item['interpretation_text']
        
        # Input format: "Species: {species_en}, Category: {category}, Interpretation: {interpretation}"
        input_text = f"Species: {species_en}, Category: {category}, Interpretation: {interpretation}"
        
        # Encode with tokenizer
        encoded = self.tokenizer.encode_plus(
            input_text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        input_ids = encoded['input_ids'].squeeze()
        attention_mask = encoded['attention_mask'].squeeze()
        
        # Labels are the same as input_ids (for loss calculation)
        labels = input_ids.clone()
        
        # Set padding positions to -100 (will be ignored in loss calculation)
        labels[labels == self.tokenizer.pad_token_id] = -100
        
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }

print("✅ Dataset class ready!\n")

# ============================================================================
# STEP 4: Helper Functions
# ============================================================================
print("=" * 60)
print("STEP 4: Setting up helper functions...")
print("=" * 60)

def calculate_perplexity(model, dataloader, device):
    """Calculate perplexity"""
    model.eval()
    total_loss = 0
    total_tokens = 0
    
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Calculating perplexity"):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            
            valid_tokens = (labels != -100).sum().item()
            total_loss += loss.item() * valid_tokens
            total_tokens += valid_tokens
    
    avg_loss = total_loss / total_tokens if total_tokens > 0 else float('inf')
    perplexity = torch.exp(torch.tensor(avg_loss)).item()
    
    return perplexity

def calculate_bleu(model, tokenizer, test_data, device, num_samples=10):
    """Calculate BLEU score"""
    model.eval()
    bleu_scores = []
    smoothing = SmoothingFunction().method1
    
    sample_indices = np.random.choice(len(test_data), min(num_samples, len(test_data)), replace=False)
    
    with torch.no_grad():
        for idx in sample_indices:
            item = test_data[idx]
            species_en = item['species_en']
            category = item['category']
            reference = item['interpretation_text']
            
            input_text = f"Species: {species_en}, Category: {category}, Interpretation:"
            input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
            
            output = model.generate(
                input_ids,
                max_length=256,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.2
            )
            
            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
            generated_text = generated_text.replace(input_text, "").strip()
            
            reference_tokens = reference.split()
            generated_tokens = generated_text.split()
            
            try:
                bleu = sentence_bleu([reference_tokens], generated_tokens, smoothing_function=smoothing)
                bleu_scores.append(bleu)
            except:
                pass
    
    avg_bleu = np.mean(bleu_scores) if bleu_scores else 0.0
    return avg_bleu

print("✅ Helper functions ready!\n")

# ============================================================================
# STEP 5: Main Training Function
# ============================================================================
print("=" * 60)
print("STEP 5: Main training function...")
print("=" * 60)

def train_model(
    csv_path='training_data_interpretation_en.csv',
    output_dir='interpretation_model',
    num_epochs=10,
    batch_size=4,
    learning_rate=5e-5,
    max_length=256,
    warmup_steps=50
):
    """Main training function"""
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}\n")
    
    print("=" * 60)
    print("🚀 Starting Interpretation Generation Model Training")
    print("=" * 60)
    
    # 1. Load model and tokenizer
    print("\n📥 Step 1: Loading pretrained model...")
    model_name = "gpt2"
    print(f"📥 Loading model from Hugging Face: {model_name}")
    
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model = model.to(device)
    model.train()
    
    print(f"✅ Model loaded (parameters: {sum(p.numel() for p in model.parameters()):,})")
    
    # 2. Prepare dataset
    print("\n📊 Step 2: Preparing dataset...")
    dataset = InterpretationDataset(csv_path, tokenizer, max_length=max_length)
    
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    print(f"   Training set: {len(train_dataset)} samples")
    print(f"   Validation set: {len(val_dataset)} samples")
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # 3. Setup optimizer
    print("\n⚙️ Step 3: Setting up optimizer...")
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    
    total_steps = len(train_loader) * num_epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_steps
    )
    
    print(f"   Total training steps: {total_steps}")
    print(f"   Warmup steps: {warmup_steps}")
    
    # 4. Training loop
    print("\n🎯 Step 4: Starting training...")
    best_val_loss = float('inf')
    training_history = []
    
    for epoch in range(num_epochs):
        print(f"\n{'='*60}")
        print(f"📅 Epoch {epoch + 1}/{num_epochs}")
        print(f"{'='*60}")
        
        # Training phase
        model.train()
        total_train_loss = 0
        
        progress_bar = tqdm(train_loader, desc=f"Training Epoch {epoch + 1}")
        for batch in progress_bar:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            
            total_train_loss += loss.item()
            progress_bar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        avg_train_loss = total_train_loss / len(train_loader)
        
        # Validation phase
        print(f"\n🔍 Validation phase...")
        model.eval()
        total_val_loss = 0
        
        with torch.no_grad():
            for batch in tqdm(val_loader, desc="Validating"):
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)
                
                outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
                total_val_loss += outputs.loss.item()
        
        avg_val_loss = total_val_loss / len(val_loader)
        
        # Calculate perplexity
        print(f"\n📊 Calculating perplexity...")
        perplexity = calculate_perplexity(model, val_loader, device)
        
        # Calculate BLEU (every 2 epochs or last epoch)
        bleu_score = 0.0
        if (epoch + 1) % 2 == 0 or epoch == num_epochs - 1:
            print(f"📊 Calculating BLEU score...")
            val_data = [dataset.data[i] for i in val_dataset.indices]
            bleu_score = calculate_bleu(model, tokenizer, val_data, device, num_samples=5)
        
        # Record training history
        epoch_history = {
            'epoch': epoch + 1,
            'train_loss': avg_train_loss,
            'val_loss': avg_val_loss,
            'perplexity': perplexity,
            'bleu': bleu_score
        }
        training_history.append(epoch_history)
        
        print(f"\n📈 Epoch {epoch + 1} Results:")
        print(f"   Training loss: {avg_train_loss:.4f}")
        print(f"   Validation loss: {avg_val_loss:.4f}")
        print(f"   Perplexity: {perplexity:.2f}")
        if bleu_score > 0:
            print(f"   BLEU score: {bleu_score:.4f}")
        
        # Save best model
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            print(f"\n💾 Saving best model (validation loss: {avg_val_loss:.4f})...")
            
            os.makedirs(output_dir, exist_ok=True)
            model.save_pretrained(output_dir)
            tokenizer.save_pretrained(output_dir)
            
            with open(os.path.join(output_dir, 'training_history.json'), 'w', encoding='utf-8') as f:
                json.dump(training_history, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print("✅ Training completed!")
    print(f"{'='*60}")
    print(f"📁 Model saved to: {output_dir}")
    print(f"📊 Best validation loss: {best_val_loss:.4f}")

print("✅ Training function ready!\n")

# ============================================================================
# STEP 6: Check if CSV exists, create test data if not
# ============================================================================
print("=" * 60)
print("STEP 6: Checking training data...")
print("=" * 60)

import os
if not os.path.exists('training_data_interpretation_en.csv'):
    print("⚠️ training_data_interpretation_en.csv not found!")
    print("💡 Creating test data for quick testing...")
    print("   (You can replace this with real data later)\n")
    
    # Create test data
    import pandas as pd
    test_data = []
    for i in range(1, 21):
        test_data.append({
            "species_en": f"Species_{i}",
            "category": ["migration", "singing", "feeding", "resting", "fighting"][i % 5],
            "interpretation_text": f"This is test interpretation #{i} for behavior analysis."
        })
    df = pd.DataFrame(test_data)
    df.to_csv('training_data_interpretation_en.csv', index=False)
    print(f"✅ Created test data: {len(df)} samples")
    print("   Note: This is test data. For real training, upload your CSV file.\n")
else:
    print("✅ Found training_data_interpretation_en.csv\n")

# ============================================================================
# STEP 7: Run Training
# ============================================================================
print("=" * 60)
print("STEP 7: Starting training...")
print("=" * 60)

# Training parameters
# Quick test mode (from Colab): num_epochs=3, max_length=128, warmup_steps=10
# Full training mode: num_epochs=10, max_length=256, warmup_steps=50

# 快速测试模式（从Colab提取的参数）
QUICK_TEST = True  # 设置为False使用完整训练参数

if QUICK_TEST:
    print("🚀 Quick Test Mode (from Colab notebook)")
    print("   Parameters: 3 epochs, max_length=128, warmup_steps=10\n")
    train_model(
        csv_path='training_data_interpretation_en.csv',
        output_dir='interpretation_model',
        num_epochs=3,
        batch_size=4,
        learning_rate=5e-5,
        max_length=128,
        warmup_steps=10
    )
else:
    print("🚀 Full Training Mode")
    print("   Parameters: 10 epochs, max_length=256, warmup_steps=50\n")
    train_model(
        csv_path='training_data_interpretation_en.csv',
        output_dir='interpretation_model',
        num_epochs=10,
        batch_size=4,
        learning_rate=5e-5,
        max_length=256,
        warmup_steps=50
    )

print("\n" + "=" * 60)
print("🎉 All done! Model saved to 'interpretation_model' folder")
print("=" * 60)

