// ============================================
// CHAT APPLICATION JAVASCRIPT
// ============================================

const chatBtn = document.getElementById('chatBtn');
const chatModal = document.getElementById('chatModal');
const closeChat = document.getElementById('closeChat');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');
const chatMessages = document.getElementById('chatMessages');
const typingIndicator = document.getElementById('typingIndicator');

// Voice support state
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const speechSupported = !!SpeechRecognition;
const speechSynthesisSupported = 'speechSynthesis' in window;
let recognition = null;
let listening = false;

// Backend API URL
const API_URL = 'http://localhost:5000/api';

// ============================================
// EVENT LISTENERS
// ============================================

// Toggle chat modal
chatBtn.addEventListener('click', () => {
    chatModal.classList.toggle('active');
    if (chatModal.classList.contains('active')) {
        chatInput.focus();
    }
});

// Close chat
closeChat.addEventListener('click', () => {
    chatModal.classList.remove('active');
});

// Send message on button click
sendBtn.addEventListener('click', sendMessage);

// Voice input button
if (voiceBtn) {
    voiceBtn.addEventListener('click', () => {
        if (!speechSupported) {
            addMessage('Sorry, voice input is not supported in this browser.', 'bot');
            return;
        }
        if (listening) {
            stopVoiceRecognition();
        } else {
            startVoiceRecognition();
        }
    });
}

// Send message on Enter key
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Close chat when clicking outside
document.addEventListener('click', (e) => {
    if (!chatModal.contains(e.target) && !chatBtn.contains(e.target)) {
        if (chatModal.classList.contains('active')) {
            chatModal.classList.remove('active');
        }
    }
});

// ============================================
// MESSAGE HANDLING
// ============================================

function sendMessage() {
    const message = chatInput.value.trim();
    
    if (message === '') return;

    // Add user message to chat
    addMessage(message, 'user');

    // Clear input
    chatInput.value = '';

    // Show typing indicator
    showTypingIndicator();

    // Send message to backend
    fetchChatResponse(message);
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);

    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    
    const messageParagraph = document.createElement('p');
    messageParagraph.textContent = text;
    
    messageContent.appendChild(messageParagraph);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('message', 'bot-message');
    typingDiv.id = 'typing-msg';
    
    const typingContent = document.createElement('div');
    typingContent.classList.add('typing-indicator');
    
    for (let i = 0; i < 3; i++) {
        const span = document.createElement('span');
        typingContent.appendChild(span);
    }
    
    typingDiv.appendChild(typingContent);
    chatMessages.appendChild(typingDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const typingMsg = document.getElementById('typing-msg');
    if (typingMsg) {
        typingMsg.remove();
    }
}

function updateVoiceButton() {
    if (!voiceBtn) return;
    voiceBtn.classList.toggle('active', listening);
}

function startVoiceRecognition() {
    if (!SpeechRecognition) return;

    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
        listening = true;
        updateVoiceButton();
        addMessage('Listening... please speak clearly.', 'bot');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        chatInput.value = transcript;
        sendMessage();
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        addMessage('Voice input failed. Please try again or type your message.', 'bot');
        stopVoiceRecognition();
    };

    recognition.onend = () => {
        listening = false;
        updateVoiceButton();
    };

    recognition.start();
}

function stopVoiceRecognition() {
    if (recognition) {
        recognition.stop();
    }
    listening = false;
    updateVoiceButton();
}

function speakText(text) {
    if (!speechSynthesisSupported || !text) return;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    speechSynthesis.speak(utterance);
}

// ============================================
// BACKEND COMMUNICATION
// ============================================

async function fetchChatResponse(userMessage) {
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: userMessage
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add bot response
        if (data.response) {
            addMessage(data.response, 'bot');
            speakText(data.response);
        } else {
            addMessage('Sorry, I could not understand that. Please try again.', 'bot');
            speakText('Sorry, I could not understand that. Please try again.');
        }

    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        addMessage('Sorry, there was an error. Please try again later.', 'bot');
    }
}

// ============================================
// SMOOTH SCROLL FOR NAV LINKS
// ============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ============================================
// INTERSECTION OBSERVER FOR ANIMATIONS
// ============================================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe animation elements
document.querySelectorAll('.slide-up, .zoom-animation').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'all 0.6s ease-out';
    observer.observe(el);
});

// ============================================
// UTILITY FUNCTIONS
// ============================================

