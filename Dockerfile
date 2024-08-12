# Use the official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy all files from the current directory to the working directory in the container
COPY . .

RUN apt-get update \
    && apt-get install -y python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libcairo2 libpq-dev libpangocairo-1.0-0
# Install pipenv
RUN pip install pipenv
# Install dependencies
RUN pipenv install --system --deploy

# Run Django migrations
RUN python manage.py migrate

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]