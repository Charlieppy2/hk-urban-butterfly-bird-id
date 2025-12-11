"""
Quiz Library for Interactive Challenge Feature
存放猜谜题目和答案，支持中英文
"""

QUIZ_LIBRARY = [
    {
        'id': 1,
        'question': '这只鸟的喙又长又直，适合在浅水中捕鱼。牠最可能是？',
        'question_en': 'This bird has a long, straight beak perfect for catching fish in shallow water. What is it most likely?',
        'options': ['A. 苍鹭 (Heron)', 'B. 麻雀 (Sparrow)', 'C. 啄木鸟 (Woodpecker)', 'D. 蜂鸟 (Hummingbird)'],
        'answer': 'A',
        'explanation': '苍鹭的喙又长又直，是专门为在浅水中捕鱼而进化的！牠们会静静地站在水中，等待鱼儿游过。',
        'explanation_en': "Herons have long, straight beaks evolved specifically for catching fish in shallow water! They stand still in water, waiting for fish to swim by.",
        'category': 'bird',
        'difficulty': 'easy'
    },
    {
        'id': 2,
        'question': '如果一只蝴蝶的翅膀上有眼状斑纹，这最可能是为了？',
        'question_en': 'If a butterfly has eye-like patterns on its wings, this is most likely for?',
        'options': ['A. 吸引配偶', 'B. 吓退捕食者', 'C. 调节体温', 'D. 导航定位'],
        'options_en': ['A. Attract mates', 'B. Scare away predators', 'C. Regulate temperature', 'D. Navigation'],
        'answer': 'B',
        'explanation': '眼状斑纹是蝴蝶的防御机制！牠们会让捕食者误以为是大型动物的眼睛，从而吓退敌人。',
        'explanation_en': "Eye-like patterns are a defense mechanism! They make predators think they're seeing a large animal's eyes, scaring them away.",
        'category': 'butterfly',
        'difficulty': 'medium'
    },
    {
        'id': 3,
        'question': '哪种鸟类的迁徙距离最长？',
        'question_en': 'Which bird species migrates the longest distance?',
        'options': ['A. 燕子 (Swallow)', 'B. 北极燕鸥 (Arctic Tern)', 'C. 大雁 (Goose)', 'D. 信天翁 (Albatross)'],
        'answer': 'B',
        'explanation': '北极燕鸥每年从北极飞到南极再飞回来，总距离可达7万公里！这是动物界最长的迁徙路线。',
        'explanation_en': 'Arctic Terns fly from the Arctic to Antarctica and back each year, covering up to 70,000 km! This is the longest migration route in the animal kingdom.',
        'category': 'bird',
        'difficulty': 'hard'
    },
    {
        'id': 4,
        'question': '蝴蝶和蛾类最明显的区别是什么？',
        'question_en': 'What is the most obvious difference between butterflies and moths?',
        'options': ['A. 触角形状', 'B. 翅膀颜色', 'C. 体型大小', 'D. 飞行速度'],
        'options_en': ['A. Antenna shape', 'B. Wing color', 'C. Body size', 'D. Flight speed'],
        'answer': 'A',
        'explanation': '蝴蝶的触角是棒状的，而蛾类的触角是羽毛状或丝状的。这是最可靠的区分方法！',
        'explanation_en': "Butterflies have club-shaped antennae, while moths have feathery or thread-like antennae. This is the most reliable way to tell them apart!",
        'category': 'butterfly',
        'difficulty': 'easy'
    },
    {
        'id': 5,
        'question': '如果一只鸟在春天不停地鸣叫，最可能的原因是？',
        'question_en': 'If a bird keeps singing in spring, the most likely reason is?',
        'options': ['A. 寻找食物', 'B. 宣告领地和求偶', 'C. 警告危险', 'D. 练习唱歌'],
        'options_en': ['A. Looking for food', 'B. Territory declaration and courtship', 'C. Warning of danger', 'D. Practicing singing'],
        'answer': 'B',
        'explanation': '春天是繁殖季节！鸟类的歌声主要用于宣告领地所有权和吸引配偶，这是牠们最重要的生存策略。',
        'explanation_en': "Spring is breeding season! Birds' songs are mainly for declaring territory and attracting mates - their most important survival strategy.",
        'category': 'bird',
        'difficulty': 'medium'
    },
    {
        'id': 6,
        'question': '蝴蝶的翅膀颜色主要来自？',
        'question_en': 'Butterfly wing colors mainly come from?',
        'options': ['A. 色素', 'B. 结构色', 'C. 两者都有', 'D. 食物颜色'],
        'options_en': ['A. Pigments', 'B. Structural colors', 'C. Both', 'D. Food colors'],
        'answer': 'C',
        'explanation': '蝴蝶的美丽颜色来自色素和结构色的结合！结构色通过光的折射产生彩虹效果，这就是为什么蝴蝶翅膀在不同角度会呈现不同颜色。',
        'explanation_en': "Butterflies' beautiful colors come from a combination of pigments and structural colors! Structural colors create iridescent effects through light refraction, which is why wings appear different colors from different angles.",
        'category': 'butterfly',
        'difficulty': 'hard'
    },
    {
        'id': 7,
        'question': '哪种鸟类可以倒着飞？',
        'question_en': 'Which bird can fly backwards?',
        'options': ['A. 蜂鸟 (Hummingbird)', 'B. 燕子 (Swallow)', 'C. 老鹰 (Eagle)', 'D. 鸽子 (Pigeon)'],
        'answer': 'A',
        'explanation': '蜂鸟是唯一可以倒着飞的鸟类！牠们的翅膀可以前后摆动，这让牠们能在空中悬停和倒飞。',
        'explanation_en': 'Hummingbirds are the only birds that can fly backwards! Their wings can beat forward and backward, allowing them to hover and fly backwards.',
        'category': 'bird',
        'difficulty': 'easy'
    },
    {
        'id': 8,
        'question': '蝴蝶的幼虫叫什么？',
        'question_en': 'What is a butterfly larva called?',
        'options': ['A. 蛹 (Pupa)', 'B. 毛毛虫 (Caterpillar)', 'C. 若虫 (Nymph)', 'D. 幼鸟 (Chick)'],
        'answer': 'B',
        'explanation': '蝴蝶的幼虫叫做毛毛虫（caterpillar）！牠们会大量进食，然后变成蛹，最后羽化成美丽的蝴蝶。',
        'explanation_en': "A butterfly's larva is called a caterpillar! They eat voraciously, then become a pupa, and finally emerge as beautiful butterflies.",
        'category': 'butterfly',
        'difficulty': 'easy'
    },
    {
        'id': 9,
        'question': '鸟类中，哪种鸟的视力最好？',
        'question_en': 'Among birds, which has the best eyesight?',
        'options': ['A. 猫头鹰 (Owl)', 'B. 老鹰 (Eagle)', 'C. 乌鸦 (Crow)', 'D. 鸽子 (Pigeon)'],
        'answer': 'B',
        'explanation': '老鹰的视力是人类的8倍！牠们可以从3公里外看到一只兔子，这是牠们作为顶级捕食者的关键优势。',
        'explanation_en': "Eagles have 8 times better vision than humans! They can spot a rabbit from 3 km away - a key advantage as top predators.",
        'category': 'bird',
        'difficulty': 'medium'
    },
    {
        'id': 10,
        'question': '蝴蝶的翅膀上覆盖着什么？',
        'question_en': 'What covers a butterfly\'s wings?',
        'options': ['A. 羽毛', 'B. 鳞片', 'C. 毛发', 'D. 皮肤'],
        'options_en': ['A. Feathers', 'B. Scales', 'C. Hair', 'D. Skin'],
        'answer': 'B',
        'explanation': '蝴蝶的翅膀上覆盖着微小的鳞片！这些鳞片像屋顶的瓦片一样排列，赋予蝴蝶美丽的颜色和图案。如果触摸蝴蝶翅膀，这些鳞片会脱落。',
        'explanation_en': "Butterfly wings are covered with tiny scales! These scales are arranged like roof tiles, giving butterflies their beautiful colors and patterns. If you touch a butterfly's wings, these scales will come off.",
        'category': 'butterfly',
        'difficulty': 'medium'
    }
]


