"""
Semantic Matcher for Description-based Species Identification

This module provides semantic similarity matching using Sentence Transformers.
Falls back to keyword matching if the model is not available.
"""

import os
import json
import numpy as np
from pathlib import Path

# Global variables for caching
_model = None
_embeddings = None
_species_keys = None
_species_index = None
_is_initialized = False
_use_semantic = False


def get_model_path():
    """Get the path to the trained model files."""
    current_dir = Path(__file__).parent
    # First try local path (same directory as this file)
    local_model_dir = current_dir / 'description_model'
    if local_model_dir.exists():
        return local_model_dir
    # Fallback to original path (for local development)
    model_dir = current_dir.parent.parent / 'models' / 'description'
    return model_dir


def is_model_available():
    """Check if the trained model files exist."""
    model_dir = get_model_path()
    embeddings_file = model_dir / 'species_embeddings.npz'
    index_file = model_dir / 'species_index.json'
    print(f"DEBUG: Checking model at: {model_dir}")
    print(f"DEBUG: Embeddings file exists: {embeddings_file.exists()}")
    print(f"DEBUG: Index file exists: {index_file.exists()}")
    return embeddings_file.exists() and index_file.exists()


def initialize():
    """Initialize the semantic matcher."""
    global _model, _embeddings, _species_keys, _species_index, _is_initialized, _use_semantic
    
    if _is_initialized:
        return _use_semantic
    
    _is_initialized = True
    
    # Check if model files exist
    if not is_model_available():
        print("⚠️ Semantic model not found. Using keyword matching.")
        print("   To enable semantic matching, run: python train_description_model.py")
        _use_semantic = False
        return False
    
    # Try to load sentence-transformers
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("⚠️ sentence-transformers not installed. Using keyword matching.")
        print("   Install with: pip install sentence-transformers")
        _use_semantic = False
        return False
    
    try:
        model_dir = get_model_path()
        
        # Load species index
        index_file = model_dir / 'species_index.json'
        with open(index_file, 'r', encoding='utf-8') as f:
            _species_index = json.load(f)
        
        # Load embeddings
        embeddings_file = model_dir / 'species_embeddings.npz'
        data = np.load(embeddings_file, allow_pickle=True)
        _embeddings = data['embeddings']
        _species_keys = data['species_keys']
        
        # Load model
        model_name = _species_index.get('model_name', 'all-MiniLM-L6-v2')
        print(f"🤖 Loading Sentence Transformer model: {model_name}")
        _model = SentenceTransformer(model_name)
        
        print(f"✅ Semantic matcher initialized with {len(_species_index['species'])} species")
        _use_semantic = True
        return True
        
    except Exception as e:
        print(f"⚠️ Failed to load semantic model: {e}")
        print("   Falling back to keyword matching.")
        _use_semantic = False
        return False


def extract_colors_from_query(query):
    """Extract color words from user query."""
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
    query_lower = query.lower()
    found_colors = []
    for color in color_keywords:
        if color in query_lower:
            found_colors.append(color)
    return found_colors


def check_color_match(query_colors, species_description):
    """Check if species description contains the query colors."""
    if not query_colors:
        return True, 1.0  # No color requirement
    
    if not species_description:
        return False, 0.0
    
    desc_lower = species_description.lower()
    matched_colors = 0
    
    for color in query_colors:
        if color in desc_lower:
            matched_colors += 1
    
    if matched_colors == 0:
        return False, 0.0
    
    match_ratio = matched_colors / len(query_colors)
    return True, match_ratio


