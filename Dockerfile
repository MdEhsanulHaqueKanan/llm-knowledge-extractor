# Use a slim and secure Python base image
FROM python:3.9-slim

# Set environment variables for production best practices
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download NLTK data during the build to prevent runtime timeouts and errors.
RUN python -m nltk.downloader punkt stopwords averaged_perceptron_tagger

# Copy application and test code into the container
COPY ./app /app/app
COPY config.py .
COPY ./tests /app/tests

EXPOSE 8000

# Run the app with a production-grade WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.main:app"]