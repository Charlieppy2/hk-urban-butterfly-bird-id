"""
Flask Backend for Butterfly and Bird Identification System
Handles image upload and model prediction
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import tensorflow as tf
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import gc  # For memory management
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("Warning: OpenCV not available. Some quality analysis features may be limited.")

# Import semantic matcher for description-based identification
try:
    from semantic_matcher import identify_species_semantic, initialize as init_semantic_matcher
    SEMANTIC_MATCHER_AVAILABLE = True
except ImportError:
    SEMANTIC_MATCHER_AVAILABLE = False
    print("Warning: Semantic matcher not available. Using keyword matching.")

app = Flask(__name__)
# Configure CORS to allow all origins (for mobile and web access)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "max_age": 3600
    }
})

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variable for model (will be loaded on startup)
model = None
feature_extractor = None  # Feature extraction model for similarity
class_names = []


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_model():
    """Load the trained model and class names"""
    global model, class_names
    
    # Get the base directory (project root)
    # Try multiple possible paths for different deployment environments
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    working_dir = os.getcwd()
    
    print(f"DEBUG: current_file = {current_file}")
    print(f"DEBUG: current_dir = {current_dir}")
    print(f"DEBUG: working_dir = {working_dir}")
    
    # Try different base directory paths
    possible_base_dirs = [
        # Koyeb: Working directory might be /workspace, need to find project root
        # Check if we're in web_app/backend subdirectory
        os.path.dirname(os.path.dirname(working_dir)) if os.path.basename(working_dir) == 'backend' else None,
        # Check if models exist in working directory
        working_dir if os.path.exists(os.path.join(working_dir, 'models', 'trained', 'model.h5')) else None,
        # Check if models exist one level up
        os.path.dirname(working_dir) if os.path.exists(os.path.join(os.path.dirname(working_dir), 'models', 'trained', 'model.h5')) else None,
        # Check if models exist two levels up
        os.path.dirname(os.path.dirname(working_dir)) if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(working_dir)), 'models', 'trained', 'model.h5')) else None,
        # Check relative to current file location
        os.path.dirname(os.path.dirname(current_dir)) if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'models', 'trained', 'model.h5')) else None,
        # Check three levels up from file
        os.path.dirname(os.path.dirname(os.path.dirname(current_file))) if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_file))), 'models', 'trained', 'model.h5')) else None,
    ]
    
    base_dir = None
    for possible_dir in possible_base_dirs:
        if possible_dir and os.path.exists(possible_dir):
            test_path = os.path.join(possible_dir, 'models', 'trained', 'model.h5')
            print(f"DEBUG: Testing path: {test_path}, exists: {os.path.exists(test_path)}")
            if os.path.exists(test_path):
                base_dir = possible_dir
                print(f"DEBUG: Found model at base_dir: {base_dir}")
                break
    
    # If still not found, search from working directory
    if base_dir is None:
        print(f"DEBUG: Model not found in standard locations, searching from {working_dir}...")
        try:
            for root, dirs, files in os.walk(working_dir):
                if 'models' in dirs:
                    potential_model = os.path.join(root, 'models', 'trained', 'model.h5')
                    if os.path.exists(potential_model):
                        base_dir = root
                        print(f"DEBUG: Found model by walking directory tree: {base_dir}")
                        break
                # Limit search depth to avoid searching entire filesystem
                if root.count(os.sep) - working_dir.count(os.sep) > 3:
                    dirs[:] = []  # Don't descend further
        except Exception as e:
            print(f"DEBUG: Error during directory walk: {e}")
    
    # If still not found, use a default base_dir (but model won't load)
    if base_dir is None:
        # Use working directory as fallback, or go up from current file
        if os.path.basename(working_dir) == 'backend':
            base_dir = os.path.dirname(working_dir)
        else:
            base_dir = os.path.dirname(os.path.dirname(current_dir))
        print(f"DEBUG: Model not found, using fallback base_dir: {base_dir}")
        print(f"DEBUG: WARNING: Model file will not be found at this location!")
    
    model_path = os.path.join(base_dir, 'models', 'trained', 'model.h5')
    class_names_path = os.path.join(base_dir, 'models', 'trained', 'class_names.json')
    
    # Debug: List directory structure
    print(f"Current file: {current_file}")
    print(f"Current directory: {current_dir}")
    print(f"Working directory: {working_dir}")
    print(f"Base directory: {base_dir}")
    print(f"Looking for model at: {model_path}")
    print(f"Model exists: {os.path.exists(model_path)}")
    
    # Debug: Check if base_dir exists and list its contents
    if os.path.exists(base_dir):
        print(f"Base directory exists. Contents: {os.listdir(base_dir)}")
        models_dir = os.path.join(base_dir, 'models')
        if os.path.exists(models_dir):
            print(f"Models directory exists. Contents: {os.listdir(models_dir)}")
            trained_dir = os.path.join(models_dir, 'trained')
            if os.path.exists(trained_dir):
                print(f"Trained directory exists. Contents: {os.listdir(trained_dir)}")
    else:
        print(f"Base directory does not exist: {base_dir}")
        # Try to find models directory from working directory
        print(f"Trying to find models from working directory...")
        for root, dirs, files in os.walk(working_dir):
            if 'models' in dirs:
                print(f"Found models directory at: {os.path.join(root, 'models')}")
                potential_model = os.path.join(root, 'models', 'trained', 'model.h5')
                if os.path.exists(potential_model):
                    print(f"Found model at: {potential_model}")
                    model_path = potential_model
                    class_names_path = os.path.join(root, 'models', 'trained', 'class_names.json')
                    base_dir = root
                    break
    
    if os.path.exists(model_path):
        try:
            model = tf.keras.models.load_model(model_path)
            print(f"Model loaded successfully from {model_path}")
            
            # Create feature extractor model (extract features before final classification layer)
            # This will be used for similarity calculations
            global feature_extractor
            try:
                # Try to get the layer before the final Dense layer
                # For MobileNetV2-based models, this is usually the global average pooling layer
                if len(model.layers) > 1:
                    # Get all layers except the last (classification) layer
                    feature_extractor = tf.keras.Model(
                        inputs=model.input,
                        outputs=model.layers[-2].output  # Second to last layer (before classification)
                    )
                    print(f"Feature extractor created successfully")
                else:
                    # Fallback: use the model itself but extract intermediate features
                    feature_extractor = model
                    print(f"Using model as feature extractor (fallback)")
            except Exception as e:
                print(f"Warning: Could not create feature extractor: {e}")
                feature_extractor = model  # Fallback to using the model itself
        except Exception as e:
            print(f"Error loading model: {e}")
            model = None
            feature_extractor = None
    else:
        print(f"Model not found at {model_path}. Please train the model first.")
    
    if os.path.exists(class_names_path):
        try:
            with open(class_names_path, 'r', encoding='utf-8') as f:
                class_names = json.load(f)
            print(f"Class names loaded: {len(class_names)} classes")
        except Exception as e:
            print(f"Error loading class names: {e}")
            class_names = []


def preprocess_image(image_path, target_size=(224, 224)):
    """Preprocess image for model prediction - Memory optimized"""
    try:
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize image to reduce memory usage
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to array and normalize
        img_array = np.array(img, dtype=np.float32) / 255.0
        
        # Close image to free memory
        img.close()
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None


def extract_features(image_array):
    """Extract feature vector from image using feature extractor model"""
    global feature_extractor
    if feature_extractor is None:
        return None
    
    try:
        features = feature_extractor.predict(image_array, verbose=0)
        # Flatten if needed
        if len(features.shape) > 1:
            features = features.flatten()
        # Normalize features for cosine similarity
        norm = np.linalg.norm(features)
        if norm > 0:
            features = features / norm
        return features
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None


def calculate_similarity(feature1, feature2):
    """Calculate cosine similarity between two feature vectors"""
    try:
        if feature1 is None or feature2 is None:
            return 0.0
        
        # Ensure both are 1D arrays
        feature1 = np.array(feature1).flatten()
        feature2 = np.array(feature2).flatten()
        
        # Normalize
        norm1 = np.linalg.norm(feature1)
        norm2 = np.linalg.norm(feature2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        feature1 = feature1 / norm1
        feature2 = feature2 / norm2
        
        # Cosine similarity
        similarity = np.dot(feature1, feature2)
        return float(similarity)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0


def get_similar_species_from_predictions(predictions_array, top_k=5, exclude_idx=None):
    """Find similar species from already computed predictions - Memory optimized"""
    global class_names
    
    if not class_names:
        return []
    
    try:
        # Use predictions that were already computed (no need to call model.predict again)
        # This saves significant memory
        similarities = []
        for idx in range(len(class_names)):
            # Skip the predicted class itself
            if exclude_idx is not None and idx == exclude_idx:
                continue
            
            # Use prediction probability as similarity score
            similarity_score = float(predictions_array[idx])
            
            # Only include if similarity is above a threshold (0.01 = 1%)
            # Higher threshold to show only truly similar species
            # This reduces noise and improves relevance
            if similarity_score > 0.01:
                similarities.append({
                    'index': idx,
                    'class': class_names[idx] if idx < len(class_names) else f"Class_{idx}",
                    'similarity': similarity_score,
                    'confidence': similarity_score
                })
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Return top K (limit to avoid too many results)
        return similarities[:top_k]
    
    except Exception as e:
        print(f"Error finding similar species: {e}")
        # Return empty list on error to prevent service failure
        return []


def get_similar_species(image_array, top_k=5, exclude_idx=None):
    """Find similar species based on feature vectors - DEPRECATED: Use get_similar_species_from_predictions instead"""
    # This function is kept for backward compatibility but should not be used
    # as it calls model.predict again, wasting memory
    global model, class_names
    
    if model is None or not class_names:
        return []
    
    try:
        # Get predictions for all classes
        predictions = model.predict(image_array, verbose=0, batch_size=1)[0]
        return get_similar_species_from_predictions(predictions, top_k, exclude_idx)
    except Exception as e:
        print(f"Error finding similar species: {e}")
        return []


def is_cartoon_or_illustration(image_path):
    """
    Detect if an image is a cartoon, illustration, or non-photographic image.
    Cartoon/illustration images typically have:
    - High color saturation with uniform regions
    - Very sharp edges (high edge density)
    - Low texture variation (uniform color patches)
    - High contrast between regions
    """
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_array = np.array(img)
        
        if CV2_AVAILABLE:
            # Convert to grayscale for edge detection
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # 1. Edge detection - cartoons have very sharp, clear edges
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
            
            # 2. Color uniformity - cartoons have large uniform color regions
            # Calculate color variance in small patches
            h, w = gray.shape
            patch_size = min(32, h // 8, w // 8)
            patches = []
            for i in range(0, h - patch_size, patch_size):
                for j in range(0, w - patch_size, patch_size):
                    patch = gray[i:i+patch_size, j:j+patch_size]
                    patches.append(np.std(patch))
            texture_variance = np.mean(patches) if patches else 0
            
            # 3. Color saturation - cartoons often have high saturation
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            saturation = np.mean(hsv[:, :, 1]) / 255.0
            
            # 4. Color count - cartoons typically have fewer distinct colors
            # Resize for faster processing
            small_img = cv2.resize(img_array, (100, 100))
            unique_colors = len(np.unique(small_img.reshape(-1, 3), axis=0))
            color_diversity = unique_colors / (100 * 100)  # Normalize
            
            # 5. Color histogram analysis - cartoons have distinct color peaks
            # Calculate histogram for each channel
            hist_b = cv2.calcHist([img_array], [0], None, [256], [0, 256])
            hist_g = cv2.calcHist([img_array], [1], None, [256], [0, 256])
            hist_r = cv2.calcHist([img_array], [2], None, [256], [0, 256])
            # Find peaks in histogram (cartoons have fewer but stronger peaks)
            hist_peaks_b = len([x for x in hist_b if x > np.max(hist_b) * 0.1])
            hist_peaks_g = len([x for x in hist_g if x > np.max(hist_g) * 0.1])
            hist_peaks_r = len([x for x in hist_r if x > np.max(hist_r) * 0.1])
            avg_peaks = (hist_peaks_b + hist_peaks_g + hist_peaks_r) / 3
            # Cartoons typically have fewer histogram peaks (< 30)
            has_cartoon_histogram = avg_peaks < 30
            
            # 6. Gradient analysis - cartoons have sharp transitions
            grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            avg_gradient = np.mean(gradient_magnitude)
            
            # Cartoon detection criteria (more sensitive thresholds):
            # - High edge density (>0.10) AND low texture variance (<30) = cartoon
            # - High saturation (>0.5) AND low color diversity (<0.4) = cartoon
            # - High average gradient (>40) AND low texture variance (<30) = cartoon
            # - Very high saturation (>0.7) = likely cartoon
            # - Very low texture variance (<15) = likely cartoon
            is_cartoon = False
            
            # Debug info (can be removed in production)
            print(f"Cartoon detection: edge_density={edge_density:.3f}, texture_variance={texture_variance:.2f}, "
                  f"saturation={saturation:.3f}, color_diversity={color_diversity:.3f}, avg_gradient={avg_gradient:.2f}, "
                  f"hist_peaks={avg_peaks:.1f}")
            
            # Criterion 1: Sharp edges + uniform texture (lowered thresholds)
            if edge_density > 0.10 and texture_variance < 30:
                is_cartoon = True
                print("  -> Detected by: Sharp edges + uniform texture")
            
            # Criterion 2: High saturation + few colors (lowered thresholds)
            if saturation > 0.5 and color_diversity < 0.4:
                is_cartoon = True
                print("  -> Detected by: High saturation + few colors")
            
            # Criterion 3: High gradient + low texture (lowered thresholds)
            if avg_gradient > 40 and texture_variance < 30:
                is_cartoon = True
                print("  -> Detected by: High gradient + low texture")
            
            # Criterion 4: Very high edge density (typical of line art) (lowered threshold)
            if edge_density > 0.20:
                is_cartoon = True
                print("  -> Detected by: Very high edge density")
            
            # Criterion 5: Very high saturation (typical of cartoon colors)
            if saturation > 0.7:
                is_cartoon = True
                print("  -> Detected by: Very high saturation")
            
            # Criterion 6: Very low texture variance (flat colors typical of cartoons)
            if texture_variance < 15:
                is_cartoon = True
                print("  -> Detected by: Very low texture variance")
            
            # Criterion 7: Low color diversity (cartoons use limited color palette)
            if color_diversity < 0.2:
                is_cartoon = True
                print("  -> Detected by: Very low color diversity")
            
            # Criterion 8: Cartoon-like histogram (few distinct color peaks)
            if has_cartoon_histogram and saturation > 0.5:
                is_cartoon = True
                print("  -> Detected by: Cartoon-like histogram + high saturation")
            
            # Criterion 9: Very high saturation with low texture (typical cartoon combination)
            if saturation > 0.75 and texture_variance < 20:
                is_cartoon = True
                print("  -> Detected by: Very high saturation + low texture")
            
            return is_cartoon
        
        else:
            # Fallback: Simple detection using PIL
            # Convert to grayscale
            gray = np.dot(img_array[...,:3], [0.2989, 0.5870, 0.1140])
            
            # Calculate color variance (texture)
            texture_variance = np.std(gray)
            
            # Calculate saturation
            rgb_max = np.max(img_array, axis=2)
            rgb_min = np.min(img_array, axis=2)
            saturation = np.mean(np.where(rgb_max > 0, (rgb_max - rgb_min) / rgb_max, 0))
            
            print(f"Cartoon detection (fallback): texture_variance={texture_variance:.2f}, saturation={saturation:.3f}")
            
            # Simple heuristic: low texture variance + high saturation = likely cartoon
            # More sensitive thresholds for fallback method
            if texture_variance < 30 and saturation > 0.5:
                print("  -> Detected by: Low texture + high saturation")
                return True
            
            # Also check for very high saturation or very low texture
            if saturation > 0.7 or texture_variance < 15:
                print("  -> Detected by: Very high saturation or very low texture")
                return True
            
            return False
    
    except Exception as e:
        print(f"Error detecting cartoon: {e}")
        return False


def analyze_image_quality(image_path):
    """Analyze image quality and provide recommendations"""
    try:
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_array = np.array(img)
        
        # 1. Brightness analysis
        gray = np.dot(img_array[...,:3], [0.2989, 0.5870, 0.1140])
        brightness = np.mean(gray) / 255.0
        brightness_score = 100 - abs(brightness - 0.5) * 200  # Optimal around 0.5
        
        # 2. Contrast analysis
        contrast = np.std(gray) / 255.0
        contrast_score = min(contrast * 200, 100)  # Higher contrast is better
        
        # 3. Sharpness analysis (using Laplacian variance)
        if CV2_AVAILABLE:
            try:
                gray_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                laplacian_var = cv2.Laplacian(gray_cv, cv2.CV_64F).var()
                # Normalize sharpness (typical range: 0-1000, good: >100)
                sharpness_score = min((laplacian_var / 10), 100)
            except:
                # Fallback calculation using gradient
                gradient = np.gradient(gray.astype(float))
                sharpness_score = min(np.std(gradient[0]) + np.std(gradient[1]), 100)
        else:
            # Fallback calculation using gradient
            gradient = np.gradient(gray.astype(float))
            sharpness_score = min(np.std(gradient[0]) + np.std(gradient[1]), 100)
        
        # 4. Color saturation
        if CV2_AVAILABLE:
            try:
                hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
                saturation = np.mean(hsv[:, :, 1]) / 255.0
            except:
                # Fallback: calculate saturation from RGB
                rgb_max = np.max(img_array, axis=2)
                rgb_min = np.min(img_array, axis=2)
                saturation = np.mean(np.where(rgb_max > 0, (rgb_max - rgb_min) / rgb_max, 0))
        else:
            # Fallback: calculate saturation from RGB
            rgb_max = np.max(img_array, axis=2)
            rgb_min = np.min(img_array, axis=2)
            saturation = np.mean(np.where(rgb_max > 0, (rgb_max - rgb_min) / rgb_max, 0))
        
        saturation_score = saturation * 100
        
        # 5. Image size and resolution
        width, height = img.size
        total_pixels = width * height
        resolution_score = min((total_pixels / (224 * 224)) * 50, 100)  # Optimal at model input size
        
        # 6. Overall quality score
        overall_score = (
            brightness_score * 0.2 +
            contrast_score * 0.25 +
            sharpness_score * 0.3 +
            saturation_score * 0.15 +
            resolution_score * 0.1
        )
        
        # Generate recommendations
        recommendations = []
        
        if brightness < 0.3:
            recommendations.append({
                'type': 'brightness',
                'severity': 'high',
                'message': 'Image is too dark. Try increasing exposure or using better lighting.',
                'suggestion': 'Increase brightness or use flash/brighter lighting'
            })
        elif brightness > 0.7:
            recommendations.append({
                'type': 'brightness',
                'severity': 'medium',
                'message': 'Image is too bright. May lose detail in highlights.',
                'suggestion': 'Reduce exposure or avoid direct sunlight'
            })
        
        if contrast < 0.2:
            recommendations.append({
                'type': 'contrast',
                'severity': 'medium',
                'message': 'Low contrast. Image may appear flat.',
                'suggestion': 'Increase contrast or adjust lighting conditions'
            })
        
        if sharpness_score < 50:
            recommendations.append({
                'type': 'sharpness',
                'severity': 'high',
                'message': 'Image appears blurry. This may affect identification accuracy.',
                'suggestion': 'Hold camera steady, ensure good focus, or get closer to subject'
            })
        
        if saturation_score < 30:
            recommendations.append({
                'type': 'saturation',
                'severity': 'low',
                'message': 'Colors appear muted.',
                'suggestion': 'Image is acceptable but colors could be more vibrant'
            })
        
        if total_pixels < 50000:
            recommendations.append({
                'type': 'resolution',
                'severity': 'medium',
                'message': 'Image resolution is low. Higher resolution improves accuracy.',
                'suggestion': 'Use higher resolution camera settings'
            })
        
        if not recommendations:
            recommendations.append({
                'type': 'quality',
                'severity': 'none',
                'message': 'Image quality is good!',
                'suggestion': 'This image should provide accurate identification results.'
            })
        
        return {
            'overall_score': round(overall_score, 1),
            'metrics': {
                'brightness': {
                    'value': round(brightness * 100, 1),
                    'score': round(brightness_score, 1),
                    'status': 'good' if 0.3 <= brightness <= 0.7 else 'needs_improvement'
                },
                'contrast': {
                    'value': round(contrast * 100, 1),
                    'score': round(contrast_score, 1),
                    'status': 'good' if contrast > 0.2 else 'needs_improvement'
                },
                'sharpness': {
                    'value': round(sharpness_score, 1),
                    'score': round(sharpness_score, 1),
                    'status': 'good' if sharpness_score > 50 else 'needs_improvement'
                },
                'saturation': {
                    'value': round(saturation * 100, 1),
                    'score': round(saturation_score, 1),
                    'status': 'good' if saturation > 0.3 else 'acceptable'
                },
                'resolution': {
                    'width': width,
                    'height': height,
                    'total_pixels': total_pixels,
                    'score': round(resolution_score, 1),
                    'status': 'good' if total_pixels >= 50000 else 'acceptable'
                }
            },
            'recommendations': recommendations
        }
    
    except Exception as e:
        print(f"Error analyzing image quality: {e}")
        return None


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Butterfly and Bird Identification API is running',
        'model_loaded': model is not None
    })


@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict():
    """Handle image prediction request"""
    # Handle preflight OPTIONS request for CORS
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    # Log request info for debugging
    print(f"Predict request from: {request.remote_addr}")
    print(f"User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please train and save the model first.'
        }), 503
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Preprocess image
        processed_image = preprocess_image(filepath)
        
        if processed_image is None:
            return jsonify({'error': 'Failed to process image'}), 500
        
        # Make prediction - use batch_size=1 to reduce memory usage
        predictions = model.predict(processed_image, verbose=0, batch_size=1)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # Get class name
        if class_names and predicted_class_idx < len(class_names):
            predicted_class = class_names[predicted_class_idx]
        else:
            predicted_class = f"Class_{predicted_class_idx}"
        
        # Get top 3 predictions
        top_indices = np.argsort(predictions[0])[-3:][::-1]
        top_predictions = []
        for idx in top_indices:
            if class_names and idx < len(class_names):
                class_name = class_names[idx]
            else:
                class_name = f"Class_{idx}"
            top_predictions.append({
                'class': class_name,
                'confidence': float(predictions[0][idx])
            })
        
        # 檢測是否為非蝴蝶/鳥類圖片
        # 方法0: 優先檢測是否為卡通/插畫圖片（所有卡通圖片都歸類為 others）
        is_cartoon = is_cartoon_or_illustration(filepath)
        is_likely_not_target = is_cartoon
        
        # 方法1: 如果置信度低於30%，可能是其他類型的圖片
        LOW_CONFIDENCE_THRESHOLD = 0.30
        is_likely_not_target = is_likely_not_target or confidence < LOW_CONFIDENCE_THRESHOLD
        
        # 方法2: 計算前3個預測的總置信度，如果都很低，更可能是非目標圖片
        top3_total_confidence = sum(p['confidence'] for p in top_predictions[:3])
        is_likely_not_target = is_likely_not_target or top3_total_confidence < 0.50
        
        # 方法3: 即使置信度高，如果預測的類別不在已知類別列表中，也可能是錯誤識別
        # 檢查預測的類別是否在 class_names 列表中
        if class_names and predicted_class not in class_names:
            is_likely_not_target = True
        
        # 方法4: 如果置信度雖然高（>70%），但前3個預測的類別都不在已知類別列表中，也可能是錯誤識別
        if confidence > 0.70 and class_names:
            all_top3_invalid = all(p['class'] not in class_names for p in top_predictions[:3])
            if all_top3_invalid:
                is_likely_not_target = True
        
        # 方法5: 如果置信度高但前3個預測的總置信度異常低（說明模型不確定），也可能是錯誤識別
        # 例如：置信度92%但前3個總和只有95%（正常應該接近100%）
        # 如果前3個總置信度 < 98%，即使單個置信度高，也可能是錯誤識別
        if confidence > 0.70 and top3_total_confidence < 0.98:
            # 如果最高置信度很高，但前3個總和較低，說明模型可能錯誤地給某個類別很高的分數
            # 這種情況下，即使置信度高，也可能是錯誤識別
            confidence_ratio = confidence / top3_total_confidence if top3_total_confidence > 0 else 1.0
            # 如果最高預測佔了前3個總和的90%以上，且總和 < 98%，可能是錯誤識別
            if confidence_ratio > 0.90:
                is_likely_not_target = True
        
        # 生成警告信息
        warning_message = None
        if is_likely_not_target:
            # 如果是卡通/插畫圖片，使用特殊的警告消息
            if is_cartoon:
                warning_message = {
                    'type': 'cartoon',
                    'title': '⚠️ Cartoon/Illustration Detected',
                    'message': 'This appears to be a cartoon, illustration, or non-photographic image. This system is designed to identify real butterflies and birds from photographs.',
                    'suggestions': [
                        'Please upload a real photograph of a butterfly or bird',
                        'Cartoon or illustrated images cannot be accurately identified',
                        'Try using a clear photo taken with a camera'
                    ],
                    'confidence': confidence,
                    'top3_total_confidence': top3_total_confidence
                }
            else:
                warning_message = {
                    'type': 'low_confidence',
                    'title': '⚠️ Low Identification Confidence',
                    'message': 'This image may not be a butterfly or bird, or the image quality is insufficient for accurate identification.',
                    'suggestions': [
                        'Please ensure you upload a clear photo of a butterfly or bird',
                        'Try taking photos from different angles to ensure the subject is clearly visible',
                        'Ensure the photo has sufficient lighting, avoid blurry or too dark images',
                        'If it is indeed a butterfly or bird, please try taking a clearer photo'
                    ],
                    'confidence': confidence,
                    'top3_total_confidence': top3_total_confidence
                }
        
        # Get similar species - pass predictions to avoid re-computing
        # This saves memory by not calling model.predict again
        # Make a copy of predictions[0] before deleting predictions
        predictions_copy = np.copy(predictions[0])
        similar_species = []
        try:
            similar_species = get_similar_species_from_predictions(predictions_copy, top_k=5, exclude_idx=predicted_class_idx)
            print(f"✅ Similar species found: {len(similar_species)} items")
            if len(similar_species) > 0:
                print(f"   First item: {similar_species[0]}")
            else:
                print(f"   ⚠️ No similar species found (threshold may be too high)")
                print(f"   Top 10 predictions (excluding predicted class):")
                # Show top 10 predictions for debugging
                top_indices = np.argsort(predictions_copy)[-10:][::-1]
                for idx in top_indices:
                    if idx != predicted_class_idx:
                        print(f"      {idx}: {class_names[idx] if idx < len(class_names) else f'Class_{idx}'} = {predictions_copy[idx]:.6f}")
        except Exception as e:
            print(f"❌ Error: Failed to get similar species: {e}")
            import traceback
            traceback.print_exc()
            similar_species = []  # Return empty list on error
        
        # Clear processed_image and predictions from memory immediately
        del processed_image
        del predictions
        del predictions_copy
        gc.collect()
        
        # Clean up uploaded file immediately to save disk space and memory
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Warning: Failed to delete uploaded file: {e}")
        
        # Skip image quality analysis to save memory (causes OOM)
        # Image quality analysis loads the image again, doubling memory usage
        # If needed, users can call /api/analyze-quality endpoint separately
        quality_analysis = None
        
        # Force garbage collection to free memory
        gc.collect()
        
        # Debug: Log similar species before returning
        print(f"Returning {len(similar_species)} similar species")
        if len(similar_species) > 0:
            print(f"First similar species: {similar_species[0]}")
        
        response = jsonify({
            'success': True,
            'prediction': {
                'class': predicted_class,
                'confidence': confidence,
                'top_predictions': top_predictions
            },
            'similar_species': similar_species,
            'image_path': filename,
            'quality_analysis': quality_analysis,
            'warning': warning_message  # 添加警告信息
        })
        
        # Add CORS headers explicitly for mobile devices
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        
        print(f"Prediction successful: {predicted_class} ({confidence:.2%})")
        return response
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error during prediction: {e}")
        print(f"Traceback: {error_trace}")
        
        response = jsonify({
            'error': str(e),
            'message': 'Failed to process prediction. Please try again.'
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check with model status - Fast response for monitoring"""
    try:
        # Quick health check - don't do heavy operations here
        return jsonify({
            'status': 'healthy',
            'model_loaded': model is not None,
            'num_classes': len(class_names) if class_names else 0,
            'message': 'Service is running'
        }), 200
    except Exception as e:
        # Even if there's an error, return a response (not 500)
        # This prevents health check from marking service as unhealthy
        print(f"Health check error: {e}")
        return jsonify({
            'status': 'degraded',
            'model_loaded': False,
            'num_classes': 0,
            'message': 'Service is running but model may not be loaded'
        }), 200


