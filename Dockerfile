# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=vschools.settings

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file into the container
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set permissions for media and static directories
RUN chmod -R 755 /app/media /app/staticfiles

# Add volumes for media and static files
VOLUME /app/media

# Collect static files
# RUN python manage.py collectstatic  --noinput

# Add an entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
# RUN python manage.py migrate

# Expose port 8000
EXPOSE 8000
#
## Set the entrypoint
#ENTRYPOINT ["/app/entrypoint.sh"]
ENTRYPOINT ["sh", "-c", "python manage.py collectstatic --no-input; python manage.py makemigrations; python manage.py migrate; python manage.py runserver 0.0.0.0:8000"]
#CMD ["python", "manage.py", "migrate", "&&", "python", "manage.py", "runserver", "0.0.0.0:8000", "--asgi"]