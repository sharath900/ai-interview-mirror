import os
import re
from google import genai


def extract_section(text, section_name):
    pattern = rf"{section_name}:\s*(.*?)(?=\n[A-Za-z ]+:|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return ""


def get_interview_feedback(role, difficulty, company_type, question, user_answer):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "ai_feedback": "Gemini API key is missing. Check your .env file.",
            "score": 0,
            "weakness_tags": "API key missing",
            "better_answer": "Not available",
            "next_question": "Not available",
        }

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are AI Interview Mirror, a personal interview coach for engineering students.

Interview details:
Role: {role}
Difficulty: {difficulty}
Company Type: {company_type}

Question:
{question}

Student Answer:
{user_answer}

Evaluate the student's answer.

Return your response exactly in this format:

Score: give only one number from 0 to 10

AI Feedback:
Explain the feedback in simple English. Mention what is good and what is missing.

Weakness Tags:
Give 2 to 5 short weakness tags separated by commas.

Better Answer:
Write a better answer in simple, natural English.

Next Follow-up Question:
Ask one follow-up interview question based on the student's weakness.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text

        score_text = extract_section(text, "Score")
        score_match = re.search(r"\d+", score_text)
        score = int(score_match.group()) if score_match else 0

        return {
            "ai_feedback": extract_section(text, "AI Feedback"),
            "score": score,
            "weakness_tags": extract_section(text, "Weakness Tags"),
            "better_answer": extract_section(text, "Better Answer"),
            "next_question": extract_section(text, "Next Follow-up Question"),
        }

    except Exception as e:
        return {
            "ai_feedback": f"Something went wrong while connecting to Gemini: {str(e)}",
            "score": 0,
            "weakness_tags": "Gemini error",
            "better_answer": "Not available",
            "next_question": "Try again later.",
        }
def get_improvement_plan(common_weaknesses, average_score):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is missing. Check your .env file."

    client = genai.Client(api_key=api_key)

    weaknesses_text = ", ".join([weakness for weakness, count in common_weaknesses])

    if not weaknesses_text:
        weaknesses_text = "No weakness data available yet."

    prompt = f"""
You are AI Interview Mirror, a personal interview coach for engineering students.

Student interview performance:
Average Score: {average_score}/10
Common Weak Areas: {weaknesses_text}

Create a simple 5-day improvement plan.

Rules:
- Use simple English.
- Give day-wise plan.
- Focus on weak areas.
- Include what to study.
- Include what to practice.
- Include one mock interview task each day.
- Make it useful for Indian engineering students.

Format:
Day 1:
Day 2:
Day 3:
Day 4:
Day 5:
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Something went wrong while generating improvement plan: {str(e)}"

def get_project_defense_questions(project_title, technologies, project_description, target_role):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is missing. Check your .env file."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are AI Interview Mirror, a strict but helpful technical interviewer.

A student is preparing for interviews.

Project Title:
{project_title}

Technologies Used:
{technologies}

Project Description:
{project_description}

Target Role:
{target_role}

Generate 10 deep project-defense interview questions.

Rules:
- Questions should be realistic.
- Ask about technical decisions.
- Ask about implementation.
- Ask about dataset/database/API if relevant.
- Ask about limitations.
- Ask about improvements.
- Ask questions that product companies may ask.
- Use simple English.
- Number the questions from 1 to 10.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Something went wrong while generating project questions: {str(e)}"

def get_first_project_question(project_title, technologies, project_description, target_role):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is missing. Check your .env file."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are AI Interview Mirror, a strict but helpful technical interviewer.

Student project details:

Project Title:
{project_title}

Technologies Used:
{technologies}

Project Description:
{project_description}

Target Role:
{target_role}

Ask only ONE strong project-defense interview question.

Rules:
- Ask a realistic interview question.
- Focus on technical decision, implementation, limitation, dataset, API, database, model, or deployment.
- Use simple English.
- Do not give explanation.
- Return only the question.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        return f"Something went wrong while generating question: {str(e)}"


def get_project_defense_feedback(project_title, technologies, project_description, target_role, question, user_answer):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "ai_feedback": "Gemini API key is missing. Check your .env file.",
            "score": 0,
            "weakness_tags": "API key missing",
            "better_answer": "Not available",
            "next_question": "Not available",
        }

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are AI Interview Mirror, a project-defense interviewer for engineering students.

Project Details:
Project Title: {project_title}
Technologies Used: {technologies}
Target Role: {target_role}
Project Description: {project_description}

Current Project Defense Question:
{question}

Student Answer:
{user_answer}

Evaluate the student's project-defense answer.

Return your response exactly in this format:

Score: give only one number from 0 to 10

AI Feedback:
Explain the feedback in simple English. Mention what is good and what is missing.

Weakness Tags:
Give 2 to 5 short weakness tags separated by commas.

Better Answer:
Write a stronger interview answer in simple, natural English.

Next Follow-up Question:
Ask one next deep project-defense question based on the student's weakness and project details.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text

        score_text = extract_section(text, "Score")
        score_match = re.search(r"\d+", score_text)
        score = int(score_match.group()) if score_match else 0

        return {
            "ai_feedback": extract_section(text, "AI Feedback"),
            "score": score,
            "weakness_tags": extract_section(text, "Weakness Tags"),
            "better_answer": extract_section(text, "Better Answer"),
            "next_question": extract_section(text, "Next Follow-up Question"),
        }

    except Exception as e:
        return {
            "ai_feedback": f"Something went wrong while connecting to Gemini: {str(e)}",
            "score": 0,
            "weakness_tags": "Gemini error",
            "better_answer": "Not available",
            "next_question": "Try again later.",
        }    
# for resume ai analyzer this code
def analyze_resume_text(resume_text):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is missing. Check your .env file."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are AI Interview Mirror, an AI resume analyzer for engineering students.

Analyze this resume text:

{resume_text}

Return the analysis in this format:

Detected Skills:
List the technical skills.

Detected Projects:
List the projects mentioned.

Strong Points:
Mention what is good in this resume.

Weak Points:
Mention what is missing or weak.

Suggested Interview Questions:
Give 10 interview questions based on this resume.

Improvement Suggestions:
Give practical suggestions to improve the resume and interview preparation.

Use simple English.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Something went wrong while analyzing resume: {str(e)}"
    
    # This function creates the first interview question from the user's resume text.
# It helps us start a resume-based interview instead of a general role-based interview.
def get_resume_based_question(resume_text):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is missing. Check your .env file."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are AI Interview Mirror, an interviewer for engineering students and freshers.

Read this resume text:

{resume_text}

Ask only ONE strong resume-based interview question.

Rules:
- The question should be based on the user's resume.
- Prefer questions about projects, skills, internships, tools, or technologies.
- Use simple English.
- Do not give explanation.
- Return only the question.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        return f"Something went wrong while generating resume-based question: {str(e)}"