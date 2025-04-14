FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev
WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install --upgrade pip && pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu && pip install accelerate==1.6.0 && pip install -r /app/requirements.txt
CMD ["python", "main.py"]

