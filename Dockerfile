FROM python:3.7.4

COPY . /app
WORKDIR /app
ENV PYTHONPATH /app

ENV PIP_NO_CACHE_DIR 1

RUN pip install --no-cache-dir pipenv && pipenv install --system --deploy --dev

CMD ["sh", "/app/run.sh"]