@app.route('/api/classes', methods=['GET'])
def get_classes():
    """Get list of all class names"""
    return jsonify({
        'classes': class_names if class_names else []
    })


@app.route('/api/analyze-quality', methods=['POST'])
def analyze_quality():
    """Analyze image quality without prediction"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP'}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"quality_{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze quality
        quality_analysis = analyze_image_quality(filepath)
        
        if quality_analysis is None:
            return jsonify({'error': 'Failed to analyze image quality'}), 500
        
        # Clean up
        # os.remove(filepath)
        
        return jsonify(quality_analysis)
    
    except Exception as e:
        print(f"Error in analyze_quality: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['POST'])
def get_statistics():
    """Calculate statistics from identification history"""
    try:
        data = request.get_json()
        history = data.get('history', [])
        
        if not history:
            return jsonify({
                'error': 'No history data provided'
            }), 400
        
        # Calculate statistics
        total_identifications = len(history)
        
        # Species frequency
        species_count = {}
        confidence_sum = {}
        for item in history:
            if 'prediction' in item and 'class' in item['prediction']:
                species = item['prediction']['class']
                confidence = item['prediction'].get('confidence', 0)
                
                species_count[species] = species_count.get(species, 0) + 1
                confidence_sum[species] = confidence_sum.get(species, 0) + confidence
        
        # Top species
        top_species = sorted(species_count.items(), key=lambda x: x[1], reverse=True)[:10]
        top_species_list = [{'species': s, 'count': c, 'avg_confidence': (confidence_sum[s] / c * 100) if c > 0 else 0} 
                           for s, c in top_species]
        
        # Average confidence
        all_confidences = [item['prediction'].get('confidence', 0) * 100 
                          for item in history if 'prediction' in item]
        avg_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0
        
        # Confidence distribution
        high_confidence = sum(1 for c in all_confidences if c >= 90)
        medium_confidence = sum(1 for c in all_confidences if 70 <= c < 90)
        low_confidence = sum(1 for c in all_confidences if c < 70)
        
        # Time-based statistics (if timestamps available)
        time_stats = {}
        for item in history:
            if 'timestamp' in item:
                # Extract date from timestamp
                try:
                    date_str = item['timestamp'].split(',')[0]  # Get date part
                    time_stats[date_str] = time_stats.get(date_str, 0) + 1
                except:
                    pass
        
        # Bird vs Butterfly classification
        bird_count = 0
        butterfly_count = 0
        
        # Get class names to determine category by index
        # Use the same logic as load_model() to find base directory
        current_file = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file)
        working_dir = os.getcwd()
        
        # Try to find base directory (same logic as load_model)
        if 'backend' in working_dir:
            base_dir = os.path.dirname(os.path.dirname(working_dir))
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        
        class_names_path = os.path.join(base_dir, 'models', 'trained', 'class_names.json')
        class_names_list = []
        if os.path.exists(class_names_path):
            try:
                with open(class_names_path, 'r', encoding='utf-8') as f:
                    class_names_list = json.load(f)
            except:
                pass
        
        for item in history:
            # 如果檢測到非蝴蝶/鳥類圖片（有 warning），直接歸類為 others
            if 'warning' in item and item['warning'] is not None:
                # 跳過，讓它歸類到 others（通過計算 total - bird_count - butterfly_count）
                continue
            
            if 'prediction' in item:
                species = item['prediction'].get('class', '')
                species_lower = species.lower()
                
                # Method 1: Check if species name starts with number (001-200 are birds)
                if species and species[0].isdigit():
                    bird_count += 1
                    continue
                
                # Method 2: Check index in class_names list (first 200 are birds, rest are butterflies/moths)
                if class_names_list:
                    try:
                        species_index = class_names_list.index(species)
                        if species_index < 200:  # First 200 are birds
                            bird_count += 1
                            continue
                        else:  # Rest are butterflies/moths
                            butterfly_count += 1
                            continue
                    except ValueError:
                        pass  # Species not found in list, try keyword matching
                
                # Method 3: Fallback to keyword matching
                bird_keywords = ['bird', 'albatross', 'auklet', 'blackbird', 'bunting', 'crow', 'finch', 'gull', 'hummingbird', 'jay', 'kingfisher', 'lark', 'loon', 'merganser', 'nuthatch', 'oriole', 'pelican', 'raven', 'shrike', 'sparrow', 'starling', 'swallow', 'tanager', 'tern', 'thrasher', 'vireo', 'warbler', 'waterthrush', 'waxwing', 'woodpecker', 'wren', 'yellowthroat']
                butterfly_keywords = ['butterfly', 'moth', 'swallowtail', 'pansy', 'tiger', 'morpho', 'monarch', 'admiral', 'hairstreak', 'skipper', 'sulphur', 'copper', 'elfin', 'pierrot', 'comma', 'white', 'blue', 'orange', 'red', 'yellow', 'peacock', 'lady', 'cabbage', 'painted', 'wood-nymph', 'argus', 'eggfly', 'brown', 'green', 'purple', 'malachite', 'metalmark', 'tortoiseshell', 'mourning', 'cloak', 'question', 'mark', 'cracker', 'postman', 'leafwing', 'popinjay', 'ulyses', 'viceroy', 'satyr', 'zebra', 'long', 'wing', 'banded', 'heliconian', 'birdwing', 'atlas', 'luna', 'polyphemus', 'io', 'hercules', 'emperor', 'gum', 'cinnabar', 'garden', 'tiger', 'clearwing', 'arcigera', 'flower', 'sixspot', 'burnet', 'white', 'lined', 'sphinx', 'oleander', 'hawk', 'humming', 'bird', 'hawk', 'moth', 'madagascan', 'sunset', 'comet', 'rosy', 'maple', 'giant', 'leopard', 'banded', 'tiger', 'bird', 'cherry', 'ermine', 'adonis', 'apollo', 'atala', 'beckers', 'chalk', 'hill', 'checquered', 'chestnut', 'cleopatra', 'clodius', 'parnassian', 'clouded', 'common', 'copper', 'tail', 'crescent', 'crimson', 'patch', 'danaid', 'eastern', 'dapple', 'eastern', 'pine', 'elbowed', 'glittering', 'sapphire', 'gold', 'great', 'green', 'celled', 'cattleheart', 'grey', 'indra', 'julia', 'large', 'marble', 'mestra', 'milberts', 'orange', 'oakleaf', 'paper', 'kite', 'pine', 'pipevine', 'purple', 'hairstreak', 'purplish', 'scarce', 'silver', 'spot', 'sleepy', 'sootywing', 'southern', 'dogface', 'straited', 'queen', 'tropical', 'two', 'barred', 'flasher', 'wood', 'yellow']
                
                if any(keyword in species_lower for keyword in bird_keywords):
                    bird_count += 1
                elif any(keyword in species_lower for keyword in butterfly_keywords):
                    butterfly_count += 1
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_identifications': total_identifications,
                'unique_species': len(species_count),
                'average_confidence': round(avg_confidence, 2),
                'top_species': top_species_list,
                'confidence_distribution': {
                    'high': high_confidence,
                    'medium': medium_confidence,
                    'low': low_confidence
                },
                'category_distribution': {
                    'birds': bird_count,
                    'butterflies': butterfly_count,
                    'others': total_identifications - bird_count - butterfly_count
                },
                'time_distribution': dict(sorted(time_stats.items(), reverse=True)[:7])  # Last 7 days
            }
        })
    
    except Exception as e:
        print(f"Error calculating statistics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/birds', methods=['GET'])
def get_birds():
    """Get all bird species information"""
    try:
        bird_info_path = os.path.join(os.path.dirname(__file__), 'bird_info_template.json')
        if os.path.exists(bird_info_path):
            with open(bird_info_path, 'r', encoding='utf-8') as f:
                bird_data = json.load(f)
            print(f"✅ Loaded {len(bird_data)} bird species from {bird_info_path}")
            return jsonify({
                'status': 'success',
                'birds': bird_data,
                'total': len(bird_data)
            })
        else:
            print(f"❌ Bird info file not found at: {bird_info_path}")
            return jsonify({
                'status': 'error',
                'message': 'Bird information file not found'
            }), 404
    except Exception as e:
        print(f"❌ Error loading birds: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/butterflies', methods=['GET'])
def get_butterflies():
    """Get all butterfly/moth species information"""
    try:
        butterfly_info_path = os.path.join(os.path.dirname(__file__), 'butterfly_info_template.json')
        if os.path.exists(butterfly_info_path):
            with open(butterfly_info_path, 'r', encoding='utf-8') as f:
                butterfly_data = json.load(f)
            print(f"✅ Loaded {len(butterfly_data)} butterfly/moth species from {butterfly_info_path}")
            return jsonify({
                'status': 'success',
                'butterflies': butterfly_data,
                'total': len(butterfly_data)
            })
        else:
            print(f"❌ Butterfly info file not found at: {butterfly_info_path}")
            return jsonify({
                'status': 'error',
                'message': 'Butterfly information file not found'
            }), 404
    except Exception as e:
        print(f"❌ Error loading butterflies: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/species-image/<path:image_path>', methods=['GET'])
def get_species_image(image_path):
    """Serve species images from the data directory"""
    try:
        # Get base directory (project root)
        current_file = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file)
        base_dir = os.path.dirname(os.path.dirname(current_dir))
        
        # Construct full image path
        # image_path comes as URL-encoded, decode it
        import urllib.parse
        decoded_path = urllib.parse.unquote(image_path)
        
        # Debug logging
        print(f"Image request (raw): {image_path}")
        print(f"Image request (decoded): {decoded_path}")
        print(f"Base dir: {base_dir}")
        
        # Handle relative paths (starting with ../, ./ or ..%2F)
        # Also handle URL-encoded paths
        if decoded_path.startswith('../') or decoded_path.startswith('..%2F'):
            # Remove ../ or ..%2F prefix and construct full path
            clean_path = decoded_path.replace('../', '').replace('..%2F', '')
            full_path = os.path.join(base_dir, clean_path)
        elif decoded_path.startswith('./'):
            # Handle paths starting with ./ (may come from URL encoding issues)
            clean_path = decoded_path.replace('./', '')
            full_path = os.path.join(base_dir, clean_path)
        elif decoded_path.startswith('data/'):
            # Handle paths starting with data/
            full_path = os.path.join(base_dir, decoded_path)
        elif decoded_path.startswith('/'):
            # Handle absolute paths (remove leading slash)
            full_path = os.path.join(base_dir, decoded_path.lstrip('/'))
        else:
            # Path relative to base_dir
            full_path = os.path.join(base_dir, decoded_path)
        
        # Additional check: if path contains %2F (encoded /), decode it
        if '%2F' in full_path:
            full_path = urllib.parse.unquote(full_path)
        
        # Additional check: handle any remaining encoded characters
        if '%' in full_path:
            full_path = urllib.parse.unquote(full_path)
        
        # Normalize path to prevent directory traversal attacks
        full_path = os.path.normpath(full_path)
        base_dir = os.path.normpath(base_dir)
        
        print(f"🔍 Full path: {full_path}")
        print(f"🔍 File exists: {os.path.exists(full_path)}")
        
        # Security check: ensure the path is within base_dir
        if not full_path.startswith(base_dir):
            print(f"❌ Security check failed: {full_path} not in {base_dir}")
            return jsonify({'status': 'error', 'message': 'Invalid image path'}), 403
        
        # Check if file exists
        if not os.path.exists(full_path):
            print(f"❌ Image not found: {full_path}")
            # Try alternative paths
            alt_paths = [
                full_path.replace('\\', '/'),
                full_path.replace('/', '\\'),
                # Try with web_app/backend prefix removed
                os.path.join(base_dir, 'data', 'raw', os.path.basename(os.path.dirname(decoded_path)), os.path.basename(decoded_path)) if '/' in decoded_path else None,
            ]
            for alt_path in alt_paths:
                if alt_path and os.path.exists(alt_path):
                    print(f"✅ Found alternative path: {alt_path}")
                    full_path = alt_path
                    break
            else:
                # If image doesn't exist, return a placeholder or 404
                # For now, return 404 but log the issue
                print(f"⚠️ Image file not found in deployment. This is expected if data/raw is not included in deployment.")
                print(f"   Expected path: {full_path}")
                print(f"   Base dir contents: {os.listdir(base_dir) if os.path.exists(base_dir) else 'N/A'}")
                if os.path.exists(os.path.join(base_dir, 'data')):
                    print(f"   Data dir exists: {os.listdir(os.path.join(base_dir, 'data'))}")
                return jsonify({
                    'status': 'error', 
                    'message': 'Image not available in deployment. Images are stored locally and not included in the deployment package.'
                }), 404
        
        # Send the image file
        directory = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        print(f"✅ Serving image: {filename} from {directory}")
        return send_from_directory(directory, filename)
    except Exception as e:
        print(f"❌ Error serving image: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """AI Chat Assistant endpoint - Supports Chinese input but always responds in English"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()  # Keep original case for Chinese detection
        context = data.get('context', {})
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Generate response (supports Chinese input, always responds in English)
        response = generate_chat_response(message, context)
        
        return jsonify({
            'response': response,  # Always in English
            'success': True
        })
    
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({'error': str(e)}), 500


