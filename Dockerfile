# Stage 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables for best practices
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- NEW STEP: Download NLTK data during the build ---
# This ensures the data is present in the image before the server ever starts,
# preventing runtime downloads and timeouts.
RUN python -m nltk.downloader punkt stopwords averaged_perceptron_tagger

# Copy the application and test code into the container
COPY ./app /app/app
COPY config.py .
COPY ./tests /app/tests

# Expose the port the app will run on
EXPOSE 8000

# Specify the command to run on container startup
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.main:app"]