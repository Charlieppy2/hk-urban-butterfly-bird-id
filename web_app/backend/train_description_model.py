#!/usr/bin/env python3
"""
Training script for Description-based Species Identification Model

This script uses Sentence Transformers to create semantic embeddings for all species,
enabling accurate text-based identification based on user descriptions.

Usage:
    python train_description_model.py

Output:
    - models/description_embeddings.npz (species embeddings)
    - models/species_index.json (species name index)
"""

import json
import os
import numpy as np
from pathlib import Path

# Check if sentence_transformers is available
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("⚠️ sentence-transformers not installed. Install with: pip install sentence-transformers")

def load_species_data():
    """Load all species data from JSON files."""
    current_dir = Path(__file__).parent
    
    # Load bird data
    bird_file = current_dir / 'bird_info_template.json'
    butterfly_file = current_dir / 'butterfly_info_template.json'
    
    all_species = {}
    
    if bird_file.exists():
        with open(bird_file, 'r', encoding='utf-8') as f:
            birds = json.load(f)
            for key, data in birds.items():
                data['type'] = 'bird'
                all_species[key] = data
        print(f"✅ Loaded {len(birds)} bird species")
    
    if butterfly_file.exists():
        with open(butterfly_file, 'r', encoding='utf-8') as f:
            butterflies = json.load(f)
            for key, data in butterflies.items():
                data['type'] = 'butterfly'
                all_species[key] = data
        print(f"✅ Loaded {len(butterflies)} butterfly species")
    
    return all_species


def extract_colors(text):
    """Extract color words from text."""
    color_keywords = [
        'black', 'white', 'brown', 'red', 'blue', 'green', 'yellow', 
        'orange', 'purple', 'grey', 'gray', 'golden', 'silver', 'dark', 
        'light', 'bright', 'pale', 'iridescent', 'spotted', 'striped',
        'pink', 'crimson', 'scarlet', 'azure', 'turquoise', 'teal',
        'cream', 'buff', 'tan', 'chestnut', 'rusty', 'cinnamon',
        'violet', 'indigo', 'navy', 'cobalt', 'cerulean', 'sapphire',
        'emerald', 'lime', 'olive', 'chartreuse', 'magenta', 'coral',
        'bronze', 'copper', 'metallic', 'glossy', 'matte', 'dusky'
    ]
    text_lower = text.lower()
    found_colors = []
    for color in color_keywords:
        if color in text_lower:
            found_colors.append(color)
    return found_colors


def create_species_descriptions(species_data):
    """
    Create comprehensive text descriptions for each species.
    Combines multiple fields to create rich descriptions for embedding.
    Enhanced with more color-focused variants for better color matching.
    """
    descriptions = []
    species_keys = []
    species_info = []
    
    for key, data in species_data.items():
        # Create multiple description variants for better matching
        common_name = data.get('common_name', key)
        scientific_name = data.get('scientific_name', '')
        description = data.get('description', '')
        habitat = data.get('habitat', '')
        distribution = data.get('distribution', '')
        behavior = data.get('behavior', '')
        diet = data.get('diet', '')
        size = data.get('size', data.get('wingspan', ''))
        species_type = data.get('type', 'unknown')
        
        # Extract colors from description
        colors = extract_colors(description)
        color_str = ' and '.join(colors) if colors else 'colorful'
        
        # Store complete info for filtering (including description for color matching)
        info_dict = {
            'key': key,
            'common_name': common_name,
            'scientific_name': scientific_name,
            'type': species_type,
            'image_path': data.get('image_path', ''),
            'colors': colors,  # Store extracted colors
            'description': description  # Store description for color matching
        }
        
        # Primary description: comprehensive
        primary_desc = f"{common_name}. {description} Habitat: {habitat}. Found in: {distribution}. Behavior: {behavior}. Diet: {diet}. Size: {size}."
        
        # Color-focused descriptions (MULTIPLE variants for better color matching)
        color_desc1 = f"A {color_str} {species_type} called {common_name}. {description}"
        color_desc2 = f"{common_name} is a {species_type} with {color_str} coloring. {description}"
        color_desc3 = f"This {species_type} has {color_str} colors: {common_name}. {description}"
        
        # If specific colors found, create even more specific descriptions
        if colors:
            for color in colors[:3]:  # Top 3 colors
                color_specific = f"A {color} {species_type} - {common_name}. {description}"
                descriptions.append(color_specific)
                species_keys.append(key)
                species_info.append(info_dict.copy())
        
        # Habitat-focused description
        habitat_desc = f"A {species_type} found in {habitat}. {distribution}. {common_name}. {description}"
        
        # Behavior-focused description
        behavior_desc = f"{common_name}: {behavior}. {diet}. {description}"
        
        # Size-focused description
        size_desc = f"{common_name} with size {size}. {description}"
        
        # Combined query-like descriptions (simulate user queries)
        query_desc1 = f"small {color_str} {species_type} in {habitat}"
        query_desc2 = f"{color_str} {species_type} with {size} found near {habitat}"
        query_desc3 = f"I saw a {color_str} {species_type} - {common_name}"
        
        # Add all variants
        all_descs = [
            primary_desc, 
            color_desc1, color_desc2, color_desc3,
            habitat_desc, behavior_desc, size_desc,
            query_desc1, query_desc2, query_desc3
        ]
        
        for desc in all_descs:
            if desc.strip():
                descriptions.append(desc)
                species_keys.append(key)
                species_info.append(info_dict.copy())
    
    return descriptions, species_keys, species_info


