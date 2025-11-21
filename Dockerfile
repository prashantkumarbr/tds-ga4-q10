# Use latest Playwright image with Python 3.12
FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements first (for caching)
COPY requirements.txt .

# Remove playwright from requirements since it's already in base image
RUN sed -i '/playwright/d' requirements.txt

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 10000

# Use PORT environment variable (Render sets this automatically)
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}
