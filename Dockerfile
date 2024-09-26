# Use the official Python image with slim version 3.9
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 3003

# Start the application
CMD ["python", "app/app.py"]























# # Use the official Python image with slim version 3.9
# FROM python:3.9-slim

# # Install system dependencies
# # RUN apt-get update && apt-get install -y \
# #     python3-pip  # Install pip for Python 3

# # Set working directory in the container
# WORKDIR /app

# # Copy requirements file and install Python dependencies
# COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code
# COPY . .

# # Expose the port the app runs on
# EXPOSE 3003

# # Start the application
# CMD ["python", "app/app.py"]
