from django.db import models
from django.contrib.auth.models import User


# This model stores one normal mock interview session.
# Each session belongs to one logged-in user.
class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    company_type = models.CharField(max_length=100)
    first_question = models.TextField(blank=True)
    current_question = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "No User"
        return f"{username} - {self.role} - {self.difficulty}"


# This model stores every answer submitted in a normal mock interview.
# It is connected to InterviewSession, so we can know which user owns it through session.user.
class InterviewAnswer(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    question = models.TextField()
    user_answer = models.TextField()
    ai_feedback = models.TextField(blank=True)
    score = models.IntegerField(default=0)
    weakness_tags = models.TextField(blank=True)
    better_answer = models.TextField(blank=True)
    next_question = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer for {self.session.role}"


# This model stores one project defense session.
# Each project defense session belongs to one logged-in user.
class ProjectDefenseSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project_title = models.CharField(max_length=200)
    technologies = models.TextField()
    target_role = models.CharField(max_length=100)
    project_description = models.TextField()
    current_question = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "No User"
        return f"{username} - {self.project_title}"


# This model stores each project defense answer.
# It is connected to ProjectDefenseSession, so the owner is available through session.user.
class ProjectDefenseAnswer(models.Model):
    session = models.ForeignKey(ProjectDefenseSession, on_delete=models.CASCADE)
    question = models.TextField()
    user_answer = models.TextField()
    ai_feedback = models.TextField(blank=True)
    score = models.IntegerField(default=0)
    weakness_tags = models.TextField(blank=True)
    better_answer = models.TextField(blank=True)
    next_question = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Project answer for {self.session.project_title}"


# This model stores uploaded resume files and Gemini resume analysis.
# Each resume analysis belongs to one logged-in user.
class ResumeAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    resume_file = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True)
    ai_analysis = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "No User"
        return f"{username} - Resume Analysis {self.id}"