def generate_chat_response(message, context):
    """Generate response based on user message - Supports Chinese input but always responds in English"""
    import random
    import re
    
    # Load knowledge base
    knowledge_base_path = os.path.join(os.path.dirname(__file__), 'knowledge_base.json')
    knowledge_base = {}
    
    if os.path.exists(knowledge_base_path):
        try:
            with open(knowledge_base_path, 'r', encoding='utf-8') as f:
                knowledge_base = json.load(f)
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
    
    # Detect if message contains Chinese characters
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', message))
    
    # Try to match against knowledge base (works for both English and Chinese)
    message_lower = message.lower()
    
    # Check each category in knowledge base
    best_match = None
    best_score = 0
    
    for category, data in knowledge_base.items():
        if category == 'default':
            continue
            
        patterns = data.get('patterns', [])
        responses = data.get('responses', [])
        
        # Calculate match score (works for both English and Chinese patterns)
        score = sum(1 for pattern in patterns if pattern in message_lower)
        
        if score > best_score and responses:
            best_score = score
            best_match = (category, responses)
    
    # If we found a good match, use it (responses are always in English)
    if best_match and best_score > 0:
        _, responses = best_match
        response = random.choice(responses)
        # Ensure response is in English (add note if Chinese was detected)
        if has_chinese:
            # Response is already in English, but we can add a note if needed
            pass
        return response
    
    # Fallback to default responses (always in English)
    if 'default' in knowledge_base and knowledge_base['default'].get('responses'):
        return random.choice(knowledge_base['default']['responses'])
    
    # Original hardcoded responses as fallback (always in English)
    return generate_fallback_response(message, context)


