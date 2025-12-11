"""
Enhanced AI Assistant with Advanced Features
- Context Memory: Remembers conversation history
- Sentiment Analysis: Adapts response style based on user emotion
- Personalization: Provides personalized recommendations based on user history
- Multi-turn Conversation: Maintains context across multiple messages
"""

import json
import os
import re
from datetime import datetime
from collections import defaultdict
import random

class EnhancedAIAssistant:
    def __init__(self, knowledge_base_path='knowledge_base.json', resource_library_path='resource_library.json'):
        self.knowledge_base_path = knowledge_base_path
        self.resource_library_path = resource_library_path
        self.knowledge_base = self._load_knowledge_base()
        self.resource_library = self._load_resource_library()
        self.conversation_memory = {}  # Store conversation history per user
        self.user_profiles = {}  # Store user preferences and history
        # Load trained intent classification model
        self.intent_model, self.intent_vectorizer = self._load_intent_model()
        # Quiz state for each user: {user_id: {'current_quiz': quiz_dict, 'waiting_for_answer': bool}}
        self.quiz_states = {}
        # Language preference for each user: {user_id: 'zh' or 'en'}
        self.user_languages = {}
        # Interpretation model generator (lazy loading)
        self.interpretation_generator = None
        
    def _load_knowledge_base(self):
        """Load knowledge base from file"""
        if os.path.exists(self.knowledge_base_path):
            try:
                with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading knowledge base: {e}")
        return {}
    
    def _load_resource_library(self):
        """Load resource library from file"""
        if os.path.exists(self.resource_library_path):
            try:
                with open(self.resource_library_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    resources = data.get('resources', [])
                    print(f"✅ Resource library loaded: {len(resources)} resources")
                    return resources
            except Exception as e:
                print(f"❌ Error loading resource library: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"⚠️ Resource library file not found: {self.resource_library_path}")
        return []
    
    def detect_language(self, text):
        """
        检测文本语言
        
        Args:
            text: 输入文本
        
        Returns:
            'zh' 如果主要是中文，'en' 如果主要是英文
        """
        if not text or not text.strip():
            return 'en'  # 默认英文
        
        # 检测中文字符（Unicode范围：\u4e00-\u9fff）
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        total_chars = len(re.findall(r'[a-zA-Z\u4e00-\u9fff]', text))
        
        if total_chars == 0:
            return 'en'  # 如果没有可识别的字符，默认英文
        
        # 如果中文字符占比超过30%，判定为中文
        chinese_ratio = chinese_chars / total_chars if total_chars > 0 else 0
        
        # 也可以检查常见的中文词汇
        chinese_keywords = ['的', '是', '在', '有', '了', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这']
        has_chinese_keywords = any(keyword in text for keyword in chinese_keywords)
        
        if chinese_ratio > 0.3 or has_chinese_keywords:
            return 'zh'
        else:
            return 'en'
    
    def _get_user_language(self, user_id, message=None):
        """
        获取用户的语言偏好
        
        Args:
            user_id: 用户ID
            message: 当前消息（可选，用于检测语言）
        
        Returns:
            'zh' 或 'en'
        """
        # 如果有当前消息，总是重新检测语言（确保使用当前消息的语言）
        if message:
            detected_lang = self.detect_language(message)
            # 更新用户语言偏好（但每次对话都根据当前消息更新）
            self.user_languages[user_id] = detected_lang
            return detected_lang
        
        # 如果用户已有语言偏好且没有当前消息，使用它
        if user_id in self.user_languages:
            return self.user_languages[user_id]
        
        # 默认英文
        return 'en'
    
    def _load_interpretation_generator(self):
        """
        Load interpretation text generation model (lazy loading)
        
        Returns:
            generator: Generator instance, None if loading fails
        """
        if self.interpretation_generator is not None:
            return self.interpretation_generator
        
        try:
            from generate_interpretation_en import get_generator
            device = 'cuda' if self._check_cuda_available() else 'cpu'
            self.interpretation_generator = get_generator(
                model_path='models/interpretation_model',
                device=device
            )
            if self.interpretation_generator and self.interpretation_generator.loaded:
                print("✅ Interpretation generation model loaded successfully")
                return self.interpretation_generator
            else:
                print("⚠️ Interpretation generation model not loaded (model file may not exist)")
                return None
        except Exception as e:
            print(f"⚠️ Interpretation generation model loading failed: {e}")
            return None
    
    def _check_cuda_available(self):
        """檢查CUDA是否可用"""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False
    
    def _generate_interpretation_with_model(self, species, category, language='en'):
        """
        Generate interpretation text using trained model
        
        Args:
            species: Species name (Chinese name like "臺灣藍鵲")
            category: Category (fun_fact, behavior, habitat, etc.)
            language: Language (model generates English text)
        
        Returns:
            interpretation_text: Generated interpretation text in English, None if failed
        """
        # Load generator (lazy loading)
        generator = self._load_interpretation_generator()
        if generator is None:
            return None
        
        try:
            # Generate text (output will be in English)
            generated_text = generator.generate(
                species=species,
                category=category,
                max_length=256,
                temperature=0.7,
                top_p=0.9
            )
            
            if generated_text and len(generated_text) > 10:  # Ensure meaningful text
                print(f"✅ Model generated interpretation successfully: {species} - {category}")
                return generated_text
            else:
                print(f"⚠️ Model generated text too short or invalid")
                return None
                
        except Exception as e:
            print(f"⚠️ Model generation failed: {e}")
            return None
    
    def _extract_species_from_message(self, message, context=None):
        """
        從消息或上下文中提取物種名稱
        
        Args:
            message: 用戶消息
            context: 上下文（可能包含lastPrediction）
        
        Returns:
            species: 物種名稱，如果無法提取返回None
        """
        # 優先從context中獲取（如果剛完成識別）
        if context and context.get('lastPrediction'):
            predicted_class = context['lastPrediction'].get('class', '')
            if predicted_class:
                return predicted_class
        
        # 從消息中提取（簡單的關鍵詞匹配）
        # 這裡可以擴展為更複雜的NER
        common_species = [
            '臺灣藍鵲', '麻雀', '鳳頭蒼鷹', '大鳳蝶', '紫斑蝶',
            'sparrow', 'eagle', 'butterfly', 'bird'
        ]
        
        message_lower = message.lower()
        for species in common_species:
            if species.lower() in message_lower or species in message:
                return species
        
        return None
    
    def _enhance_response_with_interpretation(self, base_response, message, context, language):
        """
        Enhance response with model-generated interpretation text
        
        Args:
            base_response: Base response
            message: User message
            context: Context
            language: Language
        
        Returns:
            enhanced_response: Enhanced response
        """
        # Check if it's a species information related question (works for both Chinese and English)
        species_info_keywords_zh = ['物種', '種類', '信息', '資訊', '介紹', '特徵', '特點', '習性', '行為', '棲息地']
        species_info_keywords_en = ['species', 'information', 'about', 'tell me', 'characteristics', 'features', 'behavior', 'habitat', 'facts']
        
        has_species_keyword = any(keyword in message for keyword in species_info_keywords_zh) or \
                             any(keyword in message.lower() for keyword in species_info_keywords_en)
        
        if not has_species_keyword:
            return base_response
        
        # Extract species name
        species = self._extract_species_from_message(message, context)
        if not species:
            return base_response
        
        # Try to generate interpretation for different categories
        categories_to_try = ['fun_fact', 'behavior', 'habitat']
        generated_interpretations = []
        
        for category in categories_to_try:
            interpretation = self._generate_interpretation_with_model(species, category, language='en')
            if interpretation:
                generated_interpretations.append((category, interpretation))
                # Only generate the first successful one to avoid overly long responses
                break
        
        # If successfully generated, add to response
        if generated_interpretations:
            category, interpretation = generated_interpretations[0]
            
            # Add title based on category (in English)
            category_titles = {
                'fun_fact': '💡 **Fun Fact**',
                'behavior': '🎯 **Behavior**',
                'habitat': '🌳 **Habitat**'
            }
            title = category_titles.get(category, '📝 **Additional Information**')
            
            # Combine response
            enhanced = f"{base_response}\n\n{title}:\n{interpretation}"
            print(f"✅ Enhanced response with model-generated interpretation: {species} - {category}")
            return enhanced
        
        # If model generation fails, return original response (fallback logic)
        return base_response
    
    def _load_intent_model(self):
        """Load trained intent classification model"""
        try:
            import pickle
            model_path = 'intent_classifier_model.pkl'
            vectorizer_path = 'intent_vectorizer.pkl'
            
            if os.path.exists(model_path) and os.path.exists(vectorizer_path):
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                with open(vectorizer_path, 'rb') as f:
                    vectorizer = pickle.load(f)
                print("✅ Intent classification model loaded successfully")
                return model, vectorizer
            else:
                print("⚠️ Intent model not found, using pattern matching fallback")
                return None, None
        except Exception as e:
            print(f"⚠️ Error loading intent model: {e}, using pattern matching fallback")
            return None, None
    
    def _predict_intent(self, message):
        """Predict user intent using trained model"""
        if self.intent_model is None or self.intent_vectorizer is None:
            return None, 0.0
        
        try:
            import numpy as np
            text_vectorized = self.intent_vectorizer.transform([message.lower()])
            prediction = self.intent_model.predict(text_vectorized)[0]
            probabilities = self.intent_model.predict_proba(text_vectorized)[0]
            confidence = float(max(probabilities))
            return prediction, confidence
        except Exception as e:
            print(f"⚠️ Error in intent prediction: {e}")
            return None, 0.0
    
    def _detect_sentiment(self, message):
        """
        Detect user sentiment from message
        Returns: 'positive', 'negative', 'neutral', 'curious', 'frustrated'
        """
        message_lower = message.lower()
        
        # Positive indicators
        positive_words = ['great', 'good', 'excellent', 'amazing', 'wonderful', 
                         'thanks', 'thank you', 'helpful', 'love', 'awesome',
                         '太好了', '很棒', '謝謝', '感謝', '喜歡']
        if any(word in message_lower for word in positive_words):
            return 'positive'
        
        # Negative/Frustrated indicators
        negative_words = ['bad', 'wrong', 'incorrect', 'not working', 'error',
                         'problem', 'issue', 'confused', 'difficult', 'hard',
                         '不好', '錯誤', '問題', '困難', '不懂', '不會']
        if any(word in message_lower for word in negative_words):
            return 'frustrated'
        
        # Curious indicators
        curious_words = ['why', 'how', 'what', 'when', 'where', 'explain',
                        'tell me', 'can you', 'could you', 'please',
                        '為什麼', '如何', '什麼', '怎麼', '請']
        if any(word in message_lower for word in curious_words):
            return 'curious'
        
        # Question marks indicate curiosity
        if '?' in message:
            return 'curious'
        
        return 'neutral'
    
    def _get_sentiment_style(self, sentiment):
        """Get response style based on sentiment"""
        styles = {
            'positive': {
                'greeting': "Great to hear that! ",
                'tone': 'enthusiastic',
                'emoji': '😊'
            },
            'frustrated': {
                'greeting': "I understand that can be frustrating. Let me help you. ",
                'tone': 'supportive',
                'emoji': '🤝'
            },
            'curious': {
                'greeting': "Great question! ",
                'tone': 'informative',
                'emoji': '🤔'
            },
            'neutral': {
                'greeting': "",
                'tone': 'friendly',
                'emoji': '💬'
            }
        }
        return styles.get(sentiment, styles['neutral'])
    
    def _update_conversation_memory(self, user_id, role, content):
        """Update conversation memory for a user"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        self.conversation_memory[user_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 messages to avoid memory bloat
        if len(self.conversation_memory[user_id]) > 10:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-10:]
    
    def _get_conversation_context(self, user_id):
        """Get recent conversation context"""
        if user_id not in self.conversation_memory:
            return []
        return self.conversation_memory[user_id][-5:]  # Last 5 messages
    
    def _update_user_profile(self, user_id, message, response, context):
        """Update user profile based on interaction"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'topics_asked': defaultdict(int),
                'preferred_category': None,
                'interaction_count': 0,
                'last_interaction': None
            }
        
        profile = self.user_profiles[user_id]
        profile['interaction_count'] += 1
        profile['last_interaction'] = datetime.now().isoformat()
        
        # Track topics
        message_lower = message.lower()
        topics = {
            'identification': ['identify', 'recognize', 'tell', 'what is', '識別', '辨識'],
            'photography': ['photo', 'camera', 'picture', 'image', '拍照', '攝影'],
            'habitat': ['where', 'habitat', 'location', 'find', '哪裡', '棲息地'],
            'behavior': ['behavior', 'behaviour', 'do', 'act', '行為', '習性'],
            'species_info': ['species', 'type', 'kind', '物種', '種類']
        }
        
        for topic, keywords in topics.items():
            if any(keyword in message_lower for keyword in keywords):
                profile['topics_asked'][topic] += 1
        
        # Detect preferred category from context
        if context.get('lastPrediction'):
            category = context['lastPrediction'].get('category', '')
            if 'bird' in category.lower():
                profile['preferred_category'] = 'bird'
            elif 'butterfly' in category.lower():
                profile['preferred_category'] = 'butterfly'
    
    def _get_personalized_recommendation(self, user_id, context):
        """Get personalized recommendation based on user profile"""
        if user_id not in self.user_profiles:
            return None
        
        profile = self.user_profiles[user_id]
        
        # If user has a preferred category, mention it
        if profile['preferred_category']:
            category_name = 'birds' if profile['preferred_category'] == 'bird' else 'butterflies'
            return f"Since you're interested in {category_name}, you might want to explore more {category_name} species!"
        
        # If user asks a lot about photography, suggest photo tips
        if profile['topics_asked']['photography'] > 2:
            return "I notice you're interested in photography. Would you like more advanced photography tips?"
        
        return None
    
    def _should_trigger_behavior_interpretation(self, message):
        """
        检测是否应该触发情境行为解读功能
        
        触发条件：包含地点、观察对象、行为、时间线索
        返回：是否应该触发，以及提取的关键信息
        """
        message_lower = message.lower()
        
        # 地点关键词
        location_keywords = [
            '阳台', '陽台', 'balcony', 'park', '公园', '公園', 'garden', '花园', '花園',
            'window', '窗户', '窗戶', 'yard', '院子', 'field', '田野', 'forest', '森林',
            'tree', '树', '樹', 'branch', '树枝', '樹枝', 'roof', '屋顶', '屋頂',
            'home', '家', 'house', '房子', 'outside', '外面', 'outdoor', '戶外', '户外'
        ]
        
        # 观察对象关键词
        subject_keywords = [
            'bird', 'birds', '鸟', '鳥', '小鸟', '小鳥', 'butterfly', 'butterflies',
            '蝴蝶', 'moth', '蛾', 'animal', '动物', '動物', 'creature', '生物'
        ]
        
        # 行为关键词
        behavior_keywords = [
            '叫', 'sing', 'singing', 'chirp', 'chirping', 'call', 'calling',
            '打架', 'fight', 'fighting', 'attack', 'attacking', 'chase', 'chasing',
            '吃', 'eat', 'eating', 'feed', 'feeding', 'peck', 'pecking',
            '停', 'stop', 'stopped', 'stand', 'standing', 'sit', 'sitting',
            '飞', '飛', 'fly', 'flying', 'hover', 'hovering', 'land', 'landing',
            '跳', 'jump', 'jumping', 'hop', 'hopping', 'move', 'moving',
            '不动', '不動', 'still', 'motionless', 'quiet', '安静', '安靜',
            '观察', '觀察', 'observe', 'watching', '看', 'see', 'saw'
        ]
        
        # 时间线索关键词
        time_keywords = [
            'today', '今天', 'yesterday', '昨天', 'morning', '早晨', '早上',
            'afternoon', '下午', 'evening', '晚上', 'night', '夜晚', 'night',
            'season', '季节', '季節', 'spring', '春天', 'summer', '夏天',
            'autumn', '秋天', 'winter', '冬天', 'now', '现在', '現在',
            'recently', '最近', 'lately', '近来', '近來'
        ]
        
        # 检测是否包含各类关键词
        has_location = any(keyword in message_lower for keyword in location_keywords)
        has_subject = any(keyword in message_lower for keyword in subject_keywords)
        has_behavior = any(keyword in message_lower for keyword in behavior_keywords)
        has_time = any(keyword in message_lower for keyword in time_keywords)
        
        # 还需要检测是否包含疑问词，表示用户在询问行为原因
        question_indicators = [
            'why', '为什么', '為什麼', '为何', '為何', '幹嘛', '干嘛', '做什麼', '做什么',
            '可能', 'maybe', 'perhaps', 'might', 'could', 'would',
            '在干嘛', '在做什麼', '在幹嘛', 'what', 'how', '可能',
            '可能在做', '可能在', '可能', '？', '?'
        ]
        has_question = any(indicator in message_lower for indicator in question_indicators)
        
        # 触发条件：至少包含观察对象和行为，并且（有疑问 或 包含地点/时间）
        # 这样可以捕获更多相关的问题
        should_trigger = (has_subject and has_behavior) and (has_question or has_location or has_time)
        
        if should_trigger:
            # 提取关键信息
            extracted_info = self._extract_behavior_keywords(message, location_keywords, 
                                                             subject_keywords, behavior_keywords, 
                                                             time_keywords)
            return True, extracted_info
        
        return False, None
    
    def _extract_behavior_keywords(self, message, location_keywords, subject_keywords, 
                                   behavior_keywords, time_keywords):
        """
        从消息中提取关键词：物种、行为、地点、时间
        """
        message_lower = message.lower()
        
        # 提取地点
        locations = [kw for kw in location_keywords if kw in message_lower]
        location = locations[0] if locations else None
        
        # 提取观察对象
        subjects = [kw for kw in subject_keywords if kw in message_lower]
        subject = subjects[0] if subjects else None
        
        # 提取行为
        behaviors = [kw for kw in behavior_keywords if kw in message_lower]
        behavior = behaviors[0] if behaviors else None
        
        # 提取时间
        times = [kw for kw in time_keywords if kw in message_lower]
        time_clue = times[0] if times else None
        
        # 尝试提取物种名称（从上下文或消息中）
        species = None
        if subject:
            # 尝试从消息中提取更具体的物种描述
            # 中文模式：蓝色的小鸟、红色蝴蝶等
            chinese_patterns = [
                r'([\u4e00-\u9fff]+色)\s*(?:的)?\s*(?:小)?(?:鸟|鳥|蝴蝶)',  # 蓝色的小鸟
                r'([\u4e00-\u9fff]+)\s*(?:的)?\s*(?:小)?(?:鸟|鳥|蝴蝶)',  # 蓝色小鸟
                r'(?:一只|一隻|一|个|個)\s*([\u4e00-\u9fff]+)\s*(?:的)?\s*(?:小)?(?:鸟|鳥|蝴蝶)',  # 一只蓝色的小鸟
                r'([\u4e00-\u9fff]{2,})\s*(?:的)?\s*(?:小)?(?:鸟|鳥|蝴蝶)'  # 其他描述
            ]
            # 英文模式
            english_patterns = [
                r'(\w+)\s*(?:colored|color)\s*(?:bird|butterfly)',  # blue colored bird
                r'(\w+)\s*(?:bird|butterfly)',  # blue bird
                r'(?:a|an|the)\s*(\w+)\s*(?:bird|butterfly)'  # a blue bird
            ]
            
            for pattern in chinese_patterns + english_patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    potential_species = match.group(1)
                    # 过滤掉常见词
                    common_words = ['the', 'a', 'an', 'this', 'that', 'small', 'little', 'big', 
                                   '小', '大', '一只', '一隻', '一', '个', '個', '的', '只', '隻']
                    if potential_species not in common_words and len(potential_species) > 0:
                        species = potential_species
                        break
        
        return {
            'species': species,
            'subject': subject,
            'behavior': behavior,
            'location': location,
            'time': time_clue,
            'original_message': message
        }
    
    def _generate_behavior_interpretation(self, extracted_info, language='en'):
        """
        生成情境行为解读回答
        
        Args:
            extracted_info: 提取的关键信息
            language: 用户语言偏好
        
        返回结构化的推理结果，包含2-3个可能的原因，按可能性排序
        每个原因后解释生态学意义，最后提供验证线索
        """
        species = extracted_info.get('species')
        subject = extracted_info.get('subject')
        behavior = extracted_info.get('behavior')
        location = extracted_info.get('location')
        time_clue = extracted_info.get('time')
        
        # 根据行为类型生成不同的推理
        behavior_type = self._classify_behavior(behavior)
        
        # 生成推理原因
        interpretations = self._generate_interpretations(behavior_type, subject, species, 
                                                         location, time_clue, language)
        
        # 构建回答
        response = self._build_interpretation_response(extracted_info, interpretations, language)
        
        return response
    
    def _classify_behavior(self, behavior):
        """将行为分类为不同类型"""
        if not behavior:
            return 'unknown'
        
        behavior_lower = behavior.lower()
        
        if any(b in behavior_lower for b in ['叫', 'sing', 'chirp', 'call']):
            return 'vocalization'
        elif any(b in behavior_lower for b in ['打架', 'fight', 'attack', 'chase']):
            return 'aggression'
        elif any(b in behavior_lower for b in ['吃', 'eat', 'feed', 'peck']):
            return 'feeding'
        elif any(b in behavior_lower for b in ['停', 'stop', 'stand', 'sit', '不动', 'still']):
            return 'resting'
        elif any(b in behavior_lower for b in ['飞', 'fly', 'hover', 'land']):
            return 'flying'
        elif any(b in behavior_lower for b in ['跳', 'jump', 'hop', 'move']):
            return 'movement'
        else:
            return 'unknown'
    
    def _generate_interpretations(self, behavior_type, subject, species, location, time_clue, language='en'):
        """
        根据行为类型生成2-3个可能的原因，按可能性排序
        每个原因包含：原因描述、生态学解释、可能性评分
        
        Args:
            behavior_type: 行为类型
            subject: 观察对象
            species: 物种
            location: 地点
            time_clue: 时间线索
            language: 用户语言偏好
        """
        interpretations = []
        
        # 判断是鸟类还是蝴蝶
        is_bird = subject and ('bird' in subject.lower() or '鸟' in subject or '鳥' in subject)
        is_butterfly = subject and ('butterfly' in subject.lower() or '蝴蝶' in subject)
        
        # 根据行为类型生成解释（支持双语）
        if behavior_type == 'vocalization':
            if is_bird:
                if language == 'zh':
                    interpretations = [
                        {
                            'reason': '领域宣告',
                            'reason_en': 'Territory Declaration',
                            'description': '现在可能是繁殖季，牠可能在告诉其他鸟类「这是我的地盘！」。这是许多鸟类春季的常见行为。',
                            'description_en': 'It might be breeding season, and it could be telling other birds "This is my territory!" This is common behavior for many birds in spring.',
                            'probability': 0.4,
                            'verification': '如果牠是停在固定地点有规律地叫，很可能是这个原因',
                            'verification_en': 'If it\'s calling from a fixed location regularly, this is likely the reason'
                        },
                        {
                            'reason': '求偶展示',
                            'reason_en': 'Courtship Display',
                            'description': '牠的歌声可能是在吸引潜在的伴侣。你可以观察附近有没有颜色稍暗、安静聆听的同类。',
                            'description_en': 'Its song might be attracting potential mates. You can observe if there are darker-colored, quietly listening birds nearby.',
                            'probability': 0.35,
                            'verification': '如果牠边叫边跳来跳去，东张西望，就更像这个原因',
                            'verification_en': 'If it\'s calling while jumping around and looking around, this is more likely the reason'
                        },
                        {
                            'reason': '联络同伴',
                            'reason_en': 'Contacting Companions',
                            'description': '也许牠的同伴就在附近，牠们在用叫声保持联系，这是鸟类社会行为的重要方式。',
                            'description_en': 'Perhaps its companions are nearby, and they\'re using calls to stay in contact. This is an important form of social behavior in birds.',
                            'probability': 0.25,
                            'verification': '观察是否有其他同类回应，或者牠是否在等待回应',
                            'verification_en': 'Observe if other birds respond, or if it\'s waiting for a response'
                        }
                    ]
                else:
                    interpretations = [
                        {
                            'reason': 'Territory Declaration',
                            'reason_en': 'Territory Declaration',
                            'description': 'It might be breeding season, and it could be telling other birds "This is my territory!" This is common behavior for many birds in spring.',
                            'description_en': 'It might be breeding season, and it could be telling other birds "This is my territory!" This is common behavior for many birds in spring.',
                            'probability': 0.4,
                            'verification': 'If it\'s calling from a fixed location regularly, this is likely the reason',
                            'verification_en': 'If it\'s calling from a fixed location regularly, this is likely the reason'
                        },
                        {
                            'reason': 'Courtship Display',
                            'reason_en': 'Courtship Display',
                            'description': 'Its song might be attracting potential mates. You can observe if there are darker-colored, quietly listening birds nearby.',
                            'description_en': 'Its song might be attracting potential mates. You can observe if there are darker-colored, quietly listening birds nearby.',
                            'probability': 0.35,
                            'verification': 'If it\'s calling while jumping around and looking around, this is more likely the reason',
                            'verification_en': 'If it\'s calling while jumping around and looking around, this is more likely the reason'
                        },
                        {
                            'reason': 'Contacting Companions',
                            'reason_en': 'Contacting Companions',
                            'description': 'Perhaps its companions are nearby, and they\'re using calls to stay in contact. This is an important form of social behavior in birds.',
                            'description_en': 'Perhaps its companions are nearby, and they\'re using calls to stay in contact. This is an important form of social behavior in birds.',
                            'probability': 0.25,
                            'verification': 'Observe if other birds respond, or if it\'s waiting for a response',
                            'verification_en': 'Observe if other birds respond, or if it\'s waiting for a response'
                        }
                    ]
            else:
                interpretations = [
                    {
                        'reason': '交流信号',
                        'description': '牠可能在通过声音与同类或其他生物进行交流，这是动物沟通的基本方式。',
                        'probability': 0.5,
                        'verification': '观察周围是否有其他同类，或者牠是否在等待回应'
                    },
                    {
                        'reason': '警告信号',
                        'description': '可能感知到了潜在的危险或威胁，通过叫声警告同伴或驱赶入侵者。',
                        'probability': 0.5,
                        'verification': '观察周围环境，看是否有其他动物或人类接近'
                    }
                ]
        
        elif behavior_type == 'aggression':
            if is_bird:
                interpretations = [
                    {
                        'reason': '领地争夺',
                        'description': '鸟类在繁殖期会激烈保卫自己的领地，这是确保食物和繁殖资源的重要行为。',
                        'probability': 0.45,
                        'verification': '观察是否持续在同一区域发生冲突，这通常是领地行为'
                    },
                    {
                        'reason': '资源竞争',
                        'description': '可能是在争夺食物、水源或栖息位置，这是自然选择中常见的竞争行为。',
                        'probability': 0.35,
                        'verification': '观察附近是否有食物或水源，冲突是否围绕这些资源'
                    },
                    {
                        'reason': '求偶竞争',
                        'description': '雄性之间可能在进行求偶竞争，展示自己的强壮以获得雌性的青睐。',
                        'probability': 0.2,
                        'verification': '观察是否有雌性在附近，或者是否在繁殖季节'
                    }
                ]
            else:
                interpretations = [
                    {
                        'reason': '资源竞争',
                        'description': '可能是在争夺食物、栖息地或配偶，这是动物界常见的竞争行为。',
                        'probability': 0.6,
                        'verification': '观察周围环境，看是否有明显的资源（食物、栖息地）'
                    },
                    {
                        'reason': '防御行为',
                        'description': '可能是在保护自己或后代，这是生存本能的重要体现。',
                        'probability': 0.4,
                        'verification': '观察是否有幼崽或巢穴在附近'
                    }
                ]
        
        elif behavior_type == 'feeding':
            interpretations = [
                {
                    'reason': '正常觅食',
                    'description': '这是动物的基本生存行为，牠们在寻找食物来维持能量和营养需求。',
                    'probability': 0.5,
                    'verification': '观察牠是否在仔细搜索，这是正常觅食的特征'
                },
                {
                    'reason': '育雏喂养',
                    'description': '如果是在繁殖期，牠可能在为幼崽寻找食物，这是父母照顾后代的重要行为。',
                    'probability': 0.3,
                    'verification': '观察牠是否频繁往返同一地点，可能那里有巢穴'
                },
                {
                    'reason': '季节性觅食',
                    'description': '可能是在为即将到来的季节（如迁徙或冬眠）储备能量。',
                    'probability': 0.2,
                    'verification': '结合时间线索，判断是否在迁徙或准备期'
                }
            ]
        
        elif behavior_type == 'resting':
            interpretations = [
                {
                    'reason': '能量恢复',
                    'description': '动物需要休息来恢复体力，特别是在活动后或天气炎热时。',
                    'probability': 0.4,
                    'verification': '观察牠是否显得疲惫，或者环境温度是否较高'
                },
                {
                    'reason': '观察环境',
                    'description': '牠可能在暂停活动，仔细观察周围环境，确保安全后再继续行动。',
                    'probability': 0.35,
                    'verification': '观察牠是否在转动头部或身体，保持警觉'
                },
                {
                    'reason': '等待时机',
                    'description': '可能是在等待合适的时机，比如等待猎物、同伴或天气变化。',
                    'probability': 0.25,
                    'verification': '观察牠是否在特定位置等待，或者环境是否有变化'
                }
            ]
        
        elif behavior_type == 'flying':
            if is_butterfly:
                interpretations = [
                    {
                        'reason': '寻找食物',
                        'description': '蝴蝶在飞行中寻找花蜜或合适的产卵地点，这是牠们的主要活动方式。',
                        'probability': 0.4,
                        'verification': '观察牠是否在花朵附近盘旋，或者在特定植物上停留'
                    },
                    {
                        'reason': '求偶行为',
                        'description': '可能在进行求偶飞行，通过飞行展示来吸引异性，这是繁殖行为的一部分。',
                        'probability': 0.35,
                        'verification': '观察是否有其他蝴蝶跟随，或者飞行模式是否特殊'
                    },
                    {
                        'reason': '迁徙或扩散',
                        'description': '可能在进行季节性迁徙或寻找新的栖息地，这是种群扩散的重要方式。',
                        'probability': 0.25,
                        'verification': '结合时间和地点，判断是否在迁徙季节或新环境'
                    }
                ]
            else:
                interpretations = [
                    {
                        'reason': '正常活动',
                        'description': '飞行是鸟类的基本活动方式，牠可能在寻找食物、栖息地或同伴。',
                        'probability': 0.5,
                        'verification': '观察飞行方向和模式，判断是否有特定目标'
                    },
                    {
                        'reason': '逃避威胁',
                        'description': '可能感知到了危险，通过飞行来逃避潜在的威胁。',
                        'probability': 0.3,
                        'verification': '观察周围环境，看是否有其他动物或突然的动静'
                    },
                    {
                        'reason': '迁徙',
                        'description': '如果是在迁徙季节，牠可能在进行长距离迁徙，寻找合适的栖息地。',
                        'probability': 0.2,
                        'verification': '结合时间和地点线索，判断是否在迁徙期'
                    }
                ]
        
        else:
            # 默认解释
            interpretations = [
                {
                    'reason': '自然行为',
                    'description': '这是该物种的正常行为模式，反映了牠们适应环境的方式。',
                    'probability': 0.5,
                    'verification': '持续观察，了解这种行为是否规律出现'
                },
                {
                    'reason': '环境响应',
                    'description': '可能是在响应环境变化，如天气、食物资源或同伴的存在。',
                    'probability': 0.5,
                    'verification': '观察环境因素，看是否有明显的变化'
                }
            ]
        
        # 按可能性排序（从高到低）
        interpretations.sort(key=lambda x: x['probability'], reverse=True)
        
        # 只返回前2-3个
        return interpretations[:3]
    
    def _should_trigger_resource_request(self, message):
        """
        检测是否应该触发资源推荐功能
        
        触发条件：用户明确请求资源、网站、摄影技巧等
        """
        message_lower = message.lower()
        
        resource_keywords = [
            '推荐', '推薦', '網站', '网站', '資源', '资源', '連結', '链接', 'link',
            '攝影', '摄影', '拍照', '技巧', 'technique', 'tip', 'tips',
            '哪裡看', '哪里看', 'where to see', 'where to find',
            '圖鑑', '图鉴', 'field guide', 'guide',
            'platform', 'platform', 'database', '資料庫', '数据库',
            'website', 'resource', 'recommend', 'recommendation',
            'how to photograph', 'photography tips', 'photography guide',
            '觀測', '观测', 'observation', 'watch'
        ]
        
        should_trigger = any(keyword in message_lower for keyword in resource_keywords)
        if should_trigger:
            print(f"🔍 [RESOURCE] 检测到资源请求关键词: {message[:50]}...")
        return should_trigger
    
    def _handle_resource_request(self, message, language='en'):
        """
        处理资源推荐请求
        
        Args:
            message: 用户消息
            language: 用户语言偏好
        
        Returns:
            格式化的资源推荐响应，如果匹配到资源；None如果没有匹配
        """
        if not self._should_trigger_resource_request(message):
            return None
        
        print(f"🔍 [RESOURCE] 处理资源请求，语言: {language}, 资源库大小: {len(self.resource_library)}")
        
        # 从资源库中筛选匹配的资源
        matched_resources = self._match_resources(message, language)
        
        print(f"🔍 [RESOURCE] 匹配到 {len(matched_resources)} 个资源")
        
        if not matched_resources:
            print(f"⚠️ [RESOURCE] 没有匹配到资源")
            return None
        
        # 格式化响应
        response = self._format_resource_response(matched_resources, language)
        print(f"✅ [RESOURCE] 生成资源推荐响应")
        return response
    
    def _match_resources(self, message, language):
        """
        从资源库中匹配最相关的资源
        
        Args:
            message: 用户消息
            language: 用户语言偏好
        
        Returns:
            匹配的资源列表（最多3个）
        """
        message_lower = message.lower()
        matched = []
        
        for resource in self.resource_library:
            # 计算匹配分数
            score = 0
            
            # 语言支持检查（如果语言匹配，给予加分；如果不匹配但关键词匹配度高，仍可推荐）
            language_support = resource.get('language_support', [])
            language_match = language in language_support
            if language_match:
                score += 5  # 语言匹配加分
            # 如果不匹配，但关键词匹配度高，仍然可以考虑（不直接跳过）
            
            # 关键词匹配
            keywords = resource.get('keywords', [])
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in message_lower:
                    score += 3
                elif any(word in message_lower for word in keyword_lower.split()):
                    score += 1
            
            # 标签匹配
            tags = resource.get('tags', [])
            for tag in tags:
                tag_lower = tag.lower()
                if tag_lower in message_lower:
                    score += 2
            
            # 类别匹配
            category = resource.get('category', '')
            category_keywords = {
                'photography': ['photography', 'photo', 'camera', '拍照', '摄影', '相机'],
                'field_guide': ['guide', 'field guide', 'identification', '图鉴', '指南', '识别'],
                'observation_platform': ['platform', 'observation', 'watch', '观察', '平台', '观测'],
                'mobile_app': ['app', 'mobile', 'application', '应用', '手机'],
                'sound_database': ['sound', 'audio', 'call', '声音', '音频', '叫声']
            }
            if category in category_keywords:
                for keyword in category_keywords[category]:
                    if keyword in message_lower:
                        score += 2
                        break
            
            # 如果分数足够高（即使语言不完全匹配），也可以推荐
            # 但如果语言匹配，优先推荐
            if score > 0:
                # 如果语言不匹配但分数很高，仍然可以推荐（但降低优先级）
                if not language_match and score < 5:
                    continue  # 分数太低且语言不匹配，跳过
                matched.append((resource, score))
        
        # 按分数排序，返回前3个
        matched.sort(key=lambda x: x[1], reverse=True)
        return [resource for resource, score in matched[:3]]
    
    def _format_resource_response(self, resources, language):
        """
        格式化资源推荐响应
        
        Args:
            resources: 资源列表
            language: 用户语言偏好
        
        Returns:
            格式化后的响应文本
        """
        # 确保使用正确的语言（根据当前消息检测，而不是之前保存的偏好）
        print(f"🔍 [RESOURCE] 格式化响应，使用语言: {language}")
        
        if language == 'zh':
            response_parts = ["📚 **资源推荐**：\n\n根据你的需求，我为你推荐以下资源：\n"]
            for i, resource in enumerate(resources, 1):
                # 优先使用中文名称和描述
                name = resource.get('name_zh') or resource.get('name', '')
                description = resource.get('description_zh') or resource.get('description', '')
                url = resource.get('url', '')
                response_parts.append(f"{i}. **{name}**")
                response_parts.append(f"   {description}")
                response_parts.append(f"   🔗 {url}\n")
            response_parts.append("希望这些资源对你有帮助！")
        else:
            # 英文响应
            response_parts = ["📚 **Resource Recommendations**:\n\nBased on your request, here are some recommended resources:\n"]
            for i, resource in enumerate(resources, 1):
                # 使用英文名称和描述
                name = resource.get('name', '')
                description = resource.get('description', '')
                url = resource.get('url', '')
                response_parts.append(f"{i}. **{name}**")
                response_parts.append(f"   {description}")
                response_parts.append(f"   🔗 {url}\n")
            response_parts.append("Hope these resources are helpful!")
        
        return "\n".join(response_parts)
    
    def _should_trigger_quiz(self, message):
        """
        检测是否应该触发挑战游戏功能
        
        触发条件：用户明确请求玩游戏或挑战
        """
        message_lower = message.lower()
        
        quiz_keywords = [
            '玩游戏', '来点挑战', '挑战', '猜谜', 'quiz', 'game', 'challenge',
            'play', 'guess', 'test', 'question', '题目', '问题', '小游戏',
            '來點挑戰', '玩遊戲', '猜謎', '題目', '問題', '小遊戲'
        ]
        
        return any(keyword in message_lower for keyword in quiz_keywords)
    
    def _is_waiting_for_quiz_answer(self, user_id):
        """检查是否在等待用户回答挑战题目"""
        if user_id not in self.quiz_states:
            return False
        return self.quiz_states[user_id].get('waiting_for_answer', False)
    
    def _start_quiz(self, user_id, message, language='en'):
        """
        开始一个新的挑战游戏
        
        Args:
            user_id: 用户ID
            message: 用户消息
            language: 用户语言偏好
        
        Returns:
            格式化后的题目消息，如果成功；None如果失败
        """
        try:
            from quiz_library import get_random_quiz, format_quiz_message
            
            # 检测用户偏好（鸟类还是蝴蝶）
            category = None
            message_lower = message.lower()
            if any(word in message_lower for word in ['鸟', 'bird', '鸟类']):
                category = 'bird'
            elif any(word in message_lower for word in ['蝴蝶', 'butterfly', '蝶']):
                category = 'butterfly'
            
            # 获取随机题目
            quiz = get_random_quiz(category=category)
            
            # 格式化题目（使用用户语言）
            quiz_message = format_quiz_message(quiz, language=language)
            
            # 保存状态
            if user_id not in self.quiz_states:
                self.quiz_states[user_id] = {}
            self.quiz_states[user_id]['current_quiz'] = quiz
            self.quiz_states[user_id]['waiting_for_answer'] = True
            
            return quiz_message
            
        except Exception as e:
            print(f"Error starting quiz: {e}")
            return None
    
    def _handle_quiz_answer(self, user_id, message, language='en'):
        """
        处理用户的挑战答案
        
        Args:
            user_id: 用户ID
            message: 用户消息
            language: 用户语言偏好
        
        Returns:
            反馈消息，如果识别为答案；None如果不是答案
        """
        if user_id not in self.quiz_states:
            return None
        
        quiz_state = self.quiz_states[user_id]
        if not quiz_state.get('waiting_for_answer', False):
            return None
        
        # 提取答案（A, B, C, D）
        message_upper = message.strip().upper()
        answer_pattern = re.search(r'\b([ABCD])\b', message_upper)
        
        if not answer_pattern:
            # 如果不是答案格式，清除等待状态，让用户继续正常对话
            quiz_state['waiting_for_answer'] = False
            return None
        
        user_answer = answer_pattern.group(1)
        quiz = quiz_state.get('current_quiz')
        
        if not quiz:
            quiz_state['waiting_for_answer'] = False
            return None
        
        try:
            from quiz_library import check_quiz_answer
            
            is_correct, feedback = check_quiz_answer(quiz, user_answer, language=language)
            
            # 清除等待状态
            quiz_state['waiting_for_answer'] = False
            quiz_state['current_quiz'] = None
            
            # 添加鼓励和下一步提示（根据语言）
            if language == 'zh':
                if is_correct:
                    feedback += "\n\n🎯 想再来一题吗？说「玩游戏」或「来点挑战」就可以继续！"
                else:
                    feedback += "\n\n💪 想再试试吗？说「玩游戏」就可以继续挑战！"
            else:
                if is_correct:
                    feedback += "\n\n🎯 Want another challenge? Just say 'play game' or 'quiz'!"
                else:
                    feedback += "\n\n💪 Want to try again? Just say 'play game'!"
            
            return feedback
            
        except Exception as e:
            print(f"Error handling quiz answer: {e}")
            quiz_state['waiting_for_answer'] = False
            return None
    
    def _build_interpretation_response(self, extracted_info, interpretations, language='en'):
        """构建完整的解读回答（支持双语）"""
        species = extracted_info.get('species')
        subject = extracted_info.get('subject')
        behavior = extracted_info.get('behavior')
        location = extracted_info.get('location')
        
        # 根据语言选择文本
        if language == 'zh':
            greeting = "这真是一次有趣的邂逅！"
            challenge_label = "🔍 **小挑战**："
            challenge_intro = "试著偷偷观察一下，"
            challenge_question = "你观察到的哪种情况呢？"
        else:
            greeting = "What an interesting encounter!"
            challenge_label = "🔍 **Little Challenge**:"
            challenge_intro = "Try to observe quietly: "
            challenge_question = "What situation did you observe?"
        
        # 构建开头
        response_parts = [greeting]
        
        # 总结线索（更自然的格式）
        clues = []
        if species:
            # 处理物种描述，如"蓝色的小鸟" -> "蓝色小鸟"
            species_desc = species.replace('的', '').replace(' ', '')
            clues.append(f"「{species_desc}」")
        elif subject:
            # 处理subject，如"bird" -> "小鸟"
            if 'bird' in subject.lower():
                clues.append("「小鸟」")
            elif 'butterfly' in subject.lower():
                clues.append("「蝴蝶」")
            else:
                clues.append(f"「{subject}」")
        
        if behavior:
            # 处理行为描述
            behavior_desc = behavior
            if '叫' in behavior or 'sing' in behavior.lower() or 'chirp' in behavior.lower():
                behavior_desc = "持续鸣叫"
            elif '打架' in behavior or 'fight' in behavior.lower():
                behavior_desc = "打架"
            elif '吃' in behavior or 'eat' in behavior.lower():
                behavior_desc = "吃东西"
            elif '停' in behavior or 'still' in behavior.lower() or '不动' in behavior:
                behavior_desc = "停着不动"
            clues.append(f"「{behavior_desc}」")
        
        if location:
            clues.append(f"「在{location}」")
        
        # 根据语言选择线索文本
        if language == 'zh':
            if clues:
                response_parts.append(f"根据{''.join(clues)}这些线索，有几种可能：\n")
        else:
            if clues:
                response_parts.append(f"Based on these clues {', '.join(clues)}, there are several possibilities:\n")
        
        # 添加解释（根据语言选择对应字段）
        for i, interp in enumerate(interpretations, 1):
            if language == 'zh':
                reason = interp.get('reason', interp.get('reason_en', ''))
                description = interp.get('description', interp.get('description_en', ''))
            else:
                reason = interp.get('reason_en', interp.get('reason', ''))
                description = interp.get('description_en', interp.get('description', ''))
            response_parts.append(f"{i}. **{reason}**: {description}")
        
        # 添加验证线索（根据语言选择对应字段）
        if interpretations:
            response_parts.append(f"\n{challenge_label}")
            # 构建验证提示
            if language == 'zh':
                primary_hint = interpretations[0].get('verification', interpretations[0].get('verification_en', ''))
                if len(interpretations) > 1:
                    secondary_hint = interpretations[1].get('verification', interpretations[1].get('verification_en', ''))
                    response_parts.append(f"{challenge_intro}{primary_hint}；{secondary_hint}。")
                else:
                    response_parts.append(f"{challenge_intro}{primary_hint}。")
            else:
                primary_hint = interpretations[0].get('verification_en', interpretations[0].get('verification', ''))
                if len(interpretations) > 1:
                    secondary_hint = interpretations[1].get('verification_en', interpretations[1].get('verification', ''))
                    response_parts.append(f"{challenge_intro}{primary_hint}; {secondary_hint}.")
                else:
                    response_parts.append(f"{challenge_intro}{primary_hint}.")
            response_parts.append(challenge_question)
        
        return "\n".join(response_parts)
    
    def _match_knowledge_base(self, message, language='en'):
        """
        Match message against knowledge base using trained model or pattern matching
        
        Args:
            message: User message
            language: User language preference ('zh' or 'en')
        
        Returns:
            (category, responses, score) or None
        """
        message_lower = message.lower()
        
        # Special handling for website/link requests
        website_keywords = ['網站', 'website', 'link', '連結', '鏈接', '資源', 'resource', '推薦', 'recommend']
        is_website_request = any(keyword in message_lower for keyword in website_keywords)
        
        # First try to use trained model for intent classification
        predicted_intent, model_confidence = self._predict_intent(message)
        
        if predicted_intent and model_confidence > 0.5:
            # Use model prediction if confidence is high enough
            if predicted_intent in self.knowledge_base:
                data = self.knowledge_base[predicted_intent]
                responses = data.get('responses', [])
                if responses:
                    # If it's a website request, prefer responses with links
                    if is_website_request:
                        link_responses = [r for r in responses if 'http' in r or '[' in r]
                        if link_responses:
                            return (predicted_intent, link_responses, model_confidence * 10)
                    return (predicted_intent, responses, model_confidence * 10)
        
        # Fallback to pattern matching if model not available or low confidence
        best_match = None
        best_score = 0
        
        for category, data in self.knowledge_base.items():
            if category == 'default':
                continue
            
            patterns = data.get('patterns', [])
            responses = data.get('responses', [])
            
            # Improved scoring: exact match > partial match
            score = 0
            for pattern in patterns:
                pattern_lower = pattern.lower()
                if pattern_lower == message_lower:
                    score += 10  # Exact match
                elif pattern_lower in message_lower:
                    score += 5  # Partial match (increased from 3)
                elif any(word in message_lower for word in pattern_lower.split()):
                    score += 2  # Word match (increased from 1)
            
            # 特殊处理：如果问题明确包含"蝴蝶和蛾"或"butterfly and moth"，大幅提升匹配分数
            butterfly_moth_keywords = ['蝴蝶和蛾', 'butterfly and moth', 'butterfly vs moth', 'butterfly moth', '蛾和蝴蝶', 'moth and butterfly', '有什麼區別', '有什麼不同', 'difference', '區分']
            if any(keyword in message_lower for keyword in butterfly_moth_keywords):
                if category == 'butterfly_moth_difference':
                    score += 50  # 大幅提升专门类别的分数
                    print(f"🔍 [DEBUG] 检测到蝴蝶和蛾问题，提升 {category} 分数: {score}")
                elif category == 'identification_tips':
                    score -= 10  # 降低通用类别的分数，避免误匹配
                    print(f"🔍 [DEBUG] 降低 {category} 分数以避免误匹配: {score}")
            
            # Boost score for website requests matching photo_tips
            if is_website_request and category == 'photo_tips':
                score += 5
            
            if score > best_score and responses:
                # If it's a website request, prefer responses with links
                if is_website_request:
                    link_responses = [r for r in responses if 'http' in r or '[' in r]
                    if link_responses:
                        best_score = score
                        best_match = (category, link_responses, score)
                        continue
                
                best_score = score
                best_match = (category, responses, score)
        
        return best_match
    
    def generate_response(self, message, context=None, user_id='default'):
        """
        Generate enhanced AI response with context memory and personalization
        
        Args:
            message: User message
            context: Additional context (e.g., lastPrediction, historyCount)
            user_id: Unique user identifier (for memory and personalization)
        
        Returns:
            Enhanced response with personalization
        """
        if context is None:
            context = {}
        
        # 检测并保存用户语言偏好（核心功能）
        user_language = self._get_user_language(user_id, message)
        
        # 调试日志：打印检测到的语言
        detected_lang = self.detect_language(message)
        print(f"🔍 [DEBUG] 用户消息: {message[:50]}...")
        print(f"🔍 [DEBUG] 检测到的语言: {detected_lang}")
        print(f"🔍 [DEBUG] 使用的回复语言: {user_language}")
        
        # Detect sentiment
        sentiment = self._detect_sentiment(message)
        style = self._get_sentiment_style(sentiment)
        
        # Update conversation memory
        self._update_conversation_memory(user_id, 'user', message)
        
        # Get conversation context
        conversation_context = self._get_conversation_context(user_id)
        
        # Check if this is a follow-up question
        is_follow_up = len(conversation_context) > 1
        
        base_response = None
        
        base_response = None
        
        # 检查是否在等待挑战答案
        if self._is_waiting_for_quiz_answer(user_id):
            quiz_result = self._handle_quiz_answer(user_id, message, user_language)
            if quiz_result:
                base_response = quiz_result
        
        # 如果还没有响应，检查是否请求挑战游戏
        if not base_response and self._should_trigger_quiz(message):
            quiz_response = self._start_quiz(user_id, message, user_language)
            if quiz_response:
                base_response = quiz_response
        
        # 如果还没有响应，检查是否应该触发情境行为解读功能
        if not base_response:
            should_trigger, extracted_info = self._should_trigger_behavior_interpretation(message)
            if should_trigger and extracted_info:
                base_response = self._generate_behavior_interpretation(extracted_info, user_language)
        
        # 如果还没有响应，检查是否请求资源推荐
        if not base_response:
            print(f"🔍 [RESOURCE] 检查资源推荐功能，消息: {message[:50]}...")
            # 重新检测当前消息的语言（确保使用当前消息的语言，而不是之前保存的偏好）
            current_lang = self.detect_language(message)
            print(f"🔍 [RESOURCE] 当前消息检测到的语言: {current_lang}, 用户语言偏好: {user_language}")
            resource_response = self._handle_resource_request(message, current_lang)
            if resource_response:
                print(f"✅ [RESOURCE] 资源推荐功能返回响应")
                base_response = resource_response
            else:
                print(f"ℹ️ [RESOURCE] 资源推荐功能未触发或未匹配到资源")
        
        # 如果还没有响应，尝试匹配知识库
        if not base_response:
            match_result = self._match_knowledge_base(message, user_language)
            
            if match_result:
                category, responses, score = match_result
                # 随机选择一个响应
                base_response = random.choice(responses) if responses else None
                print(f"🔍 [DEBUG] 从知识库匹配到: {category}, 分数: {score}")
            else:
                # Use fallback response
                base_response = self._generate_fallback_response(message, context, conversation_context, user_language)
                print(f"🔍 [DEBUG] 使用fallback响应, 语言: {user_language}")
        
        # 如果对话较为空闲，主动发起挑战（可选）
        if not is_follow_up and len(conversation_context) <= 2:
            # 在响应后添加主动挑战提示
            pass  # 暂时不在每次响应都主动挑战，避免过于频繁
        
        # Enhance response with personalization
        enhanced_response = self._enhance_response(
            base_response, 
            sentiment, 
            style, 
            is_follow_up,
            context,
            user_id,
            user_language
        )
        
        # 嘗試使用模型生成解讀文本來增強響應（如果適用）
        # 這會在響應末尾添加模型生成的解讀，如果模型失敗則回退到原始響應
        if base_response:  # 只在有基礎響應時嘗試
            enhanced_response = self._enhance_response_with_interpretation(
                enhanced_response,
                message,
                context,
                user_language
            )
        
        # Update user profile
        self._update_user_profile(user_id, message, enhanced_response, context)
        
        # Update conversation memory with response
        self._update_conversation_memory(user_id, 'assistant', enhanced_response)
        
        return enhanced_response
    
    def _enhance_response(self, base_response, sentiment, style, is_follow_up, context, user_id, language='en'):
        """Enhance base response with personalization and context"""
        enhanced = base_response
        
        # Add sentiment-appropriate greeting
        if style['greeting'] and not is_follow_up:
            enhanced = style['emoji'] + " " + style['greeting'] + enhanced
        
        # Add personalized recommendation
        personalized = self._get_personalized_recommendation(user_id, context)
        if personalized:
            enhanced += "\n\n💡 " + personalized
        
        # Add context-aware follow-up if this is a continuation
        if is_follow_up and context.get('lastPrediction'):
            species = context['lastPrediction'].get('class', '')
            if species:
                enhanced += f"\n\n📌 By the way, about your recent identification of {species}, feel free to ask if you have more questions!"
        
        return enhanced
    
    def _generate_fallback_response(self, message, context, conversation_context, language='en'):
        """Generate fallback response with context awareness (supports bilingual)"""
        message_lower = message.lower()
        
        # Check conversation context for continuity
        if conversation_context:
            last_user_msg = None
            for msg in reversed(conversation_context):
                if msg['role'] == 'user':
                    last_user_msg = msg['content']
                    break
            
            # If asking about previous topic
            if language == 'zh':
                if last_user_msg and any(word in message_lower for word in ['more', 'also', 'another', 'other', '還有', '另外']):
                    return "我很乐意提供更多信息！你能更具体地说明你想了解什么吗？"
            else:
                if last_user_msg and any(word in message_lower for word in ['more', 'also', 'another', 'other']):
                    return "I'd be happy to provide more information! Could you be more specific about what you'd like to know?"
        
        # Standard fallback responses
        if any(word in message_lower for word in ['help', 'what can you do', 'capabilities', '幫助', '能做什麼']):
            if language == 'zh':
                return """我是你的自然探索伙伴！我可以帮你：

🔍 **识别物种**：上传照片或描述特征，我来帮你识别
🎯 **行为解读**：告诉我你观察到的动物行为（比如「阳台上的鸟为什么一直叫？」），我像侦探一样推理原因
🎮 **挑战游戏**：说「玩游戏」或「来点挑战」，我们一起玩有趣的猜谜游戏
💡 **观察建议**：根据你的兴趣，给你个性化的探索建议
📚 **知识解答**：关于鸟类和蝴蝶的各种问题

有什么想探索的吗？或者说「玩游戏」来挑战一下！"""
            else:
                return """I'm your nature exploration partner! I can help you with:

🔍 **Species Identification**: Upload photos or describe features, and I'll help identify them
🎯 **Behavior Interpretation**: Tell me about animal behaviors you've observed (like "Why is the bird on my balcony calling?"), and I'll reason like a detective
🎮 **Challenge Games**: Say "play game" or "quiz", and let's play fun guessing games together
💡 **Observation Tips**: Personalized exploration suggestions based on your interests
📚 **Knowledge Answers**: Various questions about birds and butterflies

What would you like to explore? Or say "play game" for a challenge!"""
        
        # Default response
        if language == 'zh':
            return """我是你的自然探索伙伴 🌿

我可以帮你：
• 🔍 识别鸟类和蝴蝶
• 🎯 解读动物行为（比如「阳台上的鸟为什么一直叫？」）
• 🎮 玩有趣的猜谜挑战（说「玩游戏」试试！）
• 💡 提供观察和摄影建议
• 📚 解答各种自然问题

今天有什么有趣的发现想分享吗？或者说「玩游戏」来个小挑战！"""
        else:
            return """I'm your nature exploration partner 🌿

I can help you with:
• 🔍 Identifying birds and butterflies
• 🎯 Interpreting animal behaviors (like "Why is the bird on my balcony calling?")
• 🎮 Fun guessing challenges (try saying "play game"!)
• 💡 Observation and photography tips
• 📚 Answering various nature questions

What interesting discoveries have you made today? Or say "play game" for a little challenge!"""


# Global instance
_enhanced_assistant = None

def get_enhanced_assistant():
    """Get or create enhanced assistant instance"""
    global _enhanced_assistant
    if _enhanced_assistant is None:
        print("🔄 Creating new EnhancedAIAssistant instance...")
        _enhanced_assistant = EnhancedAIAssistant()
        print(f"✅ EnhancedAIAssistant created")
        print(f"   - Knowledge base: {len(_enhanced_assistant.knowledge_base)} categories")
        print(f"   - Resource library: {len(_enhanced_assistant.resource_library)} resources")
    return _enhanced_assistant

