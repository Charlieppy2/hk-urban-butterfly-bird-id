"""
AI Assistant Training Script
This script helps you train and improve the AI assistant's knowledge base
"""

import json
import os
from collections import defaultdict

KNOWLEDGE_BASE_PATH = 'knowledge_base.json'
TRAINING_DATA_PATH = 'training_data.json'

def load_knowledge_base():
    """Load existing knowledge base"""
    if os.path.exists(KNOWLEDGE_BASE_PATH):
        with open(KNOWLEDGE_BASE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_knowledge_base(kb):
    """Save knowledge base to file"""
    with open(KNOWLEDGE_BASE_PATH, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    print(f"Knowledge base saved to {KNOWLEDGE_BASE_PATH}")

def add_training_example(category, question, answer):
    """Add a new training example"""
    kb = load_knowledge_base()
    
    if category not in kb:
        kb[category] = {
            "patterns": [],
            "responses": []
        }
    
    # Add question as pattern (convert to lowercase keywords)
    keywords = extract_keywords(question)
    for keyword in keywords:
        if keyword not in kb[category]["patterns"]:
            kb[category]["patterns"].append(keyword)
    
    # Add answer as response
    if answer not in kb[category]["responses"]:
        kb[category]["responses"].append(answer)
    
    save_knowledge_base(kb)
    print(f"Added training example to category: {category}")

def extract_keywords(text):
    """Extract keywords from text - Supports both English and Chinese"""
    import re
    
    # Simple keyword extraction (remove common words)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'where', 'when', 'why', 'how'}
    
    # Check if text contains Chinese characters
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', text))
    
    if has_chinese:
        # For Chinese, extract Chinese characters and key English words
        # Extract Chinese characters (2-4 characters)
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        # Extract English words
        english_words = text.lower().split()
        english_keywords = [w for w in english_words if w not in stop_words and len(w) > 2 and not re.search(r'[\u4e00-\u9fff]', w)]
        return chinese_words + english_keywords
    else:
        # For English, extract keywords normally
        words = text.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords

def train_from_file(training_file):
    """Train assistant from a JSON file with Q&A pairs"""
    if not os.path.exists(training_file):
        print(f"Training file {training_file} not found!")
        return
    
    with open(training_file, 'r', encoding='utf-8') as f:
        training_data = json.load(f)
    
    for item in training_data:
        category = item.get('category', 'default')
        question = item.get('question', '')
        answer = item.get('answer', '')
        
        if question and answer:
            add_training_example(category, question, answer)
            print(f"Trained: {question[:50]}...")

def create_training_template():
    """Create a template file for training data"""
    template = [
        {
            "category": "identification_tips",
            "question": "How can I identify butterflies?",
            "answer": "To identify butterflies, look at wing patterns, colors, body shape, and habitat."
        },
        {
            "category": "observation_time",
            "question": "When is the best time to see birds?",
            "answer": "Early morning (6-9 AM) is usually the best time to observe birds."
        }
    ]
    
    with open('training_template.json', 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    
    print("Created training_template.json - add your Q&A pairs here!")

def show_statistics():
    """Show statistics about the knowledge base"""
    kb = load_knowledge_base()
    
    print("\n" + "="*50)
    print("AI Assistant Knowledge Base Statistics")
    print("="*50)
    
    total_patterns = 0
    total_responses = 0
    
    for category, data in kb.items():
        patterns = len(data.get('patterns', []))
        responses = len(data.get('responses', []))
        total_patterns += patterns
        total_responses += responses
        
        print(f"\n{category.upper()}:")
        print(f"  Patterns: {patterns}")
        print(f"  Responses: {responses}")
    
    print(f"\n{'='*50}")
    print(f"Total Categories: {len(kb)}")
    print(f"Total Patterns: {total_patterns}")
    print(f"Total Responses: {total_responses}")
    print("="*50)

def interactive_training():
    """Interactive mode for training"""
    print("\n" + "="*50)
    print("AI Assistant Interactive Training")
    print("="*50)
    print("\nCommands:")
    print("  add        - Add a new Q&A pair")
    print("  stats      - Show statistics (also: status, stat)")
    print("  load <file>- Load training data from file")
    print("  template   - Create training template")
    print("  help       - Show this help message")
    print("  quit       - Exit training mode (also: exit, q)")
    print("="*50 + "\n")
    
    kb = load_knowledge_base()
    
    while True:
        try:
            command = input("Enter command: ").strip().lower()
            
            # Remove any trailing backslashes or spaces
            command = command.rstrip('\\').strip()
            
            # Command aliases
            if command in ['quit', 'exit', 'q']:
                print("\n✓ Training session ended. Goodbye!")
                break
            elif command in ['stats', 'status', 'stat']:
                show_statistics()
            elif command == 'template':
                create_training_template()
            elif command.startswith('load '):
                filename = command.split(' ', 1)[1].strip()
                if filename:
                    train_from_file(filename)
                else:
                    print("✗ Please specify a filename: load <filename>")
            elif command == 'add':
                print("\n" + "-"*50)
                print("Add Training Example")
                print("-"*50)
                print("Available categories:")
                print("  greetings, identification_tips, observation_time, photo_tips,")
                print("  species_info, confidence, habitat, system_info, help, default")
                print("-"*50)
                category = input("\nCategory: ").strip()
                if not category:
                    print("✗ Category is required!")
                    continue
                    
                print("\n💡 Tip: Question can be in Chinese or English, but answer must be in English!")
                question = input("Question (中文/English): ").strip()
                if not question:
                    print("✗ Question is required!")
                    continue
                    
                answer = input("Answer (English only): ").strip()
                if not answer:
                    print("✗ Answer is required!")
                    continue
                
                add_training_example(category, question, answer)
                print("\n✓ Training example added successfully!")
                print("-"*50 + "\n")
            elif command == 'help' or command == 'h':
                print("\n" + "="*50)
                print("AI Assistant Interactive Training - Help")
                print("="*50)
                print("\nCommands:")
                print("  add        - Add a new Q&A pair")
                print("  stats      - Show knowledge base statistics")
                print("  load <file>- Load training data from JSON file")
                print("  template   - Create a training template file")
                print("  help       - Show this help message")
                print("  quit       - Exit training mode")
                print("\nExamples:")
                print("  add                    - Add a new Q&A pair interactively")
                print("  load training_data.json - Load training data from file")
                print("  stats                  - Show current statistics")
                print("="*50 + "\n")
            elif command == '':
                # Empty command, just continue
                continue
            else:
                print(f"✗ Unknown command: '{command}'")
                print("  Type 'help' for available commands, or 'quit' to exit.")
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user. Type 'quit' to exit or continue with commands.")
        except EOFError:
            print("\n\n⚠️  End of input. Exiting...")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("  Please try again or type 'quit' to exit.")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'template':
            create_training_template()
        elif sys.argv[1] == 'stats':
            show_statistics()
        elif sys.argv[1] == 'train' and len(sys.argv) > 2:
            train_from_file(sys.argv[2])
        else:
            print("Usage:")
            print("  python train_assistant.py template  - Create training template")
            print("  python train_assistant.py stats      - Show statistics")
            print("  python train_assistant.py train <file> - Train from file")
            print("  python train_assistant.py           - Interactive mode")
    else:
        interactive_training()

