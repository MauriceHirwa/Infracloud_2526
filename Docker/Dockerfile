# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Avoid pip using fancy progress bars / threads
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

# Copy application code
COPY flask_app_login.py .
COPY templates/ templates/
COPY static/ static/

# Expose application port
EXPOSE 5555

# Run the Flask application
CMD ["python", "flask_app_login.py"]