// Get personal info from backend
async function getPersonalInfo() {
    try {
        const response = await fetch(`${API_URL}/info`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching personal info:', error);
        // Fallback: try loading the saved JSON directly from uploads (served by Flask static)
        try {
            const fallback = await fetch('/uploads/personal_data.json');
            if (fallback.ok) {
                return await fallback.json();
            }
        } catch (err) {
            console.error('Fallback personal_data.json fetch failed:', err);
        }
        return null;
    }
}

// Initialize chat with welcome message on page load
window.addEventListener('load', () => {
    // Chat is initialized with a welcome message in HTML
    console.log('Personal Chat Bot loaded successfully');
    // populate contact and photo from backend
    populatePersonalInfo();
});

async function populatePersonalInfo() {
    const data = await getPersonalInfo();
    if (!data) return;

    renderContactCard(data);

    const photoEl = document.getElementById('profilePhoto');
    if (photoEl && data.photo) {
        // API_URL is like http://localhost:5000/api -> remove '/api'
        const base = API_URL.replace('/api', '');
        photoEl.src = base + data.photo;
    }
    const heroEl = document.getElementById('heroPhoto');
    if (heroEl && data.photo) {
        const base = API_URL.replace('/api', '');
        heroEl.src = base + data.photo;
    }
    const heroNameEl = document.getElementById('heroName');
    if (heroNameEl && data.name) {
        heroNameEl.textContent = data.name.toUpperCase();
    }
    const heroRoleEl = document.getElementById('heroRole');
    if (heroRoleEl && data.title) {
        heroRoleEl.textContent = data.title;
    }

    const aboutCards = document.querySelectorAll('.about-card p');
    if (aboutCards && aboutCards.length >= 3) {
        if (data.career_objective) {
            aboutCards[0].textContent = data.career_objective;
        }
        if (data.title) {
            aboutCards[1].textContent = `Role: ${data.title}`;
        }
        if (data.bio) {
            aboutCards[2].textContent = data.bio;
        }
    }

    if (data.education && Array.isArray(data.education)) {
        renderEducation(data.education);
    }

    if (data.internship) {
        renderInternship(data.internship);
    }

    if (data.projects && Array.isArray(data.projects)) {
        renderProjects(data.projects);
    }
}

function normalizePhoneLink(phone) {
    if (!phone) return '';
    return phone.replace(/[^+0-9]/g, '');
}

function renderContactCard(data) {
    const container = document.querySelector('.contact-info');
    if (!container) return;
    container.innerHTML = '';

    const card = document.createElement('div');
    card.className = 'contact-card contact-card--full slide-up';

    const contactRows = [
        {
            icon: 'fas fa-envelope',
            label: 'Email',
            value: data.email || 'Not available',
            href: data.email ? `mailto:${data.email}` : null
        },
        {
            icon: 'fas fa-phone',
            label: 'Phone',
            value: data.phone || 'Not available',
            href: data.phone ? `tel:${normalizePhoneLink(data.phone)}` : null
        },
        {
            icon: 'fas fa-map-marker-alt',
            label: 'Location',
            value: data.location || 'Not available',
            href: null
        }
    ];

    contactRows.forEach(item => {
        const row = document.createElement('div');
        row.className = 'contact-card-row';

        const icon = document.createElement('i');
        icon.className = item.icon;
        icon.setAttribute('aria-hidden', 'true');

        const label = document.createElement('span');
        label.className = 'contact-card-label';
        label.textContent = `${item.label}:`;

        let valueElement;
        if (item.href) {
            const link = document.createElement('a');
            link.className = 'contact-link';
            link.href = item.href;
            link.textContent = item.value;
            if (item.label === 'Email' || item.label === 'Recruiter') {
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
            }
            valueElement = link;
        } else {
            valueElement = document.createElement('p');
            valueElement.textContent = item.value;
        }

        const text = document.createElement('div');
        text.style.display = 'flex';
        text.style.flexDirection = 'column';
        text.style.gap = '0.25rem';
        text.appendChild(label);
        text.appendChild(valueElement);

        row.appendChild(icon);
        row.appendChild(text);
        card.appendChild(row);
    });

    container.appendChild(card);
}

function renderEducation(education) {
    const container = document.getElementById('educationContent');
    if (!container) return;
    container.innerHTML = '';

    education.forEach(item => {
        const card = document.createElement('div');
        card.className = 'education-card slide-up';

        const title = document.createElement('h3');
        title.textContent = item.degree || item.title || 'Education';

        const institution = document.createElement('p');
        institution.textContent = item.institution || item.university || '';

        const details = document.createElement('p');
        const year = item.graduation_year ? `Class of ${item.graduation_year}` : '';
        const score = item.cgpa ? `CGPA: ${item.cgpa}` : item.percentage ? `Score: ${item.percentage}` : '';
        details.textContent = [year, score].filter(Boolean).join(' • ');

        card.appendChild(title);
        card.appendChild(institution);
        if (details.textContent) card.appendChild(details);
        container.appendChild(card);
    });
}

function renderInternship(internship) {
    const container = document.getElementById('internshipContent');
    if (!container) return;
    container.innerHTML = '';

    const card = document.createElement('div');
    card.className = 'education-card slide-up';

    const title = document.createElement('h3');
    title.textContent = internship.company || 'Internship Experience';

    const summary = document.createElement('p');
    const pieces = [];
    if (internship.duration) pieces.push(internship.duration);
    if (internship.domain) pieces.push(internship.domain);
    summary.textContent = pieces.join(' • ');

    const desc = document.createElement('p');
    desc.textContent = internship.description || internship.role || '';

    card.appendChild(title);
    if (summary.textContent) card.appendChild(summary);
    if (desc.textContent) card.appendChild(desc);

    if (Array.isArray(internship.responsibilities) && internship.responsibilities.length) {
        const list = document.createElement('ul');
        internship.responsibilities.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            list.appendChild(li);
        });
        card.appendChild(list);
    }

    container.appendChild(card);
}

