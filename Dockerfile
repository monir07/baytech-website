# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install PostgreSQL development libraries and other dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your Django app will run on
EXPOSE 8000

# Add an entrypoint script to handle the database migration and user creation
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Run the entrypoint script by default
ENTRYPOINT ["/docker-entrypoint.sh"]

# Default command to run Django's development server
CMD ["python", "manage.py", "runserver"]