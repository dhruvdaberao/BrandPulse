# Use the official Python 3.10 image as the base
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the working directory
COPY . .

# Expose the port your Flask application will run on. Render typically uses port 10000.
EXPOSE 8000

# Set environment variables for Flask
ENV FLASK_APP=app.py

# Set the Flask environment to production for better performance and security
ENV FLASK_ENV=production

# Command to run the Flask application using Gunicorn (recommended for production)
# 'app:app' means the 'app' instance from the 'app.py' module
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]