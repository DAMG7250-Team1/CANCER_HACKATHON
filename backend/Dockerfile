# Use the official slim Python image
FROM python:3.11-slim

# Set working dir & make it importable
WORKDIR /app
ENV PYTHONPATH=/app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code for both services
COPY backend/ backend/
COPY mcp/     mcp/

# Expose your FastAPI port
EXPOSE 8000

# Launch uvicorn pointing to your app in backend/main.py
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