function renderProjects(projects) {
    const grid = document.querySelector('.projects-grid');
    if (!grid) return;
    // Clear existing projects
    grid.innerHTML = '';

    projects.forEach(p => {
        const card = document.createElement('div');
        card.className = 'project-card zoom-animation';

        const header = document.createElement('div');
        header.className = 'project-header';
        header.innerHTML = '<i class="fas fa-folder"></i>';

        const title = document.createElement('h3');
        title.textContent = p.name || p.title || 'Untitled Project';

        const desc = document.createElement('p');
        desc.textContent = p.description || p.desc || '';

        const tags = document.createElement('div');
        tags.className = 'project-tags';
        const techs = p.technologies || p.tags || [];
        techs.forEach(t => {
            const span = document.createElement('span');
            span.textContent = t;
            tags.appendChild(span);
        });

        card.appendChild(header);
        card.appendChild(title);
        card.appendChild(desc);
        if (techs.length) card.appendChild(tags);

        grid.appendChild(card);
    });
}

// Upload photo handler
const uploadPhotoBtn = document.getElementById('uploadPhotoBtn');
if (uploadPhotoBtn) {
    uploadPhotoBtn.addEventListener('click', async () => {
        const input = document.getElementById('photoInput');
        if (!input || !input.files || input.files.length === 0) {
            alert('Please select a photo file first');
            return;
        }
        const file = input.files[0];
        const fd = new FormData();
        fd.append('photo', file);

        try {
            const res = await fetch(`${API_URL.replace('/api','')}/api/upload_photo`.replace('/api/api','/api'), {
                method: 'POST',
                body: fd
            });
            const json = await res.json();
            if (json.photo) {
                const base = API_URL.replace('/api', '');
                document.getElementById('profilePhoto').src = base + json.photo;
                alert('Photo uploaded successfully');
            } else {
                alert('Upload failed');
            }
        } catch (err) {
            console.error(err);
            alert('Error uploading photo');
        }
    });
}

// Upload resume handler
const uploadResumeBtn = document.getElementById('uploadResumeBtn');
if (uploadResumeBtn) {
    uploadResumeBtn.addEventListener('click', async () => {
        const input = document.getElementById('resumeInput');
        if (!input || !input.files || input.files.length === 0) {
            alert('Please select a resume file first (DOCX)');
            return;
        }
        const file = input.files[0];
        const fd = new FormData();
        fd.append('resume', file);

        try {
            const res = await fetch(`${API_URL.replace('/api','')}/api/upload_resume`.replace('/api/api','/api'), {
                method: 'POST',
                body: fd
            });
            const json = await res.json();
            if (json.status === 'ok' && json.personal_data) {
                // update UI
                populatePersonalInfo();
                alert('Resume uploaded and parsed successfully');
            } else {
                alert('Failed to parse resume');
            }
        } catch (err) {
            console.error(err);
            alert('Error uploading resume');
        }
    });
}

// ============================================
// RESPONSIVE ADJUSTMENTS
// ============================================

// Adjust chat modal on window resize
window.addEventListener('resize', () => {
    const width = window.innerWidth;
    
    if (width <= 768) {
        // Mobile adjustments are handled by CSS media queries
        if (chatModal.classList.contains('active')) {
            chatInput.focus();
        }
    }
});

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

// Ctrl/Cmd + K to focus chat input
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        if (!chatModal.classList.contains('active')) {
            chatModal.classList.add('active');
        }
        chatInput.focus();
    }
    
    // Escape to close chat
    if (e.key === 'Escape' && chatModal.classList.contains('active')) {
        chatModal.classList.remove('active');
    }
});

console.log('Chat Bot JavaScript loaded. Press Ctrl+K (or Cmd+K) to focus chat.');
