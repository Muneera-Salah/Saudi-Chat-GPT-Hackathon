web: gunicorn gettingstarted.wsgi
web: gunicorn ddata.wsgi
web: gunicorn ddata.wsgi:application --log-file - --log-level debug
heroku ps:scale web=1
python manage.py collectstatic --noinput
web: gunicorn ddata.wsgi --log-file -