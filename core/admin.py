from django.contrib import admin

from .models import (
    InterviewSession,
    InterviewAnswer,
    ProjectDefenseSession,
    ProjectDefenseAnswer,
    ResumeAnalysis
)


# This admin class shows mock interview sessions in a clean table.
# It helps admin see which user created which interview session.
@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'role',
        'difficulty',
        'company_type',
        'created_at'
    )

    search_fields = (
        'user__username',
        'user__email',
        'role',
        'difficulty',
        'company_type'
    )

    list_filter = (
        'difficulty',
        'company_type',
        'created_at'
    )


# This admin class shows normal interview answers and AI feedback.
# It helps admin review user answers, scores, weak areas, and feedback.
@admin.register(InterviewAnswer)
class InterviewAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'session',
        'score',
        'weakness_tags',
        'created_at'
    )

    search_fields = (
        'session__user__username',
        'session__user__email',
        'question',
        'user_answer',
        'ai_feedback',
        'weakness_tags'
    )

    list_filter = (
        'score',
        'created_at'
    )


# This admin class shows project defense sessions.
# It helps admin see which user practiced which resume project.
@admin.register(ProjectDefenseSession)
class ProjectDefenseSessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'project_title',
        'target_role',
        'created_at'
    )

    search_fields = (
        'user__username',
        'user__email',
        'project_title',
        'technologies',
        'target_role'
    )

    list_filter = (
        'target_role',
        'created_at'
    )


# This admin class shows project defense answers and AI feedback.
# It helps admin check scores, weak areas, and project explanation quality.
@admin.register(ProjectDefenseAnswer)
class ProjectDefenseAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'session',
        'score',
        'weakness_tags',
        'created_at'
    )

    search_fields = (
        'session__user__username',
        'session__user__email',
        'question',
        'user_answer',
        'ai_feedback',
        'weakness_tags'
    )

    list_filter = (
        'score',
        'created_at'
    )


# This admin class shows uploaded resumes and AI resume analysis.
# It helps admin check which user uploaded a resume and view the AI analysis.
@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'resume_file',
        'created_at'
    )

    search_fields = (
        'user__username',
        'user__email',
        'extracted_text',
        'ai_analysis'
    )

    list_filter = (
        'created_at',
    )