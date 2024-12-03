FROM python:3.12.7-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir poetry \
  && poetry config virtualenvs.in-project true
RUN poetry install

ENV PYTHONUNBUFFERED=on

CMD ["poetry", "run", "uvicorn", "serve:app", "--host=0.0.0.0", "--port=8080"]

