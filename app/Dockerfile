FROM python:3.12-alpine3.21
WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install --upgrade pip && pip install -r /app/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