def generate_fallback_response(message, context):
    """Fallback response generator (original logic)"""
    
    # Help
    if any(word in message for word in ['help', 'what can you do', 'capabilities']):
        return """I can help you with:
• Species information and characteristics
• Identification tips and techniques
• Best practices for observation
• Understanding identification results
• Questions about butterflies and birds

Just ask me anything!"""
    
    # Identification tips
    if any(word in message for word in ['how to identify', 'identification tips', 'how to tell', 'distinguish']):
        return """Here are some identification tips:

For Butterflies:
• Look at wing patterns, colors, and markings
• Check wing shape and size
• Observe body color and antennae
• Note the habitat and time of day

For Birds:
• Observe size, shape, and posture
• Check beak shape and color
• Look at plumage patterns and colors
• Note behavior and habitat
• Listen to calls if possible

Take clear photos from multiple angles for better identification!"""
    
    # Best time to observe
    if any(word in message for word in ['when', 'best time', 'season', 'time of day']):
        return """Best times for observation:

Butterflies:
• Morning (9-11 AM) when they're most active
• Sunny days are ideal
• Spring and summer are peak seasons
• Avoid windy or rainy days

Birds:
• Early morning (6-9 AM) for most activity
• Late afternoon (4-6 PM) for feeding
• Migration seasons (spring/autumn) offer more variety
• Different species are active at different times"""
    
    # Camera/photo tips
    if any(word in message for word in ['photo', 'camera', 'picture', 'image quality', 'how to take']):
        return """Tips for better photos:

1. Get close but don't disturb the subject
2. Ensure good lighting (natural light is best)
3. Focus on the subject, blur the background
4. Take multiple shots from different angles
5. Make sure the subject fills the frame
6. Avoid shadows on the subject
7. Keep the camera steady

For identification, clear photos showing key features are essential!"""
    
    # About the system
    if any(word in message for word in ['system', 'model', 'accuracy', 'how does it work']):
        return """This system uses:
• Deep learning (MobileNetV2) for image classification
• Transfer learning trained on 300+ species
• Can identify butterflies and birds from photos
• Provides confidence scores and top predictions

The model analyzes image features to match against known species. Higher confidence scores indicate more reliable identifications."""
    
    # Species information
    if any(word in message for word in ['species', 'types', 'kinds', 'varieties']):
        return f"""Our system can identify:
• 200+ bird species
• 100+ butterfly species
• Total: {len(class_names) if class_names else 300}+ species

All species are commonly found in various environments. Upload a photo to get started!"""
    
    # Confidence/accuracy questions
    if any(word in message for word in ['confidence', 'accurate', 'reliable', 'trust']):
        return """About confidence scores:

• 90%+: Very high confidence, likely correct
• 70-90%: High confidence, probably correct
• 50-70%: Moderate confidence, check top predictions
• Below 50%: Low confidence, may need better photo

Always check the top 3 predictions to see alternatives. Multiple photos from different angles improve accuracy!"""
    
    # Habitat questions
    if any(word in message for word in ['where', 'habitat', 'location', 'find', 'spot']):
        return """Where to find species:

Butterflies:
• Country parks and nature reserves
• Gardens and parks with flowers
• Forest edges and clearings
• Near water sources

Birds:
• Urban parks and gardens
• Country parks and woodlands
• Wetlands and coastal areas
• Residential areas with trees

Many species adapt well to urban environments!"""
    
    # Check if asking about last prediction
    last_prediction = context.get('lastPrediction')
    if last_prediction and any(word in message for word in ['this', 'that', 'it', 'result', 'identification']):
        species = last_prediction.get('class', '')
        confidence = last_prediction.get('confidence', 0)
        
        if species:
            return f"""About your identification result:

Species: {species}
Confidence: {(confidence * 100):.1f}%

This is a {'very reliable' if confidence > 0.9 else 'reliable' if confidence > 0.7 else 'moderate' if confidence > 0.5 else 'uncertain'} identification. 

{'Great photo! The model is very confident about this identification.' if confidence > 0.9 else 'Consider taking additional photos from different angles for confirmation.' if confidence < 0.7 else 'The identification looks good, but you may want to verify with field guides.'}"""
    
    # Default response
    return """I'm here to help with butterfly and bird identification! 

You can ask me about:
• Identification tips
• Best times to observe
• Photo-taking advice
• Species information
• Understanding your results

What would you like to know?"""


