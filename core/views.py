from django.shortcuts import render, redirect, get_object_or_404
import pdfplumber
from django.contrib import messages
from django.db.models import Q
from allauth.socialaccount.models import SocialAccount

from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    InterviewSession,
    InterviewAnswer,
    ProjectDefenseSession,
    ProjectDefenseAnswer,
    ResumeAnalysis
)

from .ai_helper import (
    get_interview_feedback,
    get_improvement_plan,
    get_first_project_question,
    get_project_defense_feedback,
    analyze_resume_text,
    get_resume_based_question
)
def login_user(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        try:
            found_user = User.objects.get(
                Q(username=username_or_email) | Q(email=username_or_email)
            )

            user = authenticate(
                request,
                username=found_user.username,
                password=password
            )

        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username/email or password.")
            return render(request, "login.html")

    return render(request, "login.html")


def register_user(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please login.")
            return redirect("login")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "register.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect("login")


# This function shows the public home page.
# Login is not required for the home page.
def home(request):
    return render(request, "home.html")


# This function starts a normal mock interview.
# It stores the selected role, difficulty, and company type with the logged-in user.
@login_required
def start_interview(request):
    if request.method == "POST":
        role = request.POST.get("role")
        difficulty = request.POST.get("difficulty")
        company_type = request.POST.get("company_type")

        first_question = f"Tell me about yourself for a {role} role."

        session = InterviewSession.objects.create(
            user=request.user,
            role=role,
            difficulty=difficulty,
            company_type=company_type,
            first_question=first_question,
            current_question=first_question
        )

        return redirect("interview_room", session_id=session.id)

    return render(request, "start_interview.html")


# This function shows the current mock interview question.
# It saves the user's answer, sends it to Gemini, stores feedback, and updates the next question.
# It only allows the owner of the interview session to access the page.
@login_required
def interview_room(request, session_id):
    session = get_object_or_404(
        InterviewSession,
        id=session_id,
        user=request.user
    )

    if request.method == "POST":
        user_answer = request.POST.get("user_answer")

        ai_result = get_interview_feedback(
            role=session.role,
            difficulty=session.difficulty,
            company_type=session.company_type,
            question=session.current_question,
            user_answer=user_answer
        )

        answer = InterviewAnswer.objects.create(
            session=session,
            question=session.current_question,
            user_answer=user_answer,
            ai_feedback=ai_result["ai_feedback"],
            score=ai_result["score"],
            weakness_tags=ai_result["weakness_tags"],
            better_answer=ai_result["better_answer"],
            next_question=ai_result["next_question"]
        )

        session.current_question = ai_result["next_question"]
        session.save()

        return redirect("feedback", answer_id=answer.id)

    return render(request, "interview_room.html", {
        "session": session
    })


# This function shows feedback for a mock interview answer.
# It only allows the logged-in user to see their own answer feedback.
@login_required
def feedback(request, answer_id):
    answer = get_object_or_404(
        InterviewAnswer,
        id=answer_id,
        session__user=request.user
    )

    return render(request, "feedback.html", {
        "answer": answer
    })


# This function shows the logged-in user's personal dashboard.
# It shows only that user's mock interviews, project defense answers, scores, and weak areas.
@login_required
def dashboard(request):
    interview_sessions = InterviewSession.objects.filter(
        user=request.user
    ).order_by("-created_at")

    interview_answers = InterviewAnswer.objects.filter(
        session__user=request.user
    ).order_by("-created_at")

    project_sessions = ProjectDefenseSession.objects.filter(
        user=request.user
    ).order_by("-created_at")

    project_answers = ProjectDefenseAnswer.objects.filter(
        session__user=request.user
    ).order_by("-created_at")

    total_interviews = interview_sessions.count()
    total_interview_answers = interview_answers.count()

    total_project_sessions = project_sessions.count()
    total_project_answers = project_answers.count()

    if total_interview_answers > 0:
        total_score = sum(answer.score for answer in interview_answers)
        average_interview_score = round(total_score / total_interview_answers, 1)
    else:
        average_interview_score = 0

    if total_project_answers > 0:
        total_project_score = sum(answer.score for answer in project_answers)
        average_project_score = round(total_project_score / total_project_answers, 1)
    else:
        average_project_score = 0

    weakness_list = []

    for answer in interview_answers:
        if answer.weakness_tags:
            tags = answer.weakness_tags.split(",")
            for tag in tags:
                clean_tag = tag.strip()
                if clean_tag:
                    weakness_list.append(clean_tag)

    for answer in project_answers:
        if answer.weakness_tags:
            tags = answer.weakness_tags.split(",")
            for tag in tags:
                clean_tag = tag.strip()
                if clean_tag:
                    weakness_list.append(clean_tag)

    weakness_count = {}
    for weakness in weakness_list:
        weakness_count[weakness] = weakness_count.get(weakness, 0) + 1

    common_weaknesses = sorted(
        weakness_count.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return render(request, "dashboard.html", {
        "total_interviews": total_interviews,
        "total_interview_answers": total_interview_answers,
        "average_interview_score": average_interview_score,

        "total_project_sessions": total_project_sessions,
        "total_project_answers": total_project_answers,
        "average_project_score": average_project_score,

        "interview_answers": interview_answers,
        "project_answers": project_answers,
        "common_weaknesses": common_weaknesses,
    })


# This function creates a personal improvement plan.
# It uses both mock interview and project-defense weak areas for the logged-in user.
@login_required
def improvement_plan(request):
    interview_answers = InterviewAnswer.objects.filter(
        session__user=request.user
    ).order_by("-created_at")

    project_answers = ProjectDefenseAnswer.objects.filter(
        session__user=request.user
    ).order_by("-created_at")

    all_scores = [answer.score for answer in interview_answers] + [
        answer.score for answer in project_answers
    ]

    if all_scores:
        average_score = round(sum(all_scores) / len(all_scores), 1)
    else:
        average_score = 0

    weakness_list = []

    for answer in interview_answers:
        if answer.weakness_tags:
            tags = answer.weakness_tags.split(",")
            for tag in tags:
                clean_tag = tag.strip()
                if clean_tag:
                    weakness_list.append(clean_tag)

    for answer in project_answers:
        if answer.weakness_tags:
            tags = answer.weakness_tags.split(",")
            for tag in tags:
                clean_tag = tag.strip()
                if clean_tag:
                    weakness_list.append(clean_tag)

    weakness_count = {}
    for weakness in weakness_list:
        weakness_count[weakness] = weakness_count.get(weakness, 0) + 1

    common_weaknesses = sorted(
        weakness_count.items(),
        key=lambda x: x[1],
        reverse=True
    )

    plan = get_improvement_plan(common_weaknesses, average_score)

    return render(request, "improvement_plan.html", {
        "plan": plan,
        "average_score": average_score,
        "common_weaknesses": common_weaknesses,
    })


# This function starts project-defense practice.
# It saves project details with the logged-in user and asks Gemini for the first project-defense question.
@login_required
def project_defense(request):
    if request.method == "POST":
        project_title = request.POST.get("project_title")
        technologies = request.POST.get("technologies")
        project_description = request.POST.get("project_description")
        target_role = request.POST.get("target_role")

        first_question = get_first_project_question(
            project_title=project_title,
            technologies=technologies,
            project_description=project_description,
            target_role=target_role
        )

        session = ProjectDefenseSession.objects.create(
            user=request.user,
            project_title=project_title,
            technologies=technologies,
            project_description=project_description,
            target_role=target_role,
            current_question=first_question
        )

        return redirect("project_defense_room", session_id=session.id)

    return render(request, "project_defense.html")


# This function shows the current project-defense question.
# It saves the user's answer, sends it to Gemini, stores feedback, and updates the next project question.
# It only allows the owner of the project-defense session to access the page.
@login_required
def project_defense_room(request, session_id):
    session = get_object_or_404(
        ProjectDefenseSession,
        id=session_id,
        user=request.user
    )

    if request.method == "POST":
        user_answer = request.POST.get("user_answer")

        ai_result = get_project_defense_feedback(
            project_title=session.project_title,
            technologies=session.technologies,
            project_description=session.project_description,
            target_role=session.target_role,
            question=session.current_question,
            user_answer=user_answer
        )

        answer = ProjectDefenseAnswer.objects.create(
            session=session,
            question=session.current_question,
            user_answer=user_answer,
            ai_feedback=ai_result["ai_feedback"],
            score=ai_result["score"],
            weakness_tags=ai_result["weakness_tags"],
            better_answer=ai_result["better_answer"],
            next_question=ai_result["next_question"]
        )

        session.current_question = ai_result["next_question"]
        session.save()

        return redirect("project_defense_feedback", answer_id=answer.id)

    return render(request, "project_defense_room.html", {
        "session": session
    })


# This function shows feedback for a project-defense answer.
# It only allows the logged-in user to see their own project-defense feedback.
@login_required
def project_defense_feedback(request, answer_id):
    answer = get_object_or_404(
        ProjectDefenseAnswer,
        id=answer_id,
        session__user=request.user
    )

    return render(request, "project_defense_feedback.html", {
        "answer": answer
    })


# This function handles resume PDF upload.
# It saves the resume with the logged-in user, extracts text using pdfplumber, and sends it to Gemini.
@login_required
def resume_analyzer(request):
    analysis = None

    if request.method == "POST":
        resume_file = request.FILES.get("resume_file")

        if resume_file:
            resume_obj = ResumeAnalysis.objects.create(
                user=request.user,
                resume_file=resume_file
            )

            extracted_text = ""

            with pdfplumber.open(resume_obj.resume_file.path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"

            ai_analysis = analyze_resume_text(extracted_text)

            resume_obj.extracted_text = extracted_text
            resume_obj.ai_analysis = ai_analysis
            resume_obj.save()

            analysis = resume_obj

    return render(request, "resume_analyzer.html", {
        "analysis": analysis
    })


# This function shows the Privacy Center page.
# It lets the logged-in user delete only their own interview, project-defense, or resume data.
@login_required
def privacy_center(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "delete_interviews":
            InterviewSession.objects.filter(user=request.user).delete()

        elif action == "delete_project_defense":
            ProjectDefenseSession.objects.filter(user=request.user).delete()

        elif action == "delete_resumes":
            ResumeAnalysis.objects.filter(user=request.user).delete()

        elif action == "delete_all":
            InterviewSession.objects.filter(user=request.user).delete()
            ProjectDefenseSession.objects.filter(user=request.user).delete()
            ResumeAnalysis.objects.filter(user=request.user).delete()

        return redirect("privacy_center")

    interview_count = InterviewSession.objects.filter(user=request.user).count()
    project_count = ProjectDefenseSession.objects.filter(user=request.user).count()
    resume_count = ResumeAnalysis.objects.filter(user=request.user).count()

    return render(request, "privacy_center.html", {
        "interview_count": interview_count,
        "project_count": project_count,
        "resume_count": resume_count,
    })

# This function shows the logged-in user's profile page.
# It displays account details and basic activity counts.
@login_required
def profile(request):
    google_picture = None
    google_email = request.user.email
    google_name = request.user.get_full_name() or request.user.username
    login_type = "Username / Password"

    social_account = SocialAccount.objects.filter(
        user=request.user,
        provider="google"
    ).first()

    if social_account:
        google_picture = social_account.extra_data.get("picture")
        google_email = social_account.extra_data.get("email", request.user.email)
        google_name = social_account.extra_data.get("name", google_name)
        login_type = "Google Account"

    context = {
        "google_picture": google_picture,
        "google_email": google_email,
        "google_name": google_name,
        "login_type": login_type,
    }

    return render(request, "profile.html", context)
# It explains how users can use the main features of AI Interview Mirror.
def help_page(request):
    return render(request, "help.html")
# This function starts an interview based on a previously uploaded resume.
# It finds the logged-in user's resume analysis, asks Gemini for a resume-based question,
# creates an InterviewSession, and redirects user to the interview room.
@login_required
def start_resume_interview(request, analysis_id):
    resume_analysis = get_object_or_404(
        ResumeAnalysis,
        id=analysis_id,
        user=request.user
    )

    first_question = get_resume_based_question(
        resume_analysis.extracted_text
    )

    session = InterviewSession.objects.create(
        user=request.user,
        role="Resume-Based Interview",
        difficulty="Intermediate",
        company_type="Resume Based",
        first_question=first_question,
        current_question=first_question
    )

    return redirect("interview_room", session_id=session.id)
# This function shows all resume analyses uploaded by the logged-in user.
# It helps users view old resume analyses and start resume-based interviews again.
@login_required
def resume_history(request):
    resumes = ResumeAnalysis.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "resume_history.html", {
        "resumes": resumes
    })


# This function shows one resume analysis in detail.
# It only allows the logged-in user to open their own resume analysis.
@login_required
def resume_detail(request, analysis_id):
    resume = get_object_or_404(
        ResumeAnalysis,
        id=analysis_id,
        user=request.user
    )

    return render(request, "resume_detail.html", {
        "resume": resume
    })


# This function deletes one resume analysis.
# It only deletes the logged-in user's own resume analysis.
@login_required
def delete_resume_analysis(request, analysis_id):
    resume = get_object_or_404(
        ResumeAnalysis,
        id=analysis_id,
        user=request.user
    )

    if request.method == "POST":
        resume.delete()
        messages.success(request, "Resume analysis deleted successfully.")
        return redirect("resume_history")

    return redirect("resume_detail", analysis_id=analysis_id)

# This function deletes one mock interview answer.
# It only allows the logged-in user to delete their own interview answer.
@login_required
def delete_interview_answer(request, answer_id):
    answer = get_object_or_404(
        InterviewAnswer,
        id=answer_id,
        session__user=request.user
    )

    if request.method == "POST":
        answer.delete()
        messages.success(request, "Interview answer deleted successfully.")
        return redirect("interview_history")

    return redirect("interview_history")


# This function deletes one project-defense answer.
# It only allows the logged-in user to delete their own project-defense answer.
@login_required
def delete_project_answer(request, answer_id):
    answer = get_object_or_404(
        ProjectDefenseAnswer,
        id=answer_id,
        session__user=request.user
    )

    if request.method == "POST":
        answer.delete()
        messages.success(request, "Project-defense answer deleted successfully.")
        return redirect("project_history")

    return redirect("project_history")

# This function shows all mock interview answers of the logged-in user.
# It helps users review old questions, answers, scores, weak areas, and feedback.
@login_required
def interview_history(request):
    answers = InterviewAnswer.objects.filter(
        session__user=request.user
    ).order_by("-created_at")

    return render(request, "interview_history.html", {
        "answers": answers
    })


# This function shows all project-defense answers of the logged-in user.
# It helps users review old project questions, answers, scores, weak areas, and feedback.
@login_required
def project_history(request):
    answers = ProjectDefenseAnswer.objects.filter(
        session__user=request.user
    ).order_by("-created_at")

    return render(request, "project_history.html", {
        "answers": answers
    })


# This function deletes one mock interview answer.
# It only allows the logged-in user to delete their own interview answer.
@login_required
def delete_interview_answer(request, answer_id):
    answer = get_object_or_404(
        InterviewAnswer,
        id=answer_id,
        session__user=request.user
    )

    if request.method == "POST":
        answer.delete()
        messages.success(request, "Interview answer deleted successfully.")
        return redirect("interview_history")

    return redirect("interview_history")


# This function deletes one project-defense answer.
# It only allows the logged-in user to delete their own project-defense answer.
@login_required
def delete_project_answer(request, answer_id):
    answer = get_object_or_404(
        ProjectDefenseAnswer,
        id=answer_id,
        session__user=request.user
    )

    if request.method == "POST":
        answer.delete()
        messages.success(request, "Project-defense answer deleted successfully.")
        return redirect("project_history")

    return redirect("project_history")