def semantic_search(query, category=None, top_k=5):
    """
    Perform semantic search to find matching species.
    Enhanced with color filtering for better accuracy.
    
    Args:
        query: User's description of the species
        category: Optional filter ('bird', 'butterfly', or None for all)
        top_k: Number of top matches to return
    
    Returns:
        List of matches with scores and species info
    """
    global _model, _embeddings, _species_keys, _species_index
    
    if not _use_semantic or _model is None:
        return None  # Signal to fall back to keyword matching
    
    try:
        # Extract colors from query for filtering
        query_colors = extract_colors_from_query(query)
        
        # Encode the query
        query_embedding = _model.encode([query], normalize_embeddings=True)
        
        # Calculate similarities
        similarities = np.dot(_embeddings, query_embedding.T).flatten()
        
        # Get indices sorted by similarity (highest first)
        sorted_indices = np.argsort(similarities)[::-1]
        
        # Collect unique species (since we have multiple embeddings per species)
        seen_species = set()
        matches = []
        color_matched = []  # Store color-matched results separately
        
        for idx in sorted_indices:
            if len(matches) >= top_k * 4:  # Get more initially for filtering
                break
                
            species_key = str(_species_keys[idx])
            
            # Skip if already seen
            if species_key in seen_species:
                continue
            seen_species.add(species_key)
            
            # Get species info
            species_info = _species_index['species'].get(species_key, {})
            species_type = species_info.get('type', 'unknown')
            
            # Filter by category if specified
            if category:
                if category.lower() in ['bird', 'birds'] and species_type != 'bird':
                    continue
                if category.lower() in ['butterfly', 'butterflies'] and species_type != 'butterfly':
                    continue
            
            score = float(similarities[idx])
            
            # Only include if similarity is above threshold
            if score > 0.1:  # Minimum threshold
                match_entry = {
                    'species_key': species_key,
                    'score': score,
                    'confidence': min(score * 1.5, 1.0),  # Scale to 0-1
                    'species_info': species_info
                }
                
                # Check color matching if user specified colors
                if query_colors:
                    # Get species colors from stored info or description
                    species_colors = species_info.get('colors', [])
                    species_desc = species_info.get('description', '')
                    
                    # Check if any query color matches
                    has_color_match, color_ratio = check_color_match(query_colors, species_desc)
                    
                    if has_color_match and color_ratio > 0:
                        # Boost score for color matches
                        match_entry['score'] = score * (1 + color_ratio * 0.5)
                        match_entry['confidence'] = min(match_entry['score'] * 1.5, 1.0)
                        match_entry['color_match'] = True
                        match_entry['color_ratio'] = color_ratio
                        color_matched.append(match_entry)
                    else:
                        match_entry['color_match'] = False
                        matches.append(match_entry)
                else:
                    matches.append(match_entry)
        
        # Prioritize color-matched results
        if query_colors and color_matched:
            # Sort color matches by score
            color_matched.sort(key=lambda x: x['score'], reverse=True)
            # Combine: color matches first, then others
            final_results = color_matched + matches
        else:
            final_results = matches
        
        # Take top_k matches
        return final_results[:top_k]
        
    except Exception as e:
        print(f"Error in semantic search: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_follow_up_questions(matches, original_query):
    """
    Generate intelligent follow-up questions based on matched species.
    
    Args:
        matches: List of matched species
        original_query: The user's original query
    
    Returns:
        List of follow-up questions
    """
    questions = []
    
    if not matches or len(matches) == 0:
        return [
            "I couldn't find a good match. Could you describe what colors you saw?",
            "What was the size of the creature?",
            "Where did you see it? (forest, garden, water, etc.)",
            "What was its behavior? (flying, perching, feeding, etc.)"
        ]
    
    if len(matches) == 1:
        return []  # High confidence match, no questions needed
    
    # Analyze differences between top matches
    top_matches = matches[:3]
    
    # Check if they differ in habitat
    habitats = set()
    distributions = set()
    types = set()
    
    for match in top_matches:
        info = match.get('species_info', {})
        # We might need to load full species info
        if info.get('habitat'):
            habitats.add(info['habitat'][:50] if len(info['habitat']) > 50 else info['habitat'])
        if info.get('distribution'):
            distributions.add(info['distribution'][:50] if len(info['distribution']) > 50 else info['distribution'])
        types.add(info.get('type', 'unknown'))
    
    # Generate targeted questions
    if len(types) > 1:
        questions.append("Is this a bird or a butterfly/moth?")
    
    if len(habitats) > 1 and 'habitat' not in original_query.lower():
        questions.append("What type of habitat was it in? (forest, grassland, water, urban, etc.)")
    
    if len(distributions) > 1 and not any(word in original_query.lower() for word in ['asia', 'europe', 'america', 'africa', 'found', 'region']):
        questions.append("What region or country did you see it in?")
    
    if 'color' not in original_query.lower() and 'colour' not in original_query.lower():
        questions.append("Can you describe any distinctive colors or patterns?")
    
    if 'size' not in original_query.lower() and 'large' not in original_query.lower() and 'small' not in original_query.lower():
        questions.append("What size was it approximately?")
    
    # Limit to 3 questions
    return questions[:3]


def identify_species_semantic(description, category=None, conversation_history=None):
    """
    Main identification function using semantic matching.
    
    Args:
        description: Full description text
        category: Optional filter ('bird', 'butterfly', or None)
        conversation_history: Previous messages in the conversation
    
    Returns:
        Dictionary with matches, follow_up_questions, and metadata
    """
    # Initialize if not already done
    initialize()
    
    # Try semantic search
    matches = semantic_search(description, category)
    
    if matches is None:
        # Semantic search not available, return None to signal fallback
        return None
    
    # Generate follow-up questions
    follow_up_questions = get_follow_up_questions(matches, description)
    
    # Determine if we need more information
    needs_more_info = len(matches) == 0 or (
        len(matches) >= 2 and 
        matches[0]['confidence'] < 0.7 and
        matches[0]['confidence'] < matches[1]['confidence'] * 1.5
    )
    
    return {
        'matches': matches,
        'follow_up_questions': follow_up_questions,
        'needs_more_info': needs_more_info,
        'method': 'semantic'
    }