# ============================================
# Text Description Based Species Identification
# ============================================

def load_species_database():
    """Load all species data for text-based identification"""
    species_db = {'birds': {}, 'butterflies': {}}
    
    # Load bird data
    bird_info_path = os.path.join(os.path.dirname(__file__), 'bird_info_template.json')
    if os.path.exists(bird_info_path):
        try:
            with open(bird_info_path, 'r', encoding='utf-8') as f:
                species_db['birds'] = json.load(f)
        except Exception as e:
            print(f"Error loading bird data: {e}")
    
    # Load butterfly data
    butterfly_info_path = os.path.join(os.path.dirname(__file__), 'butterfly_info_template.json')
    if os.path.exists(butterfly_info_path):
        try:
            with open(butterfly_info_path, 'r', encoding='utf-8') as f:
                species_db['butterflies'] = json.load(f)
        except Exception as e:
            print(f"Error loading butterfly data: {e}")
    
    return species_db


def calculate_match_score(description, species_info):
    """Calculate how well a description matches a species"""
    import re
    
    description_lower = description.lower()
    score = 0
    matched_fields = []
    
    # Define field weights
    field_weights = {
        'description': 3,
        'habitat': 2,
        'distribution': 2,
        'behavior': 2,
        'diet': 1.5,
        'size': 1,
        'wingspan': 1,
        'lifecycle': 1,
        'common_name': 2,
        'scientific_name': 1.5
    }
    
    # Extract keywords from description (remove common words)
    stop_words = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
                  'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
                  'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'whom', 'whose',
                  'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
                  'most', 'other', 'some', 'such', 'no', 'not', 'only', 'own', 'same', 'so',
                  'than', 'too', 'very', 'just', 'about', 'with', 'from', 'into', 'through',
                  'during', 'before', 'after', 'above', 'below', 'between', 'under', 'over',
                  'and', 'or', 'but', 'if', 'because', 'as', 'until', 'while', 'of', 'at',
                  'by', 'for', 'on', 'off', 'out', 'in', 'to', 'up'}
    
    # Extract meaningful keywords from user description
    words = re.findall(r'\b[a-zA-Z]{3,}\b', description_lower)
    keywords = [w for w in words if w not in stop_words]
    
    # Check each field for keyword matches
    for field, weight in field_weights.items():
        if field in species_info and species_info[field]:
            field_text = str(species_info[field]).lower()
            field_match_count = 0
            
            for keyword in keywords:
                if keyword in field_text:
                    field_match_count += 1
            
            if field_match_count > 0:
                field_score = field_match_count * weight
                score += field_score
                matched_fields.append({
                    'field': field,
                    'matches': field_match_count,
                    'score': field_score
                })
    
    return score, matched_fields


