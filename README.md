# AI Resume Analyzer

An AI-powered Resume Analyzer built with Django and Python.
Upload your resume and get instant structured feedback.

## Features
- Upload PDF, DOC, DOCX resumes
- AI-powered analysis using Groq + LLaMA 3.3
- Overall score with color coding
- Section-wise scoring with progress bars
- Strengths, weaknesses, missing areas, suggestions
- Keyword highlights
- Job description matching
- Download analysis as PDF
- Loading spinner
- Duplicate resume detection

## Tech Stack
- Backend: Django (Python)
- AI Model: LLaMA 3.3 70B via Groq API
- PDF Extraction: PyMuPDF
- DOCX Extraction: python-docx
- PDF Export: ReportLab
- Database: SQLite

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/subashyeager1801/resume-analyzer.git
cd resume-analyzer

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

### 3. Install dependencies
pip install -r requirements.txt

### 4. Create .env file
Create a .env file in the root folder and add:
GROQ_API_KEY=your_groq_api_key_here

Get your free Groq API key from: https://console.groq.com

### 5. Run migrations
python manage.py makemigrations
python manage.py migrate

### 6. Create admin superuser
python manage.py createsuperuser

### 7. Run the server
python manage.py runserver

Visit http://127.0.0.1:8000

## Architecture / Flow
1. User uploads PDF/DOC/DOCX resume
2. Django saves file temporarily
3. PyMuPDF or python-docx extracts text
4. Text is sent to Groq API with a structured prompt
5. LLaMA 3.3 returns JSON with score, strengths, weaknesses etc.
6. Result is saved to SQLite database
7. Result is displayed to user with nice UI
8. User can download analysis as PDF

## AI Tools Used
- Groq API (free tier)
- LLaMA 3.3 70B Versatile model

## Prompt Used
The prompt asks the AI to return a strict JSON object containing:
- Overall score (0-100)
- Profile summary
- Strengths
- Weaknesses
- Missing areas
- Suggestions
- Keywords
- Section scores
- Job description match (optional)

## Admin Panel
Visit http://127.0.0.1:8000/admin
Login with superuser credentials to view all analyzed resumes.

## Assumptions
- Resume text is extractable (not scanned image PDFs)
- Free Groq API tier is sufficient for demo use
- SQLite is used for simplicity (can be switched to PostgreSQL)

## Limitations
- Scanned/image-based PDFs cannot be parsed
- Groq free tier has rate limits
- Analysis quality depends on resume text clarity

## Possible Improvements
- OCR support for scanned PDFs
- Multiple language support
- Resume comparison feature
- Email results to user
- Deploy to production with PostgreSQL

# AI Usage Documentation

## AI Tools Used
- **Claude (Anthropic)** — Coding assistant for development
- **Groq API + LLaMA 3.3 70B** — AI model inside the app
  for resume analysis

---

## Where I Used AI

### 1. Project Structure
- Used Claude to suggest Django project folder structure
- Claude recommended separating logic into
  pdf_extractor.py and ai_analyzer.py modules

### 2. Code Generation
- Used Claude to generate initial boilerplate for
  views.py, models.py, and urls.py
- Claude suggested PyMuPDF for PDF extraction
  and python-docx for DOCX support

### 3. Resume Analysis Prompt
- Used Claude to design the structured JSON prompt
  sent to the AI model


### 4. UI Design
- Used Claude to generate HTML and CSS for
  the upload page and result page


### 5. PDF Export Feature
- Used Claude to suggest ReportLab library
- Claude generated the initial PDF export code

### 6. Admin Panel
- Used Claude to set up Django admin panel


---

## How I Used AI

- I integrated the code into my project
- I ran and tested it manually in the browser
- When errors occurred I debugged them myself
- For complex errors I shared the error message
  with Claude to understand what went wrong

---

## What I Verified and Fixed Manually

### 1. API Provider Issues
- Claude initially suggested Anthropic API
  but I had no credits
- Switched to Google Gemini — hit quota limits
- Finally switched to Groq API manually
- Fixed all 400, 404, and 429 errors myself
  by reading error messages and documentation

### 2. Environment Configuration
- .env file was in wrong folder — fixed manually
- .gitignore was created in wrong location — fixed manually
- *.txt rule in .gitignore was blocking
  requirements.txt — identified and fixed manually

### 3. GitHub Secret Scanning
- Accidentally committed API key in .env
  and resume analyzer.txt
- GitHub blocked push multiple times
- Manually cleaned git history
- Deleted and recreated repository
- Regenerated API keys multiple times

### 4. Deployment on Render
- Configured all Render settings manually
- App showed "no such table" error after deployment
- Fixed by adding python manage.py migrate
  to build command manually
- Troubleshot environment variables on Render
- Fixed whitenoise static files configuration

### 5. Testing
- Tested with multiple real resume PDFs manually
- Verified duplicate detection works correctly
- Checked edge cases like wrong file types,
  empty files, and large resumes manually

AI was used as a coding assistant to speed up
development. All debugging, configuration,
deployment, and testing were done manually.
Both were essential to complete this project.
