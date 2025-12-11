"""
Training Script for Interpretation Generation Model
Uses English GPT-2 model with English-only inputs

Usage:
    python train_model.py
"""

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

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

class InterpretationDataset(Dataset):
    """Dataset class for loading and processing training data"""
    
    def __init__(self, csv_path, tokenizer, max_length=256):
        """
        Initialize dataset
        
        Args:
            csv_path: Path to CSV file
            tokenizer: Tokenizer
            max_length: Maximum sequence length
        """
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Read CSV data
        df = pd.read_csv(csv_path)
        self.data = df.to_dict('records')
        
        print(f"✅ Loaded {len(self.data)} training samples")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        """
        Get one data sample
        
        Returns:
            input_ids: Input IDs
            attention_mask: Attention mask
            labels: Labels (for loss calculation)
        """
        item = self.data[idx]
        
        # Build input: species (English) + category + interpretation
        species_en = item['species_en']
        category = item['category']
        interpretation = item['interpretation_text']
        
        # Input format: "Species: {species_en}, Category: {category}, Interpretation: {interpretation}"
        # This format helps the model understand the structure better
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
            
            # Calculate valid token count (excluding padding)
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
    
    # Randomly select samples for evaluation
    sample_indices = np.random.choice(len(test_data), min(num_samples, len(test_data)), replace=False)
    
    with torch.no_grad():
        for idx in sample_indices:
            item = test_data[idx]
            species_en = item['species_en']
            category = item['category']
            reference = item['interpretation_text']
            
            # Generate text
            input_text = f"Species: {species_en}, Category: {category}, Interpretation:"
            input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
            
            # Generate
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
            
            # Decode generated text
            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
            # Remove input part, keep only generated part
            generated_text = generated_text.replace(input_text, "").strip()
            
            # Calculate BLEU score
            reference_tokens = reference.split()
            generated_tokens = generated_text.split()
            
            try:
                bleu = sentence_bleu([reference_tokens], generated_tokens, smoothing_function=smoothing)
                bleu_scores.append(bleu)
            except:
                pass
    
    avg_bleu = np.mean(bleu_scores) if bleu_scores else 0.0
    return avg_bleu

def load_model_and_tokenizer(device='cpu'):
    """Load GPT-2 model and tokenizer"""
    print("🔄 Loading model and tokenizer...")
    
    # Use English GPT-2 model
    model_name = "gpt2"
    print(f"📥 Loading model from Hugging Face: {model_name}")
    
    try:
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)
        
        # Set pad_token (GPT-2 doesn't have pad_token by default)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Move model to device
        model = model.to(device)
        model.train()  # Set to training mode
        
        print(f"✅ Model and tokenizer loaded successfully (device: {device})")
        print(f"   Model parameters: {sum(p.numel() for p in model.parameters()):,}")
        
        return model, tokenizer
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise

def train_model(
    csv_path='training_data_interpretation_en.csv',
    output_dir='models/interpretation_model',
    num_epochs=10,
    batch_size=4,
    learning_rate=5e-5,
    max_length=256,
    warmup_steps=50
):
    """
    Main training function
    
    Args:
        csv_path: Path to training data CSV
        output_dir: Directory to save model
        num_epochs: Number of training epochs
        batch_size: Batch size
        learning_rate: Learning rate
        max_length: Maximum sequence length
        warmup_steps: Number of warmup steps
    """
    print("=" * 60)
    print("🚀 Starting Interpretation Generation Model Training")
    print("=" * 60)
    
    # 1. Load model and tokenizer
    print("\n📥 Step 1: Loading pretrained model...")
    model, tokenizer = load_model_and_tokenizer(device=device)
    
    # 2. Prepare dataset
    print("\n📊 Step 2: Preparing dataset...")
    dataset = InterpretationDataset(csv_path, tokenizer, max_length=max_length)
    
    # Split into train and validation (80/20)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    print(f"   Training set: {len(train_dataset)} samples")
    print(f"   Validation set: {len(val_dataset)} samples")
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # 3. Setup optimizer and learning rate scheduler
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
        for batch_idx, batch in enumerate(progress_bar):
            # Move data to device
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            # Forward pass
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # Gradient clipping
            optimizer.step()
            scheduler.step()
            
            total_train_loss += loss.item()
            
            # Update progress bar
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
                
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                
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
            
            # Save training history
            with open(os.path.join(output_dir, 'training_history.json'), 'w', encoding='utf-8') as f:
                json.dump(training_history, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print("✅ Training completed!")
    print(f"{'='*60}")
    print(f"📁 Model saved to: {output_dir}")
    print(f"📊 Best validation loss: {best_val_loss:.4f}")

if __name__ == "__main__":
    # Training parameters
    train_model(
        csv_path='training_data_interpretation_en.csv',
        output_dir='models/interpretation_model',
        num_epochs=10,  # Increased epochs
        batch_size=4,
        learning_rate=5e-5,
        max_length=256,
        warmup_steps=50
    )

