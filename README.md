# Personal Portfolio Chatbot

A fully animated, responsive personal portfolio website with an AI chatbot assistant. Features include portfolio cards, project showcase, and a Flask backend with NLP-powered chat functionality.

## Features

### Frontend
- ✨ **Fully Animated UI** - Smooth fade-ins, slide-ups, zoom animations
- 📱 **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- 💬 **Chat Interface** - Beautiful floating chat button with modal
- 🎨 **Modern Design** - Gradient backgrounds, card layouts, smooth transitions
- 🌙 **Dark Mode Support** - Automatic dark mode detection
- 📦 **Portfolio Sections**:
  - Hero Section with CTA
  - About Me Cards
  - Skills with Flip Animations
  - Projects Portfolio
  - Contact Information

### Backend
- 🤖 **NLP Chat Engine** - Intent-based response system
- 🔌 **RESTful API** - Easy-to-integrate endpoints
- 📊 **Personal Data Management** - Centralized knowledge base
- 🚀 **CORS Support** - Seamless frontend-backend communication
- 💾 **Extensible Architecture** - Easy to add more intents and data

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- A modern web browser

### Installation

1. **Clone or Navigate to Project**
   ```bash
   cd practice_session
   ```

2. **Create a Virtual Environment** (Optional but Recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key** (optional for richer GPT-style replies)
   - Windows PowerShell:
     ```powershell
     $env:OPENAI_API_KEY="your_openai_api_key"
     ```
   - macOS/Linux:
     ```bash
     export OPENAI_API_KEY="your_openai_api_key"
     ```

### Running the Application

#### Start the Backend (Flask Server)
```bash
python app.py
```

The backend will start at: `http://localhost:5000`

You should see:
```
==================================================
Personal Chatbot Backend Starting...
==================================================
✓ Loaded 12 intents
✓ Personal data loaded: John Doe

📍 API running at: http://localhost:5000
📍 Chat endpoint: http://localhost:5000/api/chat

✓ CORS enabled for frontend communication
==================================================
```

#### Open the Frontend
1. Open `index.html` in your web browser
   - Direct file: `file:///path/to/practice_session/index.html`
   - Or use a local server:
     ```bash
     # Python 3
     python -m http.server 8000
     
     # Then visit: http://localhost:8000
     ```

## Usage

### Chatting with the Bot

1. **Click the Chat Button** - The floating purple button in the bottom-right corner
2. **Type Your Message** - Ask questions about skills, projects, experience, etc.
3. **Send** - Press Enter or click the send button
4. **Get Responses** - The bot uses NLP to understand and respond

### Example Questions
- "Hello! What's your name?"
- "Tell me about yourself"
- "What are your skills?"
- "Show me your projects"
- "How can I contact you?"
- "What experience do you have?"

### Keyboard Shortcuts
- **Ctrl+K** (or **Cmd+K** on Mac) - Focus the chat input
- **Escape** - Close the chat modal
- **Enter** - Send message

## API Endpoints

### POST `/api/chat`
Send a message and get a response

**Request:**
```json
{
    "message": "What are your skills?"
}
```

**Response:**
```json
{
    "response": "My key skills include...",
    "intent": "skills",
    "confidence": 0.95
}
```

### GET `/api/info`
Get all personal information

**Response:**
```json
{
    "name": "John Doe",
    "title": "Full Stack Developer",
    "email": "john.doe@example.com",
    ...
}
```

### GET `/api/projects`
Get list of projects

### GET `/api/skills`
Get skills by category

### GET `/api/health`
Health check endpoint

## Customization

### Update Personal Information

Edit the `personal_data` dictionary in `app.py`:

```python
personal_data = {
    "name": "Your Name",
    "title": "Your Title",
    "email": "your.email@example.com",
    "phone": "+1 (555) 123-4567",
    "location": "Your Location",
    # ... more fields
}
```

### Add New Intents

Add new intents to the `intents` dictionary in `app.py`:

```python
intents = {
    # ... existing intents
    "hobby": {
        "patterns": ["your hobby", "hobbies", "do you have hobbies"],
        "responses": [
            "I love coding, reading tech blogs, and contributing to open source!"
        ]
    }
}
```

### Customize Frontend

- **Colors**: Edit CSS variables in `style.css`
  ```css
  :root {
      --primary-color: #6366f1;
      --secondary-color: #ec4899;
      /* ... */
  }
  ```

- **Content**: Edit sections in `index.html`
- **Portfolio Data**: Update project cards and skills

## File Structure

```
practice_session/
├── index.html       # Main HTML file with portfolio sections
├── style.css        # All styling and animations
├── script.js        # Frontend JavaScript and chat logic
├── app.py           # Flask backend with NLP
├── requirements.txt # Python dependencies
├── README.md        # This file
└── main.py          # (Optional) Alternative entry point
```

## Technical Stack

### Frontend
- HTML5
- CSS3 (with animations and transitions)
- Vanilla JavaScript (ES6+)
- Font Awesome Icons

### Backend
- Python 3.7+
- Flask (Web Framework)
- Flask-CORS (Cross-Origin Support)
- difflib (String Similarity for NLP)

## Browser Support

- ✅ Chrome/Edge (Latest)
- ✅ Firefox (Latest)
- ✅ Safari (Latest)
- ✅ Mobile Browsers (iOS Safari, Chrome Mobile)

## Responsive Breakpoints

- 📱 Mobile: < 480px
- 📱 Tablet: 480px - 768px
- 🖥️ Desktop: > 768px

## Features by Device

### Mobile
- Optimized chat modal (90% width)
- Responsive navigation
- Touch-friendly buttons
- Stacked layout for sections

### Tablet
- Medium chat modal (60% width)
- Grid layouts adapt gracefully

### Desktop
- Full-featured interface
- Side-by-side sections
- Hover effects on cards

## NLP Engine Details

The chatbot uses **intent matching** with the following approach:

1. **Pattern Matching** - Compares user input against predefined patterns
2. **String Similarity** - Uses difflib for fuzzy matching
3. **Confidence Scoring** - Returns matches with > 0.6 confidence
4. **Fallback Response** - Default response if no match found

### Extending NLP

For more advanced NLP, consider:
- NLTK (Natural Language Toolkit)
- spaCy
- Rasa
- Hugging Face Transformers

## Troubleshooting

### Backend Won't Start
```bash
# Ensure Flask is installed
pip install Flask Flask-CORS

# Check Python version
python --version  # Should be 3.7+

# Check port 5000 availability
netstat -an | grep 5000
```

### CORS Errors
- Ensure `Flask-CORS` is installed
- Check that backend is running on localhost:5000
- Verify API_URL in script.js matches backend URL

### Chat Not Working
1. Open browser console (F12)
2. Check Network tab for API requests
3. Ensure backend is running and accessible
4. Verify CORS headers in responses

## Performance Tips

- Chat modal uses CSS transforms for smooth animations
- Lazy loading of personal data
- Optimized asset delivery
- Mobile-first responsive design

## Future Enhancements

- 🔒 Authentication system
- 💾 Chat history persistence
- 🎙️ Voice input/output
- 🌐 Multi-language support
- 📊 Analytics dashboard
- 🔗 Integration with LinkedIn/GitHub API
- 🤖 Advanced AI/ML models

## License

Free to use and modify for personal projects.

## Support

For issues or questions:
1. Check this README
2. Review code comments
3. Check browser console for errors
4. Verify backend is running

---

**Created with ❤️ for your portfolio**

Last Updated: 2026
Version: 1.0
