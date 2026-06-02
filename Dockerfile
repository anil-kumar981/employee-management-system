# Use the official slim Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Set environment variables
# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for building PostgreSQL drivers and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY . .

# Expose Flask / Uvicorn server port
EXPOSE 5000

CMD ["python", "main.py"]
