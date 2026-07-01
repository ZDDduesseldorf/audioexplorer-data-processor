FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV TRANSFORMERS_CACHE=/app/.cache/huggingface

ARG AUDIOEXPLORER_DATA_DIR
ENV AUDIOEXPLORER_DATA_DIR=${AUDIOEXPLORER_DATA_DIR}

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY app ./app
COPY ${AUDIOEXPLORER_DATA_DIR} ./${AUDIOEXPLORER_DATA_DIR}

CMD ["python", "-m", "app.main"]