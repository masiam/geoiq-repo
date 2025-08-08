# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY app.py .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
