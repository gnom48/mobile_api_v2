FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /service

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y portaudio19-dev ffmpeg
RUN pip install --upgrade -r requirements.txt

COPY ./ service