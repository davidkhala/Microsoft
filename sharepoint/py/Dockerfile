FROM python:3.11-slim

LABEL maintainer="your-email@example.com"
LABEL description="SharePoint to IBM COS Connector"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .

# Create non-root user for running the app
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Use CMD to allow easy override
CMD ["python", "main.py"]
