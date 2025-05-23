# 1. Base image
FROM python:3.11-slim

# 2. Set a working directory
WORKDIR /app

# 3. Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your source code
COPY . .            
COPY ../mcp ./mcp   

# 5. Expose the port your FastAPI runs on
EXPOSE 8000

# 6. (Optional) Pre-download SpaCy model if needed
# RUN python -m spacy download en_core_web_sm

# 7. Default command to run the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
