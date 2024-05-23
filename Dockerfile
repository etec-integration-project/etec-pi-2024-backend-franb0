FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip

# Set working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Start the application
CMD ["python", "app.py"]
