# Databases

Transferred from original github project to this one for app deployment

Run by doing: py manage.py runserver

If you want to create a new db do: 
py manage.py makemigrations
py manage.py migrate
py manage.py runserver

If you're running locally, switch is_admin to a 1 on any user to make them an admin and start generating questions (must be using own Open_AI env key)

Otherwise, currently running on: [https://codequestions-h0bkfkbvckdwaxfv.eastus-01.azurewebsites.net/](https://codequestions-h0bkfkbvckdwaxfv.eastus-01.azurewebsites.net/)

Requirements:
pip install django
pip install openai
pip install dotenv
