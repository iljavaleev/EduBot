FROM python:3.11-slim

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./bots/telegram/ .

CMD ["python", "bot.py"]
