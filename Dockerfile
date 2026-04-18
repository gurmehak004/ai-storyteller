
FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Gradio needs the server name to be 0.0.0.0 to work inside Docker
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Expose the port for your app
EXPOSE 7860

# Command to run your FastAPI + Gradio app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]