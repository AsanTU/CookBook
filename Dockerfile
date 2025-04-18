FROM python:3.12-slim-bookworm

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["gunicorn", "auth_project.wsgi:application", "--bind", "0.0.0.0:8000"]
