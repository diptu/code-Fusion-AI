# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port 8000
EXPOSE 8000

# Run migrations
RUN python manage.py migrate

# Run makemigrations (only needed if model changes occurred)
RUN python manage.py makemigrations --noinput

# Create static files
RUN python manage.py collectstatic --noinput

# Run the setup_users script
RUN python manage.py shell -c "from utils import setup_users; setup_users()"

# Run the country data fetching script
RUN python manage.py shell -c "from countries.utils import fetch_and_store_countries; fetch_and_store_countries()"

# Start the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
