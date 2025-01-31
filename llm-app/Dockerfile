# Base image with Python
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /llm-app

# Copy only necessary files to the container
COPY requirements.txt /llm-app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /llm-app

# Expose the port for the Flask API
EXPOSE 5000

# Default command to run the Flask app
CMD ["python", "api/app.py"]