# Base image with Python
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/llm-app"

# Variables to use with the Flask api
ENV LLM_NAME=${LLM_NAME}
ENV LLM_SECRET=${LLM_API_KEY}
ENV LLM_API_URL=${LLM_API_URL}
ENV LLM_TEMPERATURE=${LLM_TEMPERATURE}

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
CMD ["python", "-m", "api.app"]