def identify_by_description(description, category=None, conversation_history=None):
    """
    Identify species based on text description.
    Uses semantic matching (if available) or falls back to keyword matching.
    Returns matches and follow-up questions if needed.
    """
    
    # Try semantic matching first (more accurate)
    if SEMANTIC_MATCHER_AVAILABLE:
        try:
            semantic_result = identify_species_semantic(description, category, conversation_history)
            if semantic_result is not None:
                # Convert semantic results to standard format
                species_db = load_species_database()
                formatted_matches = []
                
                for match in semantic_result.get('matches', []):
                    species_key = match.get('species_key', '')
                    species_info = match.get('species_info', {})
                    
                    # Get full species info from database
                    full_info = None
                    species_type = species_info.get('type', 'unknown')
                    
                    # STRICT CATEGORY FILTERING - Skip if category doesn't match
                    if category:
                        if category.lower() in ['bird', 'birds'] and species_type != 'bird':
                            continue  # Skip non-birds when user wants birds
                        if category.lower() in ['butterfly', 'butterflies'] and species_type != 'butterfly':
                            continue  # Skip non-butterflies when user wants butterflies
                    
                    if species_type == 'bird':
                        full_info = species_db.get('birds', {}).get(species_key)
                    elif species_type == 'butterfly':
                        full_info = species_db.get('butterflies', {}).get(species_key)
                    
                    if not full_info:
                        # Try both databases
                        full_info = species_db.get('birds', {}).get(species_key) or \
                                   species_db.get('butterflies', {}).get(species_key)
                    
                    if full_info:
                        formatted_matches.append({
                            'common_name': full_info.get('common_name', species_key),
                            'scientific_name': full_info.get('scientific_name', ''),
                            'description': full_info.get('description', ''),
                            'habitat': full_info.get('habitat', ''),
                            'distribution': full_info.get('distribution', ''),
                            'behavior': full_info.get('behavior', ''),
                            'size': full_info.get('size', full_info.get('wingspan', '')),
                            'category': 'Bird' if species_type == 'bird' else 'Butterfly/Moth',
                            'confidence_score': match.get('confidence', 0.5),
                            'image_path': full_info.get('image_path', ''),
                            'matched_fields': ['semantic_match'],
                            'match_method': 'semantic'
                        })
                
                return {
                    'matches': formatted_matches,
                    'needs_clarification': semantic_result.get('needs_more_info', False),
                    'follow_up_questions': semantic_result.get('follow_up_questions', [])[:3],
                    'total_searched': 300,  # Total species count
                    'match_method': 'semantic'
                }
        except Exception as e:
            print(f"Semantic matching failed, falling back to keyword: {e}")
    
    # Fallback to keyword matching
    species_db = load_species_database()
    
    # Determine which categories to search
    categories_to_search = []
    if category == 'bird' or category == 'birds':
        categories_to_search = ['birds']
    elif category == 'butterfly' or category == 'butterflies':
        categories_to_search = ['butterflies']
    else:
        categories_to_search = ['birds', 'butterflies']
    
    all_matches = []
    
    for cat in categories_to_search:
        for species_key, species_info in species_db.get(cat, {}).items():
            score, matched_fields = calculate_match_score(description, species_info)
            if score > 0:
                all_matches.append({
                    'species_key': species_key,
                    'species_info': species_info,
                    'category': cat,
                    'score': score,
                    'matched_fields': matched_fields
                })
    
    # Sort by score
    all_matches.sort(key=lambda x: x['score'], reverse=True)
    
    # Take top matches
    top_matches = all_matches[:5]
    
    # Determine if we need follow-up questions
    needs_clarification = False
    follow_up_questions = []
    
    if len(top_matches) == 0:
        needs_clarification = True
        follow_up_questions = [
            "I couldn't find a good match. Could you provide more details?",
            "What colors does it have?",
            "Where did you see it (habitat)?",
            "What size is it approximately?",
            "What behavior did you observe?"
        ]
    elif len(top_matches) >= 2 and top_matches[0]['score'] < top_matches[1]['score'] * 1.5:
        # Top matches are close in score, need clarification
        needs_clarification = True
        
        # Generate targeted questions based on what differentiates the top matches
        top_species = top_matches[:3]
        
        # Find differentiating features
        habitats = set()
        distributions = set()
        sizes = set()
        colors = set()
        
        for match in top_species:
            info = match['species_info']
            if info.get('habitat'):
                habitats.add(info['habitat'][:50])
            if info.get('distribution'):
                distributions.add(info['distribution'][:50])
            if info.get('size') or info.get('wingspan'):
                sizes.add(info.get('size', info.get('wingspan', ''))[:30])
        
        if len(habitats) > 1:
            follow_up_questions.append(f"What type of habitat was it in? (e.g., {', '.join(list(habitats)[:2])})")
        if len(distributions) > 1:
            follow_up_questions.append(f"What region/area did you see it in?")
        if len(sizes) > 1:
            follow_up_questions.append(f"What size was it approximately?")
        
        follow_up_questions.append("Can you describe any distinctive markings or patterns?")
        follow_up_questions.append("What colors did you notice?")
    
    # Format top matches for response
    formatted_matches = []
    for match in top_matches:
        info = match['species_info']
        formatted_matches.append({
            'common_name': info.get('common_name', match['species_key']),
            'scientific_name': info.get('scientific_name', ''),
            'description': info.get('description', ''),
            'habitat': info.get('habitat', ''),
            'distribution': info.get('distribution', ''),
            'behavior': info.get('behavior', ''),
            'size': info.get('size', info.get('wingspan', '')),
            'category': 'Bird' if match['category'] == 'birds' else 'Butterfly/Moth',
            'confidence_score': min(match['score'] / 10, 1.0),  # Normalize to 0-1
            'image_path': info.get('image_path', ''),
            'matched_fields': match['matched_fields'],
            'match_method': 'keyword'
        })
    
    return {
        'matches': formatted_matches,
        'needs_clarification': needs_clarification,
        'follow_up_questions': follow_up_questions[:3] if follow_up_questions else [],
        'total_searched': sum(len(species_db.get(cat, {})) for cat in categories_to_search),
        'match_method': 'keyword'
    }


