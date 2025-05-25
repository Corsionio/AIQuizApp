from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    admin_level = models.IntegerField(default=1)

class Question(models.Model):
    qnum = models.AutoField(primary_key=True)
    text = models.TextField()
    wrong_answers = models.TextField()
    trust_rating = models.FloatField(default=0.0)
    explanation = models.TextField(blank=True, null=True)

class RightAnswer(models.Model):
    qnum = models.OneToOneField(Question, on_delete=models.CASCADE, primary_key=True)
    text = models.TextField()

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    taken_at = models.DateTimeField(auto_now_add=True)

class QuestionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qnum = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=[(0, "Down"), (1, "Up")])
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
