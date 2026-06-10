"""
Personal Chatbot Backend - Flask Application
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import difflib
import json
from datetime import datetime
import os
import re
from docx import Document

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

personal_data = {
    "name": "SIDDARAJU T",
    "title": "Full Stack Developer",
    "email": "siddunayak604@gmail.com",
    "phone": "+91 8151042840",
    "date_of_birth": "24-08-2003",
    "location": "Bangalore, INDIA",
    "degree": "Bachelor of Science in Computer Science",
    "BE_university": "VTU University",
    "BE_institution": "RVITM",
    "DIPLOMA_institution": "JSS POLYTECHNIC NANJANGUD ",
    "BE_graduation_year": 2026,
    "BE_CGpa": "7.62",
    "bio": "I'm a passionate full-stack developer with expertise in Python, JavaScript, and web technologies. I love building scalable applications and solving complex problems.",
    "experience_years": "6 months",
    "skills": {
        "programming_languages": ["Python", "JavaScript", "HTML5", "CSS3", "SQL"],
        "languages": ["Python", "JavaScript", "HTML5", "CSS3", "SQL"],
        "frameworks": ["Flask", "Django", "React", "Node.js", "FastAPI"],
        "databases": ["PostgreSQL", "MongoDB", "Firebase", "MySQL"],
        "tools": ["Git", "Docker", "AWS", "Linux", "Jupyter Notebook"]
    },
    "education": {
        "degree": "Bachelor of Science in Computer Science",
        "BE_university": "VTU University",
        "BE_institution": "RVITM",
        "BE_graduation_year": 2026,
        "cgpa": "7.62",
        "diploma_institution": "JSS POLYTECHNIC NANJANGUD ",
        "DIPLOMA_graduation_year": 2023,
        "DIPLOMA_cgpa": "7.3",
        "DIPLOMA_degree": "Diploma in Computer Science",
        "DIPLOMA_university": "DEPARTMENT OF TECHNICAL EDUCATION, KARNATAKA",
        "DIPLOMA_institution": "JSS POLYTECHNIC NANJANGUD ",
        "sslc_institution": "GOVT HIGH SCHOOL CHIKKATI",
        "sslc_university": "KARNATAKA SECONDARY EDUCATION EXAMINATION BOARD",
        "sslc_graduation_year": 2019,
        "sslc_percentage": "84.64"
    },
    "projects": [
        {
            "name": "CSE CHAT-BOT",
            "description": "Natural Language Processing chatbot with intelligent responses",
            "technologies": ["Python", "JavaScript", "Flask", "MongoDB", "NLP"]
        },
        {
            "name": "ATTENDENCE MANAGEMENT SYSTEM",
            "description": "A web application for tracking and managing attendance.",
            "technologies": ["JAVA", "HTML", "CSS", "MySQL"]
        },
        {
            "name": "AR INDOOR NAVIGATION",
            "description": "Real-time indoor navigation system using Augmented Reality.",
            "technologies": ["ARCore", "Unity", "C#", "Computer Vision"]
        }
    ],
    "career_objective": "student of computer science with a strong interest in full-stack development, AI, and automation.",
    "education": [
        {
            "degree": "Bachelor of Science in Computer Science",
            "institution": "RVITM",
            "university": "VTU University",
            "graduation_year": 2026,
            "cgpa": "7.62"
        },
        {
            "DIPLOMA_degree": "Diploma in Computer Science",
            "institution": "JSS Polytechnic Nanjangud",
            "university": "Department of Technical Education, Karnataka",
            "graduation_year": 2023,
            "cgpa": "7.30"
        },
        {
            "HIGH_SCHOOL": "SSLC",
            "institution": "Govt High School Chikkati",
            "university": "Karnataka Secondary Education Examination Board",
            "graduation_year": 2019,
            "percentage": "84.64"
        }
    ],
    "projects": [
        {
            "name": "CSE CHAT-BOT",
            "description": "Natural Language Processing chatbot with intelligent responses",
            "technologies": ["Python", "JavaScript", "Flask", "MongoDB", "NLP"]
        },
        {
            "name": "ATTENDENCE MANAGEMENT SYSTEM",
            "description": "A web application for tracking and managing attendance.",
            "technologies": ["JAVA", "HTML", "CSS", "MySQL"]
        },
        {
            "name": "AR INDOOR NAVIGATION",
            "description": "Real-time indoor navigation system using Augmented Reality.",
            "technologies": ["ARCore", "Unity", "C#", "Computer Vision"]
        }
    ],
    "internship": {
        "company": "",
        "duration": "",
        "domain": "",
        "description": "",
        "responsibilities": []
    },
    "certifications": [],
    "achievements": [],
    "languages_known": [],
    "social_links": {
        "github": "https://github.com/SidduVinod",
        "linkedin": "https://linkedin.com",
        "twitter": "https://twitter.com"
    },
    "photo": None
}

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

pd_path = os.path.join(UPLOAD_DIR, "personal_data.json")
if os.path.exists(pd_path):
    try:
        with open(pd_path, "r", encoding="utf-8") as f:
            saved = json.load(f)
            personal_data.update(saved)
    except Exception:
        pass

if not personal_data.get("photo"):
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        profile_path = os.path.join(UPLOAD_DIR, f"profile{ext}")
        if os.path.exists(profile_path):
            personal_data["photo"] = f"/uploads/profile{ext}"
            break


def get_skills_languages():
    skills = personal_data.get("skills", {})
    return skills.get("programming_languages") or skills.get("languages") or []


def get_education():
    education = personal_data.get("education", {})

    if isinstance(education, list) and len(education) > 0:
        return education[0]

    if isinstance(education, dict):
        return education

    return {}


def get_education_text():
    education = personal_data.get("education", [])
    if isinstance(education, dict):
        education = [education]

    if education:
        summary = []
        for edu in education[:2]:
            degree = edu.get("degree", "Computer Science")
            institution = edu.get("institution") or edu.get("university") or "my university"
            year = edu.get("graduation_year", "N/A")
            cgpa = edu.get("cgpa")
            if cgpa:
                summary.append(f"{degree} from {institution} with CGPA {cgpa}, class of {year}.")
            else:
                summary.append(f"{degree} from {institution}, class of {year}.")
        return " ".join(summary)

    return "I have a strong academic background in computer science and related fields."


def get_projects_text():
    projects = personal_data.get("projects", [])
    if not isinstance(projects, list):
        return "I have built several projects that demonstrate my technical skills."

    text = "I've worked on these projects:\n\n"
    for i, project in enumerate(projects, start=1):
        tech = ", ".join(project.get("technologies", []))
        desc = project.get("description") or project.get("role") or ""
        text += f"{i}. {project.get('name')}\n"
        if desc:
            text += f"   {desc}\n"
        if tech:
            text += f"   Technologies: {tech}\n"
        text += "\n"

    return text.strip()


def get_education_breakdown_text():
    education_entries = personal_data.get("education", [])
    if isinstance(education_entries, dict):
        education_entries = [education_entries]

    if not education_entries:
        return "I have a strong academic background in computer science and related technologies."

    summary_lines = []
    for entry in education_entries:
        degree = entry.get("degree", "Education")
        institution = entry.get("institution") or entry.get("university") or "my institution"
        year = entry.get("graduation_year")
        cgpa = entry.get("cgpa")
        line = f"{degree} from {institution}"
        if year:
            line += f", class of {year}"
        if cgpa:
            line += f" with CGPA {cgpa}"
        summary_lines.append(line + ".")

    return " ".join(summary_lines)


def get_education_detail_text(topic):
    topic = topic.lower()
    education_entries = personal_data.get("education", [])
    if isinstance(education_entries, dict):
        education_entries = [education_entries]

    matched = [entry for entry in education_entries if topic in entry.get("degree", "").lower() or topic in entry.get("institution", "").lower() or topic in entry.get("university", "").lower()]

    if matched:
        entry = matched[0]
        degree = entry.get("degree", "Education")
        institution = entry.get("institution") or entry.get("university") or "my institution"
        year = entry.get("graduation_year")
        cgpa = entry.get("cgpa")
        details = f"{degree} from {institution}"
        if year:
            details += f", class of {year}"
        if cgpa:
            details += f" with CGPA {cgpa}"
        return details + "."

    return get_education_breakdown_text()


def find_project_by_message(user_message):
    if not user_message:
        return None

    query = user_message.lower()
    projects = personal_data.get("projects", [])
    if not isinstance(projects, list):
        return None

    for project in projects:
        name = project.get("name", "").lower()
        if name and name in query:
            return project

    best_match = None
    best_score = 0
    for project in projects:
        name = project.get("name", "").lower()
        score = difflib.SequenceMatcher(None, query, name).ratio()
        if score > best_score:
            best_score = score
            best_match = project

    return best_match if best_score > 0.4 else None


def get_project_detail_text(project):
    if not project:
        return "I have built several projects\n, including applications for attendance management\n, chatbot systems, and augmented reality navigation."

    tech = ", ".join(project.get("technologies", []))
    desc = project.get("description") or "This project was built to demonstrate my technical skills."
    details = f"{project.get('name')} is {desc}"
    if tech:
        details += f" Technologies used: {tech}."
    return details


def get_resume_summary_text():
    objective = personal_data.get("career_objective") or personal_data.get("bio") or "I am a motivated developer."
    education_text = get_education_breakdown_text()
    project_text = get_projects_text().split("\n\n")[0]
    return f"{objective} {education_text} Here are few highlighted projects: {project_text}."


def get_skill_project_recommendations(skill_topic):
    topic = skill_topic.lower()
    if "machine" in topic or "learning" in topic:
        return (
            "Yes, I know machine learning. I can work with concepts like supervised learning, NLP, and data preprocessing. "
            "A few project ideas I can recommend are:\n"
            "1. Build an intelligent chatbot with NLP and Python.\n"
            "2. Create a classification model for image or text data.\n"
            "3. Develop a recommendation or prediction system using scikit-learn."
        )
    return "I have knowledge in that area and can recommend relevant projects based on the topic."


def get_contact_email_text():
    return f"You can email me at {personal_data.get('email', 'not available')} for the quickest response."


def get_openai_response(user_message):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        import openai
    except ImportError:
        print("OpenAI package not installed. Install openai to enable OpenAI responses.")
        return None

    openai.api_key = api_key
    system_prompt = (
        f"You are a helpful personal portfolio assistant for {personal_data.get('name', 'a developer')}. "
        f"Answer as this portfolio owner with concise, friendly responses, mentioning skills, projects, education, and machine learning experience when appropriate."
    )
    user_prompt = f"{user_message}\n\nUse the personal profile data available to answer accurately."

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=220,
            temperature=0.8,
            n=1,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None


def get_personal_info_text():
    return (
        f"My name is {personal_data.get('name', 'not available')} and I am a {personal_data.get('title', 'developer')} based in {personal_data.get('location', 'not available')}. "
        f"I have {personal_data.get('experience_years', 'experience')} experience and strong skills in web development, Python, JavaScript, and cloud tools."
    )

def get_social_links_text():
    links = personal_data.get("social_links", {})
    if not links:
        return "I do not currently share social profiles."
    items = []
    for name, href in links.items():
        items.append(f"{name.capitalize()}: {href}")
    return "My social links are: " + ", ".join(items) + "."


def get_internship_text():
    internship = personal_data.get("internship", {})
    if not internship:
        return "I have internship experience in software development and automation."

    company = internship.get("company", "an organization")
    duration = internship.get("duration", "a contract")
    domain = internship.get("domain", "software development")
    return f"I interned at {company} for {duration} in {domain}."


intents = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning", "good evening"],
        "responses": [
            "Hello! Welcome to my portfolio. How can I help you today?"
        ]
    },
    "name": {
        "patterns": ["what is your name", "who are you", "your name"],
        "responses": [
            f"My name is {personal_data['name']}. Nice to meet you!"
        ]
    },
    "about": {
        "patterns": ["tell me about yourself", "about you", "who are you"],
        "responses": [
            f"I'm {personal_data['name']}, a {personal_data.get('title', 'developer')} with {personal_data.get('experience_years', 'experience')} experience. {personal_data.get('career_objective', personal_data.get('bio', ''))}"
        ]
    },
    "skills": {
        "patterns": ["skills", "technical skills", "programming languages", "what can you do"],
        "responses": [
            f"I'm proficient in various technologies across different domains:\n\n"
            f"**Frontend Technologies**\n"
            f"• HTML5, CSS3, JavaScript, React.js, Bootstrap\n\n"
            f"**Backend Technologies**\n"
            f"• Python, Flask, Node.js, REST APIs\n\n"
            f"**Databases**\n"
            f"• MySQL, MongoDB, PostgreSQL\n\n"
            f"**UI/UX Design**\n"
            f"• Figma, Adobe XD\n\n"
            f"**Tools & Platforms**\n"
            f"• Git, GitHub, Android Studio, VS Code, Unity 3D\n\n"
            f"**Cloud & Other Technologies**\n"
            f"• Cloud Computing, Machine Learning, Computer Vision"
        ]
    },
    "machine_learning": {
        "patterns": [
            "machine learning",
            "do you know machine learning",
            "are you familiar with machine learning",
            "machine learning projects",
            "recommend machine learning project",
            "suggest a project based on machine learning"
        ],
        "responses": [
            get_skill_project_recommendations("machine learning"),
            "Yes, I know machine learning. I recommend building projects like a chatbot with NLP, a text classification model, or a recommendation system using Python and scikit-learn.",
            "I am familiar with machine learning. Great project ideas are: an NLP chatbot, an image classifier, or a predictive analytics model using data from real-world datasets.",
            "Yes, I know ML. Start with a Python-based machine learning project such as an intelligent chatbot or a model that predicts trends from data."
        ]
    },
    "experience": {
        "patterns": ["experience", "work experience", "how many years experience"],
        "responses": [
            f"I have {personal_data['experience_years']} experience in development and automation testing."
        ]
    },
    "education": {
        "patterns": ["education", "degree", "where did you study", "university", "college"],
        "responses": [
            get_education_text()
        ]
    },
    "internship": {
        "patterns": ["internship", "internships", "work experience", "industry experience"],
        "responses": [
            get_internship_text()
        ]
    },
    "projects": {
        "patterns": ["projects", "your projects", "what have you built", "portfolio"],
        "responses": [
            get_projects_text()
        ]
    },
    "project_detail": {
        "patterns": ["tell me about", "project details", "project explanation", "more about"],
        "responses": [
            get_projects_text()
        ]
    },
    "contact": {
        "patterns": ["contact", "reach you", "reach me", "get in touch"],
        "responses": [
            f"You can reach me at:\n\nEmail: {personal_data['email']}\nPhone: {personal_data['phone']}\nLocation: {personal_data['location']}"
        ]
    },
    "email": {
        "patterns": ["email", "your email", "send me an email", "email address", "how can i email"],
        "responses": [
            get_contact_email_text()
        ]
    },
    "resume": {
        "patterns": ["resume", "cv", "curriculum vitae", "experience summary", "career summary"],
        "responses": [
            get_resume_summary_text()
        ]
    },
    "education": {
        "patterns": ["education", "degree", "where did you study", "university", "college", "qualification", "academic"],
        "responses": [
            get_education_breakdown_text()
        ]
    },
    "diploma": {
        "patterns": ["diploma", "polytechnic", "diploma in"],
        "responses": [
            get_education_detail_text("diploma")
        ]
    },
    "sslc": {
        "patterns": ["sslc", "10th", "tenth grade", "secondary school"],
        "responses": [
            "I have strong academic credentials including higher secondary and diploma qualifications. Ask me for more details about any specific educational stage."
        ]
    },
    "social_links": {
        "patterns": ["social links", "github", "linkedin", "twitter"],
        "responses": [
            get_social_links_text()
        ]
    },
    "location": {
        "patterns": ["location", "where are you from", "where are you based"],
        "responses": [
            f"I'm based in {personal_data['location']}."
        ]
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you", "exit"],
        "responses": [
            "Goodbye! Thanks for visiting my portfolio."
        ]
    },
    "help": {
        "patterns": ["help", "what can i ask", "what can you do", "how do i use this"],
        "responses": [
            "You can ask me about my skills, education, diploma, projects, experience, or contact details. If your browser supports voice input, press the microphone button to speak.",
            "Ask me about my education breakdown, project details, email, resume summary, or career objective. I can also answer specific questions like project explanation or diploma details."
        ]
    },
    "time": {
        "patterns": ["time", "current time", "what time is it"],
        "responses": [
            f"The current time is {datetime.now().strftime('%I:%M %p')}"
        ]
    },
    "date_of_birth": {
        "patterns": ["date of birth", "birthday", "when were you born"],
        "responses": [
            f"My date of birth is {personal_data.get('date_of_birth', 'not available')}."
        ]
    },
    "degree": {
        "patterns": ["degree", "qualification", "education level", "what is your degree"],
        "responses": [
            f"My highest degree is {personal_data.get('degree', 'not available')}."
        ]
    },
        "social_links": {
        "patterns": ["social links", "github", "linkedin", "twitter"],  
    },
    
        "BE_institution" :{
        "patterns": ["BE_institution", "college", "university", "where did you study"],
        "responses": [
            f"I studied at {personal_data.get('BE_institution', 'my university')}."
        ]
    },
    "DIPLOMA_institution" :{
        "patterns": ["DIPLOMA_institution", "DIPLOMA_college", "DIPLOMA_university", "where did you study DIPLOMA"],
        "responses": [
            f"I studied at {personal_data.get('DIPLOMA_institution', 'my university')}."
        ]
    },
    "BE_university" :{
        "patterns": ["university", "where did you study", "which university"], 
        "responses": [
            f"My university is {personal_data.get('BE_university', 'my university')}."
        ]
    }
}


def find_best_intent(user_message):
    user_message_lower = user_message.lower()
    best_match = None
    best_score = 0

    for intent_name, intent_data in intents.items():
        for pattern in intent_data["patterns"]:
            similarity = difflib.SequenceMatcher(
                None,
                user_message_lower,
                pattern.lower()
            ).ratio()

            if pattern.lower() in user_message_lower:
                similarity = max(similarity, 0.9)

            if similarity > best_score:
                best_score = similarity
                best_match = intent_name

    if best_score > 0.35:
        return best_match, best_score

    return None, best_score


def get_response(intent_name, user_message=None):
    message_lower = (user_message or "").lower()

    openai_response = get_openai_response(user_message or "")
    if openai_response:
        return openai_response

    if "email" in message_lower and "phone" not in message_lower and "contact" in message_lower:
        return get_contact_email_text()

    if "email" in message_lower and intent_name != "contact" and intent_name != "phone":
        return get_contact_email_text()

    if "project" in message_lower or "portfolio" in message_lower:
        project = find_project_by_message(user_message)
        if project:
            return get_project_detail_text(project)

    if "diploma" in message_lower:
        return get_education_detail_text("diploma")

    if "sslc" in message_lower or "10th" in message_lower or "tenth" in message_lower:
        return get_education_detail_text("sslc")

    if intent_name and intent_name in intents:
        import random
        return random.choice(intents[intent_name]["responses"])

    if "resume" in message_lower or "cv" in message_lower:
        return get_resume_summary_text()

    return "I'm not sure how to answer that. You can ask me about my skills, education, projects, or contact details."


def save_uploaded_file(file_storage, filename=None):
    if not filename:
        filename = file_storage.filename

    safe_path = os.path.join(UPLOAD_DIR, filename)
    file_storage.save(safe_path)
    return safe_path, filename


def extract_text_from_docx(path):
    try:
        doc = Document(path)
        text = []

        for para in doc.paragraphs:
            if para.text.strip():
                text.append(para.text.strip())

        return "\n".join(text)
    except Exception as e:
        print(f"Error reading docx: {e}")
        return ""


def save_personal_data():
    try:
        with open(pd_path, "w", encoding="utf-8") as f:
            json.dump(personal_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving personal_data.json: {e}")
    return personal_data


def _normalize_heading(line):
    return re.sub(r"[^a-z0-9 ]", "", line.strip().lower())


def extract_section(text, headers):
    lines = [line.strip() for line in text.splitlines()]
    normalized_headers = [_normalize_heading(h) for h in headers]
    section_lines = []
    start_index = None
    for i, line in enumerate(lines):
        norm = _normalize_heading(line)
        for header in normalized_headers:
            if norm == header or norm.startswith(header):
                start_index = i + 1
                break
        if start_index is not None:
            break

    if start_index is None:
        return []

    global_headers = [
        "career objective", "objective", "summary", "professional summary",
        "education", "skills", "projects", "experience", "internship",
        "certifications", "achievements", "languages", "social", "contact"
    ]
    end_index = len(lines)
    for i in range(start_index, len(lines)):
        norm = _normalize_heading(lines[i])
        if any(norm == h or norm.startswith(h) for h in global_headers):
            end_index = i
            break

    section_lines = lines[start_index:end_index]
    return [re.sub(r"^[•\-*\s]+", "", line).strip() for line in section_lines if line.strip()]


def parse_education_section(lines):
    education = []
    for line in lines:
        if not line:
            continue
        parts = re.split(r"\s*[|–—-]\s*|\s*\|\s*", line)
        entry = {}
        entry["degree"] = parts[0].strip()

        if len(parts) > 1:
            entry["institution"] = parts[1].strip()

        year_match = re.search(r"(19|20)\d{2}(?:\s*[-–]\s*(?:19|20)\d{2})?", line)
        if year_match:
            entry["graduation_year"] = year_match.group(0)

        cgpa_match = re.search(r"(?:CGPA|GPA)[:\s]*([0-9]+\.?[0-9]*)", line, re.I)
        if cgpa_match:
            entry["cgpa"] = cgpa_match.group(1)

        perc_match = re.search(r"(\d{1,2}\.\d{1,2}%|\d{1,2}%)(?!\S)", line)
        if perc_match:
            entry["percentage"] = perc_match.group(1)

        if entry:
            education.append(entry)
    return education


def parse_list_section(lines):
    items = []
    for line in lines:
        if not line:
            continue
        item = re.sub(r"^[•\-*\s]+", "", line).strip()
        if item:
            items.append(item)
    return items


def parse_projects_section(lines):
    projects = []
    current = None
    for line in lines:
        if not line:
            continue
        cleaned = re.sub(r"^[•\-*\s]+", "", line).strip()
        if re.match(r"^[A-Za-z0-9].{3,}$", cleaned) and len(cleaned.split()) <= 10 and ":" not in cleaned and "-" in cleaned:
            name, desc = cleaned.split("-", 1)
            projects.append({
                "name": name.strip(),
                "description": desc.strip(),
                "technologies": []
            })
            current = projects[-1]
        elif re.match(r"^[A-Za-z0-9].{3,}$", cleaned) and ":" in cleaned:
            name, desc = cleaned.split(":", 1)
            projects.append({
                "name": name.strip(),
                "description": desc.strip(),
                "technologies": []
            })
            current = projects[-1]
        elif current and len(cleaned.split()) > 4:
            if current.get("description") and not current.get("role"):
                current["description"] += " " + cleaned
            else:
                current["description"] = current.get("description", "") + " " + cleaned
        elif cleaned:
            projects.append({
                "name": cleaned,
                "description": "",
                "technologies": []
            })
            current = projects[-1]

    return projects


def parse_skills_section(lines):
    skills = {
        "programming_languages": [],
        "frameworks": [],
        "databases": [],
        "tools": []
    }
    combined = " ".join(lines)

    categories = {
        "programming_languages": ["python", "java", "c++", "c#", "javascript", "sql", "html", "css", "react", "node"],
        "frameworks": ["flask", "django", "react", "node", "fastapi", "spring", "vue"],
        "databases": ["mysql", "mongodb", "postgresql", "firebase", "sql"] ,
        "tools": ["git", "docker", "aws", "linux", "jira", "jenkins", "nlp", "ar"]
    }

    for line in lines:
        if ":" in line:
            label, values = line.split(":", 1)
            items = [item.strip() for item in re.split(r",|;|\|", values) if item.strip()]
            key = _normalize_heading(label)
            if "programming" in key or "language" in key:
                skills["programming_languages"].extend(items)
            elif "framework" in key or "library" in key:
                skills["frameworks"].extend(items)
            elif "database" in key:
                skills["databases"].extend(items)
            else:
                skills["tools"].extend(items)
        else:
            values = [item.strip() for item in re.split(r",|;|\|", line) if item.strip()]
            for value in values:
                lower = value.lower()
                matched = False
                for category, keywords in categories.items():
                    if any(keyword in lower for keyword in keywords):
                        skills[category].append(value)
                        matched = True
                        break
                if not matched:
                    skills["tools"].append(value)

    for key in skills:
        skills[key] = sorted(set(skills[key]), key=lambda x: skills[key].index(x))

    return skills


def parse_social_links(text):
    links = {}
    for pattern, key in [
        (r"https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+", "github"),
        (r"https?://(?:www\.)?linkedin\.com/[A-Za-z0-9_/-]+", "linkedin"),
        (r"https?://(?:www\.)?twitter\.com/[A-Za-z0-9_/-]+", "twitter")
    ]:
        match = re.search(pattern, text, re.I)
        if match:
            links[key] = match.group(0)
    return links


def parse_resume_text(text):
    data = {}
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if lines:
        data["name"] = lines[0]

    if len(lines) > 1 and len(lines[1]) < 50 and "@" not in lines[1]:
        data["title"] = lines[1]

    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if email_match:
        data["email"] = email_match.group(0)

    phone_match = re.search(r"\+?\d[\d \-()]{7,}\d", text)
    if phone_match:
        data["phone"] = phone_match.group(0)

    career_obj = extract_section(text, ["Career Objective", "Objective", "Summary", "Professional Summary"])
    if career_obj:
        data["career_objective"] = " ".join(career_obj)

    education_lines = extract_section(text, ["Education"])
    education_entries = parse_education_section(education_lines)
    if education_entries:
        data["education"] = education_entries

    skills_lines = extract_section(text, ["Skills", "Technical Skills", "Skills & Expertise"])
    skills_entries = parse_skills_section(skills_lines)
    if any(skills_entries.values()):
        data["skills"] = skills_entries

    project_lines = extract_section(text, ["Projects", "Project Experience", "Selected Projects"])
    project_entries = parse_projects_section(project_lines)
    if project_entries:
        data["projects"] = project_entries

    internship_lines = extract_section(text, ["Internship", "Internships", "Experience", "Work Experience"])
    internship_items = parse_list_section(internship_lines)
    if internship_items:
        data["internship"] = {
            "description": " ".join(internship_items),
            "responsibilities": internship_items
        }

    certification_lines = extract_section(text, ["Certifications", "Certification"])
    certifications = parse_list_section(certification_lines)
    if certifications:
        data["certifications"] = certifications

    achievement_lines = extract_section(text, ["Achievements", "Awards", "Honors"])
    achievements = parse_list_section(achievement_lines)
    if achievements:
        data["achievements"] = achievements

    language_lines = extract_section(text, ["Languages", "Languages Known"])
    languages = parse_list_section(language_lines)
    if languages:
        data["languages_known"] = languages

    socials = parse_social_links(text)
    if socials:
        data["social_links"] = socials

    location_match = re.search(r"\b(Bengaluru|Bangalore|India|\w+\s*,\s*India)\b", text)
    if location_match:
        data["location"] = location_match.group(0)

    objective_line = next((line for line in lines if "objective" in line.lower() or "summary" in line.lower()), None)
    if objective_line and "career_objective" not in data:
        data["career_objective"] = objective_line

    return data


@app.route("/uploads/<path:filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/api/upload_photo", methods=["POST"])
def upload_photo():
    try:
        if "photo" not in request.files:
            return jsonify({"error": "No photo provided"}), 400

        photo = request.files["photo"]

        if photo.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        ext = os.path.splitext(photo.filename)[1]
        _, filename = save_uploaded_file(photo, filename="profile" + ext)

        personal_data["photo"] = f"/uploads/{filename}"
        save_personal_data()

        return jsonify({"photo": personal_data["photo"]})

    except Exception as e:
        print(f"Error uploading photo: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/upload_resume", methods=["POST"])
def upload_resume():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No resume provided"}), 400

        resume = request.files["resume"]

        if resume.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        saved_path, filename = save_uploaded_file(
            resume,
            filename="resume" + os.path.splitext(resume.filename)[1]
        )

        text = extract_text_from_docx(saved_path)
        parsed = parse_resume_text(text)

        personal_data.update(parsed)
        save_personal_data()

        return jsonify({
            "status": "ok",
            "personal_data": personal_data
        })

    except Exception as e:
        print(f"Error uploading resume: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON body required"}), 400

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        intent, confidence = find_best_intent(user_message)
        response = get_response(intent, user_message)

        return jsonify({
            "response": response,
            "intent": intent,
            "confidence": confidence
        })

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/info", methods=["GET"])
def get_info():
    return jsonify(personal_data)


@app.route("/api/projects", methods=["GET"])
def get_projects():
    return jsonify(personal_data.get("projects", []))


@app.route("/api/skills", methods=["GET"])
def get_skills():
    return jsonify(personal_data.get("skills", {}))


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/", methods=["GET"])
def home():
    return send_from_directory('.', 'index.html')


@app.route("/api/", methods=["GET"])
def api_root():
    return jsonify({
        "message": "Personal Chatbot Backend API",
        "version": "1.0",
        "endpoints": {
            "chat": "/api/chat POST",
            "info": "/api/info GET",
            "projects": "/api/projects GET",
            "skills": "/api/skills GET",
            "health": "/api/health GET"
        }
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("=" * 50)
    print("Personal Chatbot Backend Starting...")
    print("=" * 50)
    print(f"Loaded {len(intents)} intents")
    print(f"Personal data loaded: {personal_data['name']}")
    print("API running at: http://localhost:5000")
    print("Chat endpoint: http://localhost:5000/api/chat")
    print("=" * 50)

    app.run(debug=True, host="localhost", port=5000)