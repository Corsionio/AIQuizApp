from django.db import connection
from django.contrib.auth.models import AbstractUser
from django.db import models

#defined here because it gives security automatically to user fields
class User(AbstractUser):
            created_at = models.DateTimeField(auto_now_add=True)
class Admin:
    pass

class Question:
    pass

class RightAnswer:
    pass

class QuizAttempt:
    pass

def create_tables():
    with connection.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_admin (
            user_id INTEGER PRIMARY KEY,
            admin_level INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES quiz_user(id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_question (
            qnum INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            wrong_answers TEXT NOT NULL,
            trust_rating FLOAT NOT NULL DEFAULT 0.0,
            explanation TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_rightanswer (
            qnum_id INTEGER PRIMARY KEY,
            text TEXT NOT NULL,
            FOREIGN KEY(qnum_id) REFERENCES quiz_question(qnum) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_quizattempt (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            taken_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES quiz_user(id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_questionvote (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            qnum_id INTEGER NOT NULL,
            vote INTEGER NOT NULL CHECK(vote IN (0, 1)),
            attempt_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES quiz_user(id) ON DELETE CASCADE,
            FOREIGN KEY(qnum_id) REFERENCES quiz_question(qnum) ON DELETE CASCADE,
            FOREIGN KEY(attempt_id) REFERENCES quiz_quizattempt(id) ON DELETE CASCADE
        )
        """)

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully")
