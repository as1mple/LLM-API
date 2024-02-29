FROM python:3.9

COPY requirements.txt ./requirements.txt

RUN python -m pip install -U pip && \
    python -m pip install -r requirements.txt && \
    python -m pip cache purge

COPY ./src /app/src
COPY ./models /app/models

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]