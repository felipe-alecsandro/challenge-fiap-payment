# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your Django app will run on
EXPOSE 8000

# Define the command to run your Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
