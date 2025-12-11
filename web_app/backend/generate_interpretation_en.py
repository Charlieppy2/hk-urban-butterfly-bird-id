"""
Inference Module: Generate Interpretation Text
Uses English-only inputs and outputs

Usage:
    from generate_interpretation_en import InterpretationGenerator
    
    generator = InterpretationGenerator('models/interpretation_model')
    result = generator.generate("Taiwan Blue Magpie", "fun_fact")
"""

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os
import json

class InterpretationGenerator:
    """Interpretation text generator"""
    
    def __init__(self, model_path='models/interpretation_model', device='cpu'):
        """
        Initialize generator
        
        Args:
            model_path: Path to trained model
            device: Device to run on
        """
        self.device = torch.device(device)
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.loaded = False
        
        # Load species name mapping
        self.species_mapping = self._load_species_mapping()
    
    def _load_species_mapping(self):
        """Load Chinese to English species name mapping"""
        mapping_path = 'species_name_mapping.json'
        if os.path.exists(mapping_path):
            with open(mapping_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _convert_species_name(self, species):
        """Convert Chinese species name to English"""
        return self.species_mapping.get(species, species)
    
    def load_model(self):
        """Load trained model"""
        if self.loaded:
            return True
        
        if not os.path.exists(self.model_path):
            print(f"⚠️ Model path does not exist: {self.model_path}")
            print("💡 Please train the model first or check the model path")
            return False
        
        try:
            print(f"📥 Loading model: {self.model_path}")
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_path)
            self.model = GPT2LMHeadModel.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            self.loaded = True
            print(f"✅ Model loaded successfully (device: {self.device})")
            return True
        except Exception as e:
            print(f"❌ Model loading failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate(
        self,
        species,
        category,
        max_length=256,
        temperature=0.7,
        top_p=0.9,
        num_return_sequences=1
    ):
        """
        Generate interpretation text
        
        Args:
            species: Species name (Chinese or English)
            category: Category (e.g., "fun_fact", "behavior", "habitat")
            max_length: Maximum generation length
            temperature: Temperature parameter (controls randomness)
            top_p: Nucleus sampling parameter (controls diversity)
            num_return_sequences: Number of sequences to generate
        
        Returns:
            generated_text: Generated interpretation text in English, None if failed
        """
        if not self.loaded:
            if not self.load_model():
                return None
        
        try:
            # Convert species name to English if needed
            species_en = self._convert_species_name(species)
            
            # Build input text (same format as training)
            input_text = f"Species: {species_en}, Category: {category}, Interpretation:"
            
            # Encode input
            input_ids = self.tokenizer.encode(input_text, return_tensors='pt').to(self.device)
            
            # Generate text
            with torch.no_grad():
                output = self.model.generate(
                    input_ids=input_ids,
                    max_length=max_length,
                    num_return_sequences=num_return_sequences,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.2
                )
            
            # Decode generated text
            generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
            
            # Remove input part, keep only generated part
            generated_text = generated_text.replace(input_text, "").strip()
            
            # Clean text (remove special characters and extra spaces)
            generated_text = generated_text.replace("\n", " ").strip()
            
            return generated_text
            
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None

# Global generator instance (singleton pattern)
_global_generator = None

def get_generator(model_path='models/interpretation_model', device='cpu'):
    """
    Get global generator instance (singleton pattern)
    
    Args:
        model_path: Model path
        device: Device
    
    Returns:
        generator: Generator instance
    """
    global _global_generator
    
    if _global_generator is None:
        _global_generator = InterpretationGenerator(model_path, device)
        _global_generator.load_model()
    
    return _global_generator

if __name__ == "__main__":
    # Test generation
    print("=" * 60)
    print("🧪 Testing Interpretation Text Generation")
    print("=" * 60)
    
    # Create generator
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    generator = InterpretationGenerator(
        model_path='models/interpretation_model',
        device=device
    )
    
    # Test generation: Taiwan Blue Magpie fun_fact
    print("\n📝 Test: Taiwan Blue Magpie - fun_fact")
    print("-" * 60)
    
    result = generator.generate(
        species="Taiwan Blue Magpie",  # Can also use "臺灣藍鵲"
        category="fun_fact",
        max_length=256,
        temperature=0.7
    )
    
    if result:
        print(f"✅ Generation successful:")
        print(f"{result}")
    else:
        print("❌ Generation failed (model may not be trained yet)")
        print("💡 Tip: Run train_model.py to train the model first")

