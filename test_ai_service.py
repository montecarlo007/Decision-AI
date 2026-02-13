from apps.ai_core.services import OllamaService
import os
import json

def test_ai():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
        
    ai = OllamaService()
    test_text = "The Internet of Things (IoT) describes the network of physical objects—'things'—that are embedded with sensors, software, and other technologies for the purpose of connecting and exchanging data with other devices and systems over the internet."
    
    print("--- Testing Summary Generation ---")
    try:
        summary = ai.generate_summary(test_text)
        print(f"Summary Response Type: {type(summary)}")
        print(json.dumps(summary, indent=2))
    except Exception as e:
        print(f"Summary Failed: {e}")

    print("\n--- Testing Quiz Generation ---")
    try:
        quiz = ai.generate_quiz(test_text)
        print(f"Quiz Response Type: {type(quiz)}")
        print(json.dumps(quiz, indent=2))
    except Exception as e:
        print(f"Quiz Failed: {e}")

if __name__ == "__main__":
    test_ai()
