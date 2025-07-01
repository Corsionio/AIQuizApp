from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RegisterForm, LoginForm
from .generate_question import save_to_db
from django.views.decorators.http import require_POST
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count, Avg
from quiz.models import Question, RightAnswer, QuestionVote, User, Admin, QuizAttempt
import random
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def home(request):
    return render(request, 'quiz/home.html')

def auth_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('quiz:home')
        else:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('quiz:home')

    return render(request, 'quiz/auth.html', {
        'login_form': login_form,
        'register_form': register_form
    })

def logout_view(request):
    logout(request)
    return redirect('quiz:home')

@staff_member_required
def manage_questions(request):
    questions = (
        Question.objects
        .annotate(vote_count=Count('questionvote'))
        .values('qnum', 'text', 'vote_count')
    )
    return render(request, 'quiz/manage_questions.html', {'questions': questions})

@staff_member_required
def manage_users(request):
    users = User.objects.all().values('id', 'username', 'email', 'is_staff')
    return render(request, 'quiz/manage_users.html', {'users': users})

@require_POST
def delete_question(request, qnum):
    RightAnswer.objects.filter(qnum_id=qnum).delete()
    Question.objects.filter(qnum=qnum).delete()
    return redirect('quiz:manage_questions')

@staff_member_required
@require_POST
def delete_all_questions(request):
    RightAnswer.objects.all().delete()
    Question.objects.all().delete()
    return redirect('quiz:manage_questions')

@staff_member_required
def delete_user(request, user_id):
    user = User.objects.filter(id=user_id, is_staff=False).first()
    if user:
        user.delete()
    return redirect('quiz:manage_users')

@staff_member_required
@require_POST
def promote_user(request, user_id):
    user = User.objects.filter(id=user_id, is_staff=False).first()
    if user:
        user.is_staff = True
        user.save()
        Admin.objects.get_or_create(user=user)
    return redirect('quiz:manage_users')

def start_quiz(request):
    all_questions = list(Question.objects.all())
    random.shuffle(all_questions)
    selected_questions = all_questions[:10]
    quiz_questions = []

    for q in selected_questions:
        correct = q.rightanswer.text.strip().strip("[]\"'") if hasattr(q, 'rightanswer') else ""
        wrongs = json.loads(q.wrong_answers)
        options = [a.strip().strip("[]\"'") for a in wrongs[:3]] + [correct]
        random.shuffle(options)
        quiz_questions.append({'qnum': q.qnum, 'text': q.text, 'option_list': options})

    request.session['quiz_qnums'] = [q['qnum'] for q in quiz_questions]

    if request.user.is_authenticated:
        attempt = QuizAttempt.objects.create(user=request.user, score=0, total=len(quiz_questions))
        request.session['current_attempt_id'] = attempt.id
    else:
        request.session['current_attempt_id'] = None

    return render(request, 'quiz/quiz.html', {'questions': quiz_questions})

def submit_quiz(request):
    if request.method == 'POST':
        quiz_qnums = request.session.get('quiz_qnums', [])
        questions = list(
            Question.objects.filter(qnum__in=quiz_qnums)
            .select_related('rightanswer')
            .annotate(vote_count=Count('questionvote'))
        )

        score, results = 0, []

        for q in questions:
            selected = request.POST.get(f"question_{q.qnum}")
            correct = q.rightanswer.text
            is_correct = selected == correct
            if is_correct:
                score += 1

            q.trust_rating = (q.trust_rating + (1.0 if is_correct else 0.0)) / 2
            q.save()

            results.append({
                'text': q.text,
                'selected': selected,
                'correct': correct,
                'is_correct': is_correct,
                'explanation': q.explanation
            })

            if q.vote_count >= 3 and q.trust_rating < 0.6:
                q.delete()
                save_to_db()

        # Calculate average only for logged-in users
        if request.user.is_authenticated:
            avg = QuizAttempt.objects.filter(user=request.user).aggregate(
                avg=Avg('score') * 1.0 / Avg('total')
            )['avg'] or 0.0
        else:
            avg = None

        return render(request, 'quiz/result.html', {
            'score': score,
            'total': len(questions),
            'results': results,
            'avg': avg * 100 if avg is not None else None
        })

    return redirect('quiz:home')

@staff_member_required
@require_POST
def generate_questions(request):
    count = 0
    for _ in range(10):
        if save_to_db():
            count += 1
    return redirect('quiz:manage_questions')

@csrf_exempt
@login_required
@require_POST
def vote_question(request, qnum, vote_value):
    vote_val = 1 if vote_value == 'up' else 0
    attempt_id = request.session.get('current_attempt_id')
    if not attempt_id:
        return JsonResponse({"status": "error", "message": "No active quiz attempt."})

    QuestionVote.objects.create(user_id=request.user.id, qnum_id=qnum, vote=vote_val, attempt_id=attempt_id)

    updated = QuestionVote.objects.filter(qnum_id=qnum).aggregate(avg=Avg('vote'))['avg']
    Question.objects.filter(qnum=qnum).update(trust_rating=updated)

    return JsonResponse({"status": "success"})