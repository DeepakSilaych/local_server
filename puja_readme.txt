[one timer commands] (path = local_server directory)

command: pip install venv                    # if already not installed
command: python -m venv env
command: source env/bin/activate
command: pip install -r reqirements.txt


[run everytime] (in local_server directory)

command: python manage.py runserver

to download: http://localhost:8000/check
to gfs: http://localhost:8000/gfs
to hourly: http://localhost:8000/hourly
to daily: http://localhost:8000/daily

