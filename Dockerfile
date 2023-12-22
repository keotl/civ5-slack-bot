FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY civbot /app/civbot

ENV PYTHONPATH /app

RUN adduser app -G nobody -u 2000 -D -H
#RUN chown -R app:app /app
USER app:nobody

EXPOSE 8080
CMD ["sh", "-c", "gunicorn --workers=${GUNICORN_WORKERS:-1} --threads=${GUNICORN_THREADS:-4} --timeout=10 --bind=0.0.0.0:${PORT:-8080} civbot.main"]