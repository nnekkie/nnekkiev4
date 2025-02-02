APP_PORT=${PORT:-8000}

cd /app/


# Run gunicorn
/opt/venv/bin/gunicorn facebook_prj.wsgi:application --bind "0.0.0.0:${APP_PORT}"