@app.route('/api/identify-by-description', methods=['POST'])
def identify_species_by_description():
    """
    API endpoint for text-based species identification.
    Accepts description and optional category, returns matching species.
    """
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        category = data.get('category', None)  # 'bird', 'butterfly', or None for both
        conversation_history = data.get('conversation_history', [])
        
        if not description:
            return jsonify({
                'error': 'Description is required',
                'success': False
            }), 400
        
        if len(description) < 5:
            return jsonify({
                'error': 'Please provide a more detailed description (at least 5 characters)',
                'success': False
            }), 400
        
        # Perform identification
        result = identify_by_description(description, category, conversation_history)
        
        # Generate response message
        if result['matches']:
            if result['needs_clarification']:
                message = f"I found {len(result['matches'])} possible matches, but I'd like to narrow it down. "
                if result['follow_up_questions']:
                    message += result['follow_up_questions'][0]
            else:
                top_match = result['matches'][0]
                confidence = top_match['confidence_score']
                if confidence > 0.8:
                    message = f"Based on your description, this is most likely a **{top_match['common_name']}** ({top_match['category']})."
                else:
                    message = f"Based on your description, this could be a **{top_match['common_name']}** ({top_match['category']}), but I'm not entirely certain."
        else:
            message = "I couldn't find a good match for your description. Could you provide more details about the species you're trying to identify?"
        
        return jsonify({
            'success': True,
            'message': message,
            'matches': result['matches'],
            'needs_clarification': result['needs_clarification'],
            'follow_up_questions': result['follow_up_questions'],
            'total_species_searched': result['total_searched']
        })
    
    except Exception as e:
        print(f"Error in identify_species_by_description: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/description-chat', methods=['POST'])
def description_chat():
    """
    Interactive chat for species identification by description.
    Maintains conversation context and progressively narrows down matches.
    """
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        conversation_history = data.get('conversation_history', [])
        current_matches = data.get('current_matches', [])  # Previous matches to narrow down
        category = data.get('category', None)
        
        if not message:
            return jsonify({
                'error': 'Message is required',
                'success': False
            }), 400
        
        # Build full description from conversation history
        full_description = ' '.join([
            msg.get('content', '') 
            for msg in conversation_history 
            if msg.get('role') == 'user'
        ])
        full_description += ' ' + message
        
        # Detect category from conversation if not explicitly set
        detected_category = category
        if not detected_category:
            # Check if user mentioned bird or butterfly in any message
            full_text_lower = full_description.lower()
            if 'bird' in full_text_lower and 'butterfly' not in full_text_lower:
                detected_category = 'bird'
            elif 'butterfly' in full_text_lower and 'bird' not in full_text_lower:
                detected_category = 'butterfly'
            elif 'moth' in full_text_lower:
                detected_category = 'butterfly'
        
        # If we have previous matches, extract the category from them
        inferred_category = None
        if current_matches and len(current_matches) > 0:
            # Get categories from previous matches
            prev_categories = set()
            for m in current_matches:
                cat = m.get('category', '')
                if 'Bird' in cat:
                    prev_categories.add('bird')
                elif 'Butterfly' in cat or 'Moth' in cat:
                    prev_categories.add('butterfly')
            
            # If all previous matches were one category, stick with it
            if len(prev_categories) == 1:
                inferred_category = list(prev_categories)[0]
        
        # Use inferred category if no explicit category and we have previous context
        effective_category = detected_category or inferred_category
        
        # Perform identification with accumulated description
        result = identify_by_description(full_description, effective_category, conversation_history)
        
        # If we have previous matches, narrow down to those that still match
        if current_matches and len(current_matches) > 0:
            previous_names = set(m.get('common_name', '').lower() for m in current_matches)
            
            # Also get the category of previous matches for strict filtering
            prev_category_type = None
            if inferred_category:
                prev_category_type = inferred_category
            
            # Filter new results to prioritize species from previous matches
            refined_matches = []
            same_category_matches = []
            
            for match in result['matches']:
                match_name = match.get('common_name', '').lower()
                match_category = match.get('category', '')
                
                # Check if it's the same category as previous matches
                is_same_category = False
                if prev_category_type == 'bird' and 'Bird' in match_category:
                    is_same_category = True
                elif prev_category_type == 'butterfly' and ('Butterfly' in match_category or 'Moth' in match_category):
                    is_same_category = True
                
                if match_name in previous_names:
                    # This species was in previous results - highest priority
                    refined_matches.append(match)
                elif is_same_category:
                    # Same category but different species - second priority
                    same_category_matches.append(match)
            
            # Use refined matches if available, otherwise same-category matches
            if refined_matches:
                result['matches'] = refined_matches
                result['narrowed_down'] = True
            elif same_category_matches:
                # No exact overlap, but stay within the same category
                result['matches'] = same_category_matches[:5]
                result['narrowed_down'] = False
                result['stayed_in_category'] = True
            # If neither, keep the original results (category might have changed)
        
        # Generate appropriate response
        if result['matches']:
            top_match = result['matches'][0]
            num_matches = len(result['matches'])
            
            # Check if we've narrowed down significantly
            was_narrowed = result.get('narrowed_down', False)
            
            if num_matches == 1 or (
                num_matches >= 2 and 
                result['matches'][0]['confidence_score'] > result['matches'][1]['confidence_score'] * 1.5
            ):
                # High confidence single match
                confidence_pct = int(top_match['confidence_score'] * 100)
                response_text = f"""🎯 Based on all the information you've provided, I'm {confidence_pct}% confident this is:

**{top_match['common_name']}** ({top_match['scientific_name']})

**Category:** {top_match['category']}
**Description:** {top_match['description'][:200]}...

**Habitat:** {top_match['habitat']}
**Distribution:** {top_match['distribution']}

Is this the species you were looking for? If not, please tell me what's different."""
                needs_more_info = False
            elif num_matches <= 3:
                # Few candidates left - getting closer!
                if was_narrowed:
                    response_text = f"✨ Great! I've narrowed it down to {num_matches} possibilities:\n\n"
                else:
                    response_text = f"I found {num_matches} possible matches:\n\n"
                
                for i, match in enumerate(result['matches'][:3], 1):
                    conf = int(match['confidence_score'] * 100)
                    response_text += f"{i}. **{match['common_name']}** ({match['category']}) - {conf}% match\n"
                    response_text += f"   _{match['description'][:80]}..._\n\n"
                
                if result.get('follow_up_questions'):
                    response_text += f"\n💡 To help me narrow it down further: {result['follow_up_questions'][0]}"
                needs_more_info = True
            else:
                # Multiple possible matches
                if was_narrowed:
                    response_text = f"📋 Narrowed down from previous results. Still have {num_matches} possibilities:\n\n"
                else:
                    response_text = f"📋 I found {num_matches} possible matches:\n\n"
                
                for i, match in enumerate(result['matches'][:3], 1):
                    conf = int(match['confidence_score'] * 100)
                    response_text += f"{i}. **{match['common_name']}** ({match['category']}) - {conf}% match\n"
                
                if result.get('follow_up_questions'):
                    response_text += f"\n💡 To help me identify it more precisely: {result['follow_up_questions'][0]}"
                needs_more_info = True
        else:
            response_text = """I'm having trouble finding a match. Could you describe:
- What colors did you see?
- Was it large or small?
- Where exactly did you see it (forest, garden, water, etc.)?
- What was it doing (flying, perching, feeding)?"""
            needs_more_info = True
        
        return jsonify({
            'success': True,
            'response': response_text,
            'matches': result['matches'],
            'needs_more_info': needs_more_info,
            'follow_up_questions': result['follow_up_questions']
        })
    
    except Exception as e:
        print(f"Error in description_chat: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


if __name__ == '__main__':
    print("Loading model...")
    load_model()
    print("Starting Flask server...")
    # Get port from environment variable or default to 5001
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)

