from app import create_app

# The application instance is created by the factory function.
app = create_app()

if __name__ == '__main__':
    # This block is executed only when you run 'python app/main.py' directly.
    # It starts Flask's built-in development server.
    # Note: This server is not suitable for production. Gunicorn will be used in our Docker container.
    app.run(host='0.0.0.0', port=5000)