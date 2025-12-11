"""
Train Intent Classification Model for AI Assistant
This model classifies user questions into different intent categories
"""

import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
from collections import Counter

# Intent categories based on knowledge base
INTENT_CATEGORIES = [
    'greetings',
    'identification_tips',
    'observation_time',
    'photo_tips',
    'species_info',
    'confidence',
    'habitat',
    'system_info',
    'help',
    'default'
]

def load_training_data(knowledge_base_path='knowledge_base.json'):
    """Load training data from knowledge base"""
    if not os.path.exists(knowledge_base_path):
        print(f"❌ Knowledge base not found: {knowledge_base_path}")
        return None, None
    
    with open(knowledge_base_path, 'r', encoding='utf-8') as f:
        knowledge_base = json.load(f)
    
    texts = []
    labels = []
    
    # Extract patterns and their categories
    for category, data in knowledge_base.items():
        if category == 'default':
            continue
        
        patterns = data.get('patterns', [])
        for pattern in patterns:
            texts.append(pattern.lower())
            labels.append(category)
    
    # Add default examples if needed
    if 'default' in knowledge_base:
        default_patterns = [
            'hello', 'hi', 'help', 'what can you do',
            '你好', '幫助', '能做什麼'
        ]
        for pattern in default_patterns:
            texts.append(pattern.lower())
            labels.append('default')
    
    return texts, labels

def create_synthetic_training_data():
    """Create synthetic training data for better coverage"""
    synthetic_data = {
        'greetings': [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon',
            '你好', '嗨', '早晨', '午安', '哈囉'
        ],
        'identification_tips': [
            'how to identify', 'identification tips', 'how to tell',
            'distinguish', 'recognize', '如何識別', '辨識', '識別',
            '怎麼分辨', '如何分辨', '辨別', '識別技巧'
        ],
        'observation_time': [
            'when', 'best time', 'season', 'time of day',
            '什麼時候', '最佳時間', '季節', '時間'
        ],
        'photo_tips': [
            'photo', 'camera', 'picture', 'image quality', 'how to take',
            '拍照', '攝影', '照片', '圖像質量', '如何拍攝'
        ],
        'species_info': [
            'species', 'types', 'kinds', 'varieties', 'information',
            '物種', '種類', '類型', '信息'
        ],
        'confidence': [
            'confidence', 'accurate', 'reliable', 'trust', 'accuracy',
            '置信度', '準確', '可靠', '信任'
        ],
        'habitat': [
            'where', 'habitat', 'location', 'find', 'spot',
            '哪裡', '棲息地', '位置', '找到', '地點'
        ],
        'system_info': [
            'system', 'model', 'accuracy', 'how does it work',
            '系統', '模型', '準確度', '如何工作'
        ],
        'help': [
            'help', 'what can you do', 'capabilities', 'assist',
            '幫助', '能做什麼', '功能', '協助'
        ],
        'default': [
            'thanks', 'thank you', 'ok', 'okay', 'yes', 'no',
            '謝謝', '感謝', '好的', '是', '否'
        ]
    }
    
    texts = []
    labels = []
    
    for category, patterns in synthetic_data.items():
        for pattern in patterns:
            texts.append(pattern.lower())
            labels.append(category)
    
    return texts, labels

def train_model(texts, labels, model_type='naive_bayes'):
    """Train intent classification model"""
    if len(texts) == 0 or len(labels) == 0:
        print("❌ No training data available")
        return None, None
    
    print(f"📊 Training data: {len(texts)} examples")
    print(f"📊 Categories: {Counter(labels)}")
    
    # Vectorize text
    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),  # Unigrams and bigrams
        stop_words='english',
        min_df=1,
        max_df=0.95
    )
    
    X = vectorizer.fit_transform(texts)
    y = np.array(labels)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    if model_type == 'naive_bayes':
        model = MultinomialNB(alpha=0.1)
    elif model_type == 'logistic':
        model = LogisticRegression(max_iter=1000, random_state=42)
    else:
        model = MultinomialNB(alpha=0.1)
    
    print(f"🔄 Training {model_type} model...")
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Model trained successfully!")
    print(f"📊 Accuracy: {accuracy:.2%}")
    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=INTENT_CATEGORIES))
    
    return model, vectorizer

def save_model(model, vectorizer, model_path='intent_classifier_model.pkl', 
               vectorizer_path='intent_vectorizer.pkl'):
    """Save trained model and vectorizer"""
    try:
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"✅ Model saved to: {model_path}")
        
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(vectorizer, f)
        print(f"✅ Vectorizer saved to: {vectorizer_path}")
        
        return True
    except Exception as e:
        print(f"❌ Error saving model: {e}")
        return False

def load_model(model_path='intent_classifier_model.pkl',
               vectorizer_path='intent_vectorizer.pkl'):
    """Load trained model and vectorizer"""
    try:
        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            return None, None
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        
        print(f"✅ Model loaded from: {model_path}")
        return model, vectorizer
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None, None

def predict_intent(model, vectorizer, text):
    """Predict intent for a given text"""
    if model is None or vectorizer is None:
        return 'default', 0.0
    
    try:
        text_vectorized = vectorizer.transform([text.lower()])
        prediction = model.predict(text_vectorized)[0]
        probabilities = model.predict_proba(text_vectorized)[0]
        confidence = max(probabilities)
        
        return prediction, confidence
    except Exception as e:
        print(f"⚠️ Error in prediction: {e}")
        return 'default', 0.0

def main():
    """Main training function"""
    print("=" * 60)
    print("🤖 Training Intent Classification Model for AI Assistant")
    print("=" * 60)
    
    # Load training data
    print("\n1️⃣ Loading training data...")
    texts, labels = load_training_data()
    
    if texts is None or len(texts) == 0:
        print("⚠️ No data from knowledge base, using synthetic data...")
        texts, labels = create_synthetic_training_data()
    
    # Add synthetic data for better coverage
    synthetic_texts, synthetic_labels = create_synthetic_training_data()
    texts.extend(synthetic_texts)
    labels.extend(synthetic_labels)
    
    print(f"✅ Loaded {len(texts)} training examples")
    
    # Train model
    print("\n2️⃣ Training model...")
    model, vectorizer = train_model(texts, labels, model_type='naive_bayes')
    
    if model is None:
        print("❌ Training failed")
        return
    
    # Save model
    print("\n3️⃣ Saving model...")
    save_model(model, vectorizer)
    
    # Test predictions
    print("\n4️⃣ Testing predictions...")
    test_cases = [
        "how to identify butterflies?",
        "when is the best time to observe birds?",
        "how to take good photos?",
        "what species can you identify?",
        "hello",
        "你好",
        "如何識別蝴蝶？"
    ]
    
    for test_text in test_cases:
        intent, confidence = predict_intent(model, vectorizer, test_text)
        print(f"  '{test_text}' → {intent} ({confidence:.2%})")
    
    print("\n" + "=" * 60)
    print("✅ Training completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()

