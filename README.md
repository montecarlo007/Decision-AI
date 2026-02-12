# Decision AI Platform

A production-ready AI-powered educational platform using Django, MongoDB, Ollama, and Celery.

## Prerequisites

- Docker Desktop installed
- Git

## Setup & Running

1.  **Clone/Open the project** in your terminal.
2.  **Ensure Ollama is running** (optional if using Docker only, but usually better to have model pulled locally):
    ```bash
    ollama pull qwen3:30b  #42
    ```
    *Note: The docker-compose includes an `ollama` service. If you have a local GPU, uncomment the GPU section in `docker-compose.yml`.*

3.  **Build and Start**:
    ```bash
    docker-compose up --build
    ```

4.  **Access the Application**:
    - Web Interface: http://localhost:8000
    - Admin Dashboard: http://localhost:8000/admin-dashboard/ (Must register and manually set role to 'admin' in Mongo for now, or use a script)

## Creating an Admin User

Since there is no default superuser command for this custom mongo setup, you can create a user via the registration page, then access the mongo shell to promote them:

1.  Register at `/auth/register/`.
2.  Run:
    ```bash
    docker-compose exec db mongosh decision_db
    > db.users.updateMany({email: "your@email.com"}, {$set: {role: "admin"}})
    ```

## Features

-   **File Upload**: Supports PDF, DOCX, TXT, Images (OCR).
-   **AI Processing**: Summarization and Adaptive Quiz generation using local Ollama.
-   **Analytics**: Student performance tracking and Admin global stats using Pandas & Matplotlib.
-   **Architecture**:
    -   Django 5 (Web Framework)
    -   MongoDB (NoSQL Database)
    -   Celery + Redis (Async Tasks)
    -   TailwindCSS (Frontend)

## Troubleshooting

-   **Ollama Connection**: Ensure `OLLAMA_BASE_URL` in `.env` matches your setup. If running Ollama on host, use `http://host.docker.internal:11434`.
-   **Celery**: Check logs `docker-compose logs worker` if documents stick in "Processing".