def train_embeddings(model_name='all-MiniLM-L6-v2'):
    """
    Generate embeddings for all species descriptions using Sentence Transformers.
    
    Args:
        model_name: The Sentence Transformer model to use.
                   Options: 'all-MiniLM-L6-v2' (fast), 'all-mpnet-base-v2' (accurate)
    """
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        print("❌ Cannot train: sentence-transformers not installed")
        print("   Install with: pip install sentence-transformers")
        return False
    
    print(f"\n🚀 Training Description Model using {model_name}")
    print("=" * 60)
    
    # Load species data
    print("\n📖 Loading species data...")
    species_data = load_species_data()
    
    if not species_data:
        print("❌ No species data found!")
        return False
    
    # Create descriptions
    print("\n📝 Creating species descriptions...")
    descriptions, species_keys, species_info = create_species_descriptions(species_data)
    print(f"   Created {len(descriptions)} description variants for {len(species_data)} species")
    
    # Load model
    print(f"\n🤖 Loading Sentence Transformer model: {model_name}")
    print("   (This may take a moment on first run...)")
    model = SentenceTransformer(model_name)
    
    # Generate embeddings
    print("\n⚙️ Generating embeddings...")
    embeddings = model.encode(
        descriptions, 
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True  # For cosine similarity
    )
    
    print(f"   Embeddings shape: {embeddings.shape}")
    
    # Create output directory
    output_dir = Path(__file__).parent.parent.parent / 'models' / 'description'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save embeddings
    embeddings_file = output_dir / 'species_embeddings.npz'
    np.savez_compressed(
        embeddings_file,
        embeddings=embeddings,
        species_keys=np.array(species_keys, dtype=object)
    )
    print(f"\n💾 Saved embeddings to: {embeddings_file}")
    
    # Save species index (for lookup)
    index_file = output_dir / 'species_index.json'
    
    # Create unique species index
    unique_species = {}
    for info in species_info:
        key = info['key']
        if key not in unique_species:
            unique_species[key] = info
    
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump({
            'model_name': model_name,
            'num_species': len(unique_species),
            'num_embeddings': len(embeddings),
            'embedding_dim': embeddings.shape[1],
            'species': unique_species
        }, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved species index to: {index_file}")
    
    # Also save descriptions for reference
    desc_file = output_dir / 'descriptions.json'
    with open(desc_file, 'w', encoding='utf-8') as f:
        json.dump({
            'descriptions': descriptions,
            'species_keys': species_keys
        }, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved descriptions to: {desc_file}")
    
    print("\n" + "=" * 60)
    print("✅ Training complete!")
    print(f"   Total species: {len(unique_species)}")
    print(f"   Total embeddings: {len(embeddings)}")
    print(f"   Embedding dimension: {embeddings.shape[1]}")
    print("\n📁 Output files:")
    print(f"   - {embeddings_file}")
    print(f"   - {index_file}")
    print(f"   - {desc_file}")
    
    return True


def test_model():
    """Test the trained model with sample queries."""
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        print("❌ Cannot test: sentence-transformers not installed")
        return
    
    output_dir = Path(__file__).parent.parent.parent / 'models' / 'description'
    embeddings_file = output_dir / 'species_embeddings.npz'
    index_file = output_dir / 'species_index.json'
    
    if not embeddings_file.exists():
        print("❌ Model not trained yet. Run training first.")
        return
    
    print("\n🧪 Testing trained model...")
    print("=" * 60)
    
    # Load model and embeddings
    with open(index_file, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    model = SentenceTransformer(index_data['model_name'])
    
    data = np.load(embeddings_file, allow_pickle=True)
    embeddings = data['embeddings']
    species_keys = data['species_keys']
    
    # Test queries
    test_queries = [
        "small blue butterfly with orange spots in grasslands",
        "large black seabird with long wingspan over ocean",
        "red bird with black mask found in gardens",
        "yellow and black butterfly with long tail",
        "small brown bird that makes a nest in trees"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        
        # Encode query
        query_embedding = model.encode([query], normalize_embeddings=True)
        
        # Calculate similarities
        similarities = np.dot(embeddings, query_embedding.T).flatten()
        
        # Get top 3 matches
        top_indices = np.argsort(similarities)[-3:][::-1]
        
        print("   Top matches:")
        for i, idx in enumerate(top_indices):
            species_key = species_keys[idx]
            score = similarities[idx]
            species_name = index_data['species'].get(species_key, {}).get('common_name', species_key)
            print(f"   {i+1}. {species_name} (score: {score:.4f})")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Train Description-based Species Identification Model')
    parser.add_argument('--model', type=str, default='all-MiniLM-L6-v2',
                       help='Sentence Transformer model name')
    parser.add_argument('--test', action='store_true',
                       help='Test the trained model')
    
    args = parser.parse_args()
    
    if args.test:
        test_model()
    else:
        success = train_embeddings(args.model)
        if success:
            test_model()

