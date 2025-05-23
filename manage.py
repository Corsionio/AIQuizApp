import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

    try:
        from django.core.management import execute_from_command_line

        # Only call create_default_admin AFTER migrations run
        if len(sys.argv) >= 2 and sys.argv[1] in ["runserver", "shell", "createsuperuser"]:
            import django
            django.setup()
            try:
                from quiz.startup import create_default_admin
                create_default_admin()
            except ImportError:
                pass

        execute_from_command_line(sys.argv)

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH?"
        ) from exc
