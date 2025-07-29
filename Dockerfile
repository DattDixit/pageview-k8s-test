# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency list and install them first
# This leverages Docker's layer caching for faster builds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# The port our Flask app will listen on
EXPOSE 5000

# The command to run when the container starts
CMD ["python", "app.py"]
