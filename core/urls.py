from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    

    path('start-interview/', views.start_interview, name='start_interview'),
    path('interview-room/<int:session_id>/', views.interview_room, name='interview_room'),
    path('feedback/<int:answer_id>/', views.feedback, name='feedback'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('improvement-plan/', views.improvement_plan, name='improvement_plan'),

    path('project-defense/', views.project_defense, name='project_defense'),
    path('project-defense-room/<int:session_id>/', views.project_defense_room, name='project_defense_room'),
    path('project-defense-feedback/<int:answer_id>/', views.project_defense_feedback, name='project_defense_feedback'),
    path('resume-analyzer/', views.resume_analyzer, name='resume_analyzer'),
    path('privacy-center/', views.privacy_center, name='privacy_center'),
    path('profile/', views.profile, name='profile'),
    path('help/', views.help_page, name='help'),
    path('resume-interview/<int:analysis_id>/', views.start_resume_interview, name='start_resume_interview'),
    path('resume-history/', views.resume_history, name='resume_history'),
    path('resume-detail/<int:analysis_id>/', views.resume_detail, name='resume_detail'),
    path('delete-resume/<int:analysis_id>/', views.delete_resume_analysis, name='delete_resume_analysis'),
    path('interview-history/', views.interview_history, name='interview_history'),
    path('project-history/', views.project_history, name='project_history'),
    path('delete-interview-answer/<int:answer_id>/', views.delete_interview_answer, name='delete_interview_answer'),
    path('delete-project-answer/<int:answer_id>/', views.delete_project_answer, name='delete_project_answer'),


]