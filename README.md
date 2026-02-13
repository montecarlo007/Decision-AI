# 🧠 Decision AI Platform

[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Latest-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_AI-blue?style=for-the-badge)](https://ollama.ai/)
[![Celery](https://img.shields.io/badge/Celery-Distributed_Tasks-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)

**Decision AI** is a powerful, locally-hosted educational platform designed to transform your learning materials into intelligent summaries, flashcards, and interactive assessments. 

---

## ✨ Key Features

### 📄 Content Intelligence
- **Universal File Support**: Upload PDF, DOCX, TXT, and Images.
- **AI OCR**: Integrated text extraction from images and scanned documents.
- **Smart Summarization**: Get high-level overviews and key concepts instantly.
- **Flashcard Generation**: Auto-created flashcards for efficient active recall.

### 📝 Interactive Assessments
- **Customizable Quizzes**: Generate quizzes with specific **Difficulty Levels** (Easy, Medium, Hard).
- **Question Volume Control**: Choose exactly how many questions you want to generate.
- **Adaptive Question Types**: Mix of Multiple Choice, True/False, and Open Ended (Advanced Matching/Sequencing coming soon!).
- **Instant Feedback**: Detailed results with scores and explanations for every answer.

### 📊 Deep Analytics
- **Performance Tracking**: Visual charts showing your progress over time.
- **Global Stats**: Admin dashboard for monitoring system-wide usage.

---

## 🛠️ Tech Stack

- **Backend**: Django 5.0 (Python)
- **Database**: MongoDB (via MongoEngine)
- **AI Engine**: Ollama (Running local models like Llama 3.2:1b)
- **Task Queue**: Celery + Redis
- **Frontend**: TailwindCSS + Vanilla JS
- **Visuals**: Matplotlib & Pandas for analytics

---

## 🚀 Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.9+](https://www.python.org/downloads/) (for local development)

### One-Click Setup (Docker)

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd Quiz_flash_card
   ```

2. **Run the services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the app**:
   - 🌐 **Web Interface**: [http://localhost:8000](http://localhost:8000)
   - 🛠️ **Admin Panel**: [http://localhost:8000/admin-dashboard/](http://localhost:8000/admin-dashboard/)

---

## 🔧 Maintenance & Utilities

We include several helper scripts to manage your local environment:

| Script | Purpose |
| :--- | :--- |
| `verify_connections.py` | Checks MongoDB, Redis, and Ollama connectivity. |
| `create_admin.py` | Quickly creates an admin user for the dashboard. |
| `check_ollama.py` | Verifies the AI engine and available models. |
| `change_role.py` | Modifies user permissions (Admin/User). |

---

## 🛡️ Troubleshooting

- **Processing Stalls**: If documents remain in "Processing", check the Celery worker logs:
  ```bash
  docker-compose logs worker
  ```
- **Connection Issues**: Ensure your `.env` file is correctly configured. If using host-only Ollama, set `OLLAMA_BASE_URL=http://host.docker.internal:11434`.

---

*Built with ❤️ for better learning.*
