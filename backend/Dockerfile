FROM python:3.7

RUN mkdir /api
WORKDIR /api

RUN apt update && \
    apt install -y postgresql-client && \
    apt install -y pipenv

COPY . .
RUN pipenv install --deploy --system

EXPOSE 8000
# CMD ["pipenv", "run", "uvicorn", "app:app", "--host", "0.0.0.0"]
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]