FROM python:3.12-slim

WORKDIR /app

COPY ./ /app
COPY ./config /app/config
RUN pip install fastapi uvicorn[standard] httpx websockets jsonschema

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
