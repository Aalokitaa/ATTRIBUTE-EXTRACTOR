FROM python:3.10-slim

# Set working directory
WORKDIR "/app"

# Copy requirements file first to utilize Docker layer caching
COPY "requirements.txt" "/app/"

# Install dependencies
RUN pip install --no-cache-dir -r "requirements.txt"

# Copy code modules, data, and trained models
COPY "src" "/app/src"
COPY "data" "/app/data"
COPY "api" "/app/api"
COPY "models" "/app/models"
COPY "frontend" "/app/frontend"

# Expose port 8000
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
