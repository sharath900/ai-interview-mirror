# 🎓 AI Interview Mirror

> AI-Powered Placement Preparation Platform | Resume Analysis | Mock Interviews | Project Defense

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Gemini AI](https://img.shields.io/badge/Gemini-8f7ee7?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 🎯 Live Demo

**Try it now:** [https://ai-interview-mirror.onrender.com/](https://ai-interview-mirror.onrender.com/)

---

## 📋 Overview

**AI Interview Mirror** is a comprehensive placement preparation platform that helps engineering students ace their interviews. It combines AI-powered analysis with personalized practice tools to prepare for technical and HR interviews.

**Perfect for:**
- 📚 Students preparing for placements
- 🎯 Resume optimization and feedback
- 🎤 Mock interview practice
- 🚀 Project defense preparation

---

## ✨ Features

### 🔐 **Authentication & Security**
- User registration and secure login
- Google OAuth authentication for quick signup
- Profile management and privacy controls
- Secure password handling

### 📄 **Resume Analyzer**
- Upload resume as PDF
- AI-powered analysis using Gemini API
- Feedback on:
  - Skills identification and gaps
  - Weak areas and improvements needed
  - Missing key details
  - Predicted interview questions
- Resume history tracking

### 🎤 **Mock Interview Practice**
- Role-based interview questions
- Difficulty levels (Easy, Medium, Hard)
- Interview type selection (Technical, HR, Behavioral)
- AI-powered question generation
- Interview history with performance tracking
- Practice unlimited times

### 🛡️ **Project Defense Preparation**
- Enter project details (title, technologies, description)
- AI generates deep, technical questions
- Learn to explain projects effectively
- Project defense history
- Improve communication skills

### 📊 **Professional Dashboard**
- Quick access to all tools
- Preparation activity overview
- History of resumes, interviews, and projects
- Performance metrics
- User profile with Google account integration

### 🔒 **Privacy & Security**
- Privacy center for data management
- Django admin panel for management
- Secure database with PostgreSQL
- CSRF protection

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Backend** | Django 4.x, Django REST Framework |
| **Database** | PostgreSQL |
| **Authentication** | Django Auth, Google OAuth, Django Allauth |
| **AI/ML** | Google Gemini API |
| **Deployment** | Render, WhiteNoise (static files) |
| **Environment** | Python 3.9+ |

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- PostgreSQL (or SQLite for development)
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/sharath900/ai-interview-mirror.git
cd ai-interview-mirror
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Variables
Create a `.env` file in the project root:
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_NAME=interview_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Gemini API
GEMINI_API_KEY=your-gemini-api-key

# Email Configuration (for notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Step 5: Database Migrations
```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Access the application at: **http://localhost:8000**

---

## 🚀 Usage

### For Students

1. **Sign Up / Login**
   - Create account with email or Google OAuth
   - Complete your profile

2. **Analyze Resume**
   - Go to "Resume Analyzer"
   - Upload your PDF resume
   - Get AI feedback and improvement suggestions

3. **Practice Interviews**
   - Select role, difficulty, and interview type
   - Answer AI-generated questions
   - Review your responses
   - Track progress

4. **Project Defense**
   - Add your project details
   - Get asked technical questions
   - Practice explaining your work
   - Save for future reference

### For Admins

1. Access Django admin panel at: **http://localhost:8000/admin**
2. Manage users, resumes, interviews, and projects
3. Monitor platform usage
4. Configure API keys and settings

---

## 📁 Project Structure

```
ai-interview-mirror/
├── manage.py
├── requirements.txt
├── .env.example
├── core/                          # Main Django app
│   ├── models.py                  # User, Resume, Interview models
│   ├── views.py                   # Business logic
│   ├── forms.py                   # Django forms
│   ├── urls.py                    # URL routing
│   └── ai_service.py             # Gemini API integration
├── templates/
│   ├── base.html                  # Base template
│   ├── dashboard.html
│   ├── resume_analyzer.html
│   ├── mock_interview.html
│   ├── project_defense.html
│   └── ...
├── static/
│   ├── css/                       # Custom CSS
│   ├── js/                        # JavaScript files
│   └── images/
└── config/
    ├── settings.py                # Django settings
    ├── urls.py                    # Project URLs
    └── wsgi.py
```

---

## 🔌 API Integration

### Google Gemini API
This project uses Google Gemini API for AI-powered features:

- **Resume Analysis** - Extract skills, identify gaps, suggest improvements
- **Interview Questions** - Generate role-based technical and HR questions
- **Project Defense** - Create deep technical questions about projects

[Get your Gemini API key](https://ai.google.dev/)

---

## 🎯 Future Enhancements

- [ ] Video interview recording and playback
- [ ] AI-powered answer evaluation
- [ ] Interview preparation roadmap
- [ ] Peer comparison analytics
- [ ] Export interview reports as PDF
- [ ] Mobile app version
- [ ] Real-time collaboration features
- [ ] Integration with job portals
- [ ] Multi-language support

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Ensure PostgreSQL is running
# Check credentials in .env file
# Verify database exists
```

### Gemini API Error
```
# Verify API key in .env
# Check API is enabled in Google Cloud
# Ensure you have sufficient API quota
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 📞 Support & Contact

- 📧 Email: your-email@example.com
- 🔗 LinkedIn: [sharath-kumar](https://linkedin.com/in/sharath-kumar)
- 🐙 GitHub: [@sharath900](https://github.com/sharath900)

---

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- Django community for excellent framework
- Bootstrap for UI components
- All contributors and users

---

<div align="center">

**⭐ If this project helped you, please consider giving it a star!**

Made with ❤️ by [Sharathkumar](https://github.com/sharath900)

</div>
