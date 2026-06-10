

from app import app, personal_data, intents, find_best_intent, get_response

# ============================================
# TESTING & CONFIGURATION
# ============================================

def test_chatbot():
    """
    Test the chatbot with sample queries
    Useful for debugging the NLP engine
    """
    print("\n" + "="*60)
    print("PERSONAL CHATBOT - NLP ENGINE TEST")
    print("="*60)
    
    test_queries = [
    # Greetings
    "Hi",
    "Hello",
    "Good morning",
    "Good evening",
    "How are you?",

    # Personal Information
    "Who are you?",
    "Introduce yourself",
    "Tell me about yourself",
    "What is your full name?",
    "What is your background?",
    "Where are you from?",
    "Where are you based?",
    "What do you do?",

    # Education
    "What is your education?",
    "Which college are you studying in?",
    "What degree are you pursuing?",
    "What is your CGPA?",
    "When will you graduate?",
    "What certifications do you have?",

    # Skills
    "What are your skills?",
    "What programming languages do you know?",
    "Do you know Python?",
    "Do you know Java?",
    "What databases have you worked with?",
    "What frontend technologies do you know?",
    "What backend technologies do you know?",
    "Do you know machine learning?",
    "Do you know cloud computing?",
    "What tools do you use?",

    # Experience
    "How many years of experience do you have?",
    "Do you have internship experience?",
    "Tell me about your work experience",
    "Have you worked in any company?",
    "What is your current role?",

    # Projects
    "What projects have you worked on?",
    "Tell me about your best project",
    "What is your indoor navigation project?",
    "Tell me about your chatbot project",
    "What machine learning projects have you done?",
    "Have you built mobile applications?",
    "What technologies did you use in your projects?",
    "Which project are you most proud of?",

    # Resume
    "Can I see your resume?",
    "What achievements do you have?",
    "What awards have you received?",
    "What are your strengths?",
    "What are your hobbies?",
    "What are your career goals?",

    # Contact
    "How can I contact you?",
    "What is your email address?",
    "Do you have LinkedIn?",
    "Do you have GitHub?",
    "Can I hire you?",
    "Are you available for work?",

    # Career
    "What job roles are you looking for?",
    "Are you open to internships?",
    "Are you interested in software development?",
    "Do you work on freelance projects?",
    "What are your future plans?",

    # Technical Questions
    "Explain your Python skills",
    "Explain your machine learning experience",
    "What frameworks do you use?",
    "Do you know React?",
    "Do you know Flask?",
    "Do you know SQL?",
    "Do you know MongoDB?",
    "Do you know data analysis?",

    # Fun Questions
    "What is your favorite programming language?",
    "Why should I hire you?",
    "What makes you unique?",
    "Can you help me with coding?",
    "Can you help me with projects?",
    "What are your interests?",
    "Tell me something interesting about yourself"
]
    
    print(f"\n✓ Loaded {len(intents)} intents")
    print(f"✓ Personal data: {personal_data['name']}")
    print("\n" + "-"*60)
    
    for query in test_queries:
        intent, confidence = find_best_intent(query)
        response = get_response(intent)
        
        print(f"\n📝 User: {query}")
        print(f"🎯 Intent: {intent} (Confidence: {confidence:.2%})")
        print(f"🤖 Bot: {response[:100]}..." if len(response) > 100 else f"🤖 Bot: {response}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60 + "\n")

def run_server():
    """
    Run the Flask server
    """
    print("\n" + "="*60)
    print("STARTING PERSONAL CHATBOT SERVER")
    print("="*60)
    print(f"✓ Initialized: {personal_data['name']}")
    print(f"✓ Intents loaded: {len(intents)}")
    print("\n🚀 Starting Flask server...")
    print("📍 Backend URL: http://localhost:5000")
    print("📍 Chat API: http://localhost:5000/api/chat")
    print("📍 Health Check: http://localhost:5000/api/health")
    print("\n✨ Frontend: Open index.html in your browser")
    print("🎙️ Keyboard Shortcut: Ctrl+K to focus chat")
    print("="*60 + "\n")
    
    app.run(debug=True, host='localhost', port=5000)

# ============================================
# COMMAND LINE INTERFACE
# ============================================

def interactive_chat():
    """
    Interactive CLI chat for testing
    """
    print("\n" + "="*60)
    print("INTERACTIVE CHATBOT - CLI MODE")
    print("="*60)
    print(f"Chatting with {personal_data['name']}")
    print("Type 'exit' to quit, 'help' for commands")
    print("="*60 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'exit':
            print("\nGoodbye! Thanks for chatting.")
            break
        elif user_input.lower() == 'help':
            print("\nAvailable commands:")
            print("  - Type any question to chat")
            print("  - 'exit' to quit")
            print("  - 'info' to see personal data")
            print("  - 'intents' to see available intents")
            print()
            continue
        elif user_input.lower() == 'info':
            print(f"\nName: {personal_data['name']}")
            print(f"Title: {personal_data['title']}")
            print(f"Email: {personal_data['email']}")
            print(f"Location: {personal_data['location']}")
            print(f"Experience: {personal_data['experience_years']} years")
            print()
            continue
        elif user_input.lower() == 'intents':
            print("\nAvailable intents:")
            for intent_name in intents.keys():
                print(f"  - {intent_name}")
            print()
            continue
        elif not user_input:
            continue
        
        # Process message
        intent, confidence = find_best_intent(user_input)
        response = get_response(intent)
        
        print(f"\nBot: {response}")
        if intent:
            print(f"[Intent: {intent}, Confidence: {confidence:.2%}]\n")
        else:
            print("[Intent: unknown]\n")

# ============================================
# MAIN MENU
# ============================================

def main_menu():
    """
    Interactive menu for different modes
    """
    while True:
        print("\n" + "="*60)
        print("PERSONAL CHATBOT - MAIN MENU")
        print("="*60)
        print("\n1. Run Web Server (Flask)")
        print("2. Interactive Chat (CLI)")
        print("3. Test NLP Engine")
        print("4. View Personal Data")
        print("5. Exit")
        print("\n" + "="*60)
        
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            run_server()
            break
        elif choice == '2':
            interactive_chat()
        elif choice == '3':
            test_chatbot()
        elif choice == '4':
            print("\n" + "="*60)
            print("PERSONAL DATA")
            print("="*60)
            import json
            print(json.dumps(personal_data, indent=2))
            print("="*60)
        elif choice == '5':
            print("\nExiting... Goodbye!")
            break
        else:
            print("\n❌ Invalid option. Please select 1-5.")

# ============================================
# ENTRY POINT
# ============================================

if __name__ == '__main__':
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'server':
            run_server()
        elif command == 'chat':
            interactive_chat()
        elif command == 'test':
            test_chatbot()
        elif command == 'info':
            import json
            print(json.dumps(personal_data, indent=2))
        elif command == 'help':
            print("""
Personal Chatbot - Usage:
  
  python main.py server    - Start Flask web server
  python main.py chat      - Interactive CLI chat
  python main.py test      - Test NLP engine
  python main.py info      - Show personal data
  python main.py           - Show menu (default)
  
To start the web server:
  python main.py server
  
Then open index.html in your browser.
            """)
        else:
            print(f"Unknown command: {command}\nRun 'python main.py help' for usage")
    else:
        # Show menu by default
        try:
            main_menu()
        except KeyboardInterrupt:
            print("\n\nExiting... Goodbye!")
