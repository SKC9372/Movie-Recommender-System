# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy your app files into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask/Gunicorn will run on
EXPOSE 8080

# Start the app using Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers=1", "--threads=2"]
