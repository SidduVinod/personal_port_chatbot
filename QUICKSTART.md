# 🚀 QUICK START GUIDE

## Personal Portfolio Chatbot - Setup & Run

Your fully animated personal chatbot web application is ready to use! Follow these simple steps:

---

## ⚡ QUICK START (2 Steps)

### Step 1: Start the Backend Server
Open PowerShell/Command Prompt in the `practice_session` folder and run:

```powershell
python app.py
```

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

**Keep this terminal open!** The server needs to keep running.

### Step 2: Open the Frontend
Open `index.html` in your web browser:
- Double-click the `index.html` file, OR
- Copy this path into your browser address bar:
  ```
  file:///c:/Users/UP60084224/Downloads/practice_session/index.html
  ```

---

## ✨ Features to Try

1. **Chat with the Bot** 🤖
   - Click the purple chat icon (bottom-right corner)
   - Type: "Hello" or "Tell me about yourself"
   - Press Enter to send

2. **Explore Portfolio** 📑
   - Scroll down to see sections
   - Click nav links to jump to sections
   - Hover over cards for animations

3. **Keyboard Shortcuts** ⌨️
   - `Ctrl+K` - Focus chat input
   - `Escape` - Close chat

---

## 📱 Responsive Design

The app works on:
- 🖥️ **Desktop** - Full features
- 💻 **Tablet** - Responsive layout
- 📱 **Mobile** - Optimized interface

---

## 🛠️ Alternative Modes

### Interactive CLI Chat (for testing)
```powershell
python main.py chat
```

### Test NLP Engine
```powershell
python main.py test
```

### Menu-Driven Mode
```powershell
python main.py
```

---

## 🎨 What You Get

### Frontend
✅ Animated hero section with gradient background
✅ Portfolio cards with hover effects  
✅ Skills with flip animations
✅ Projects showcase
✅ Contact information
✅ Floating chat button
✅ Responsive message interface
✅ Smooth animations & transitions
✅ Mobile-optimized layout

### Backend
✅ Flask API server
✅ NLP-based intent matching
✅ 12 pre-built chat intents
✅ Personal data management
✅ CORS-enabled for frontend access
✅ RESTful endpoints

---

## 🔧 Customize It

### Change Personal Information
Edit `app.py` - Look for `personal_data` dictionary:
```python
personal_data = {
    "name": "Your Name",
    "email": "your.email@example.com",
    "skills": {...}
    # ... customize here
}
```

### Add More Chat Intents
Edit `app.py` - Add to `intents` dictionary:
```python
"hobby": {
    "patterns": ["hobby", "hobbies", "interests"],
    "responses": ["I love coding and open source!"]
}
```

### Change Colors
Edit `style.css` - Update CSS variables:
```css
:root {
    --primary-color: #6366f1;      /* Purple */
    --secondary-color: #ec4899;    /* Pink */
}
```

---

## ❓ Troubleshooting

**Backend won't start?**
- Check Python is installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`
- Try different port if 5000 is in use

**Chat doesn't respond?**
- Check browser console (F12) for errors
- Ensure backend server is running
- Check Network tab to see API calls

**Frontend won't load?**
- Use full file path or local server
- Try: `python -m http.server 8000` then visit `localhost:8000`

**Issues with CORS?**
- Ensure Flask-CORS is installed
- Backend must run on `localhost:5000`

---

## 📊 API Endpoints

The backend provides these endpoints:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/chat` | Send message, get response |
| GET | `/api/info` | Get personal information |
| GET | `/api/projects` | Get projects list |
| GET | `/api/skills` | Get skills data |
| GET | `/api/health` | Health check |

---

## 🎯 Example Questions to Ask Bot

- "Hello!"
- "What is your name?"
- "Tell me about yourself"
- "What are your skills?"
- "How many years of experience do you have?"
- "What projects have you worked on?"
- "How can I contact you?"
- "Where are you located?"
- "What's your education?"

---

## 📚 Project Structure

```
practice_session/
├── index.html           # Frontend (portfolio + chat UI)
├── style.css            # Styling & animations
├── script.js            # Chat functionality
├── app.py               # Flask backend & NLP
├── main.py              # Alternative entry point
├── requirements.txt     # Python dependencies
├── README.md            # Full documentation
└── QUICKSTART.md        # This file
```

---

## 🎉 You're All Set!

1. ✅ Dependencies installed
2. ✅ Backend ready to run
3. ✅ Frontend ready to display
4. ✅ Chat system configured

**Now run the backend and open the frontend in your browser!**

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the full README.md
3. Check browser console for error messages
4. Ensure backend is running and accessible

---

**Version 1.0 | Created with ❤️**
