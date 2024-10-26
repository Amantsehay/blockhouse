# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install system dependencies for PostgreSQL and building Python packages
RUN apt update && apt install -y --no-install-recommends \
    libpq-dev gcc python3-dev \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel, then install Python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Stage 2: Create the final runtime environment
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the rest of the application code to the container
COPY . .

# Set environment variable for the app to run on port 8000
ENV PORT=8000

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Health check to ensure the app is running correctly
HEALTHCHECK CMD ["python", "manage.py", "check"]
