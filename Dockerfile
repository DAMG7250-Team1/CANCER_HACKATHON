# Use the official slim Python image
FROM python:3.11-slim

# Set working dir & make it importable
WORKDIR /app
ENV PYTHONPATH=/app

# Install dependencies from backend requirements
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and mcp code into the image
COPY backend/ ./backend/
COPY backend/core/ ./core/
COPY backend/features/ ./features/
COPY mcp/ ./mcp/


# Expose FastAPI port
EXPOSE 8000

# Launch uvicorn, pointing at backend/main.py
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
