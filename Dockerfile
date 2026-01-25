FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Django using Gunicorn
CMD ["gunicorn", "adaptlearn.wsgi:application", "--bind", "0.0.0.0:8080"]

pip freeze > requirements.txt