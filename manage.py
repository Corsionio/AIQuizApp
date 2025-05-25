import os
import sys

def run_setup_hook():
    try:
        from quiz.startup import create_default_admin
        create_default_admin()
    except Exception as e:
        print(f"Admin setup skipped: {e}")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

    try:
        import django
        django.setup()

        # Only call admin setup for runserver
        if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
            run_setup_hook()

        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH?"
        ) from exc
