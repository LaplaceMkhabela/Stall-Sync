FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Expose port for Cloud Run
EXPOSE 8080
# Use a bash script to run both services, or deploy them as separate Cloud Run services (Recommended)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]