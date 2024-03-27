# app/Dockerfile

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    virtualenv \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --home /app app && chown -R app:app /app

USER app
ENV PATH="/app/env/bin:$PATH"

RUN virtualenv env
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./* ./

EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

ENTRYPOINT ["streamlit", "run", "cvbot.py", "--server.port=8080", "--server.address=0.0.0.0"]