def get_random_quiz(category=None, difficulty=None):
    """
    随机获取一道题目
    
    Args:
        category: 'bird' 或 'butterfly'，None表示不限制
        difficulty: 'easy', 'medium', 'hard'，None表示不限制
    
    Returns:
        随机选择的题目字典
    """
    import random
    
    filtered_quizzes = QUIZ_LIBRARY
    
    if category:
        filtered_quizzes = [q for q in filtered_quizzes if q.get('category') == category]
    
    if difficulty:
        filtered_quizzes = [q for q in filtered_quizzes if q.get('difficulty') == difficulty]
    
    if not filtered_quizzes:
        filtered_quizzes = QUIZ_LIBRARY
    
    return random.choice(filtered_quizzes)


def format_quiz_message(quiz, language='en'):
    """
    格式化题目为对话消息（支持双语）
    
    Args:
        quiz: 题目字典
        language: 'zh' 或 'en'
    
    Returns:
        格式化后的题目字符串
    """
    if language == 'zh':
        question = quiz.get('question', quiz.get('question_en', ''))
        options = quiz.get('options', quiz.get('options_en', []))
        challenge_label = "🎯 **小挑战来了！**"
        think_prompt = "\n\n💭 想一想，然后告诉我你的答案（A/B/C/D）！"
    else:
        question = quiz.get('question_en', quiz.get('question', ''))
        options = quiz.get('options_en', quiz.get('options', []))
        challenge_label = "🎯 **Little Challenge!**"
        think_prompt = "\n\n💭 Think about it, then tell me your answer (A/B/C/D)!"
    
    message = f"{challenge_label}\n\n{question}\n\n"
    message += "\n".join(options)
    message += think_prompt
    
    return message


def check_quiz_answer(quiz, user_answer, language='en'):
    """
    检查用户答案是否正确（支持双语）
    
    Args:
        quiz: 题目字典
        user_answer: 用户答案（'A', 'B', 'C', 或 'D'）
        language: 用户语言偏好 ('zh' 或 'en')
    
    Returns:
        (is_correct: bool, feedback: str)
    """
    correct_answer = quiz.get('answer', '').upper()
    user_answer = user_answer.strip().upper()
    
    is_correct = user_answer == correct_answer
    
    if language == 'zh':
        explanation = quiz.get('explanation', quiz.get('explanation_en', ''))
        if is_correct:
            feedback = f"🎉 太棒了！答对了！\n\n{explanation}"
        else:
            feedback = f"❌ 很接近，但正确答案是 {correct_answer}。\n\n{explanation}\n\n别灰心，继续加油！"
    else:
        explanation = quiz.get('explanation_en', quiz.get('explanation', ''))
        if is_correct:
            feedback = f"🎉 Excellent! You got it right!\n\n{explanation}"
        else:
            feedback = f"❌ Close, but the correct answer is {correct_answer}.\n\n{explanation}\n\nDon't give up, keep trying!"
    
    return is_correct, feedback

