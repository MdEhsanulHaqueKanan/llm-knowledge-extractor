# LLM Knowledge Extractor
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9B71?style=for-the-badge&logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)


This project is a prototype API that accepts unstructured text, uses a mock LLM to generate a summary and structured metadata, and persists the analysis in a database. It was developed as a take-home assignment for the Senior Software Engineer role at Jouster.

The system is fully containerized with Docker, includes a suite of automated tests, and handles batch processing and edge cases, demonstrating a production-minded approach to a rapid prototype.

## Design Choices

This system was architected to be robust, scalable, and maintainable, reflecting modern software engineering best practices.

1.  **Modular & Scalable Architecture:** I used a modular structure (separating API, core logic, and database) with a Flask application factory. This pattern makes the codebase highly maintainable, testable, and easy to extend with new features without refactoring existing code.

2.  **Strategic Use of a Mock Service:** Instead of requiring a live LLM API key, I implemented an "intelligent mock" service. This was a deliberate choice to **guarantee a zero-friction, zero-cost setup for the reviewer**, focus the exercise on the system architecture itself, and enable fully deterministic testing of all code paths, including the "LLM failure" edge case. The architecture is pluggable, allowing this mock to be swapped with a real LLM service (e.g., OpenAI, Ollama) with a single line of code change.

3.  **Production-Ready Tooling:**
    *   **Docker & Gunicorn:** The application is containerized and served via Gunicorn, demonstrating an understanding of production deployment practices over using Flask's development server.
    *   **SQLAlchemy ORM:** By using an ORM, the application is decoupled from the underlying database. It runs on SQLite for simplicity but can be switched to PostgreSQL in production by changing a single environment variable, showcasing foresight for scalability.
    *   **Pytest:** A comprehensive test suite validates all core functionality and edge cases, ensuring reliability and simplifying future development.

## Trade-offs and Future Improvements

Given the time constraint, I prioritized a clean architecture, full test coverage, and robust core functionality. If this were a production system, my next steps would be:

*   **Asynchronous Processing:** The `/analyze` endpoint processes requests synchronously. For long-running LLM calls, I would integrate a task queue like **Celery** with **Redis** to process analyses asynchronously, improving API responsiveness and throughput.
*   **Concrete LLM Implementation:** I would replace the `MockLLMService` with a concrete implementation (e.g., `OpenAILLMService`) and manage API keys securely via environment variables.
*   **Advanced Database Search:** For the `/search` endpoint, searching within JSON strings is sufficient for a prototype. In production, I would use a database with native JSONB support (like PostgreSQL) and indexing for efficient querying or implement a dedicated search index like Elasticsearch.

## Setup and Run Instructions

### Prerequisites
*   Docker and Docker Compose

### Running the Application (Recommended)

This is the simplest and most reliable way to run the project.

1.  **Clone the repository.**
2.  **Navigate to the project's root directory.**
3.  **Build and run the container using Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    The API will be available at `http://localhost:8000`. The SQLite database will be persisted in a new `app_instance` directory that is created in the project root.

### Running Automated Tests

To run the full suite of tests against the application (while the container is running in another terminal):

```bash
docker-compose exec web pytest
```

## API Endpoints

### 1. Analyze Text

*   **Endpoint:** `POST /api/analyze`
*   **Description:** Processes one or more blocks of text.

*   **Request Body (Single):**
    ```json
    {
        "texts": ["Your text about technology and innovation goes here."]
    }
    ```

*   **Request Body (Batch):**
    ```json
    {
        "texts": ["First text block.", "Second text block."]
    }
    ```

*   **Success Response (201 Created):**
    ```json
    {
        "id": 1,
        "summary": "This is a mock summary...",
        "title": "A Mock Analysis",
        "topics": ["mock data", "software testing", "prototyping"],
        "sentiment": "neutral",
        "keywords": ["technology", "innovation"],
        "confidence": 0.95
    }
    ```

### 2. Search Analyses

*   **Endpoint:** `GET /api/search`
*   **Description:** Searches for stored analyses by topic or keyword.

*   **Query Parameter:**
    *   `topic` (string, required): The term to search for.

*   **Example Request:**
    `GET http://localhost:8000/api/search?topic=prototyping`

*   **Success Response (200 OK):**
    ```json
    [
        {
            "id": 1,
            "summary": "This is a mock summary...",
            "title": "A Mock Analysis",
            "topics": ["mock data", "software testing", "prototyping"],
            "sentiment": "neutral",
            "keywords": ["technology", "innovation"],
            "confidence": 0.95
        }
    ]
    ```