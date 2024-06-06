FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install poetry 

RUN poetry install

RUN pip install django

EXPOSE 8000

CMD poetry run python manage.py runserver 0.0.0.0:8000