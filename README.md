# RAGdoll

A FastAPI-based service for managing and retrieving chat context using Retrieval-Augmented Generation (RAG) principles with placeholder embeddings and a PostgreSQL database. This service allows storing user messages and model responses, and retrieving relevant past messages based on (placeholder) semantic similarity.

## Project Structure

```
RAGdoll/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── embedding.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── context_service.py
│   ├── main.py
│   └── __init__.py
├── requirements.txt
├── .env
└── README.md
```

## Setup Instructions

### 1. Clone the Repository (if applicable)
If this project were on a version control system:
```bash
git clone https://github.com/roshan-c/RAGdoll.git
cd RAGdoll
```

### 2. Create and Activate a Virtual Environment
It\'s highly recommended to use a virtual environment.

**Using `venv` (standard Python):**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
```

**Using `uv` (if you have it installed):**
```bash
uv venv
source .venv/bin/activate # On Windows: .venv\\Scripts\\activate
```

### 3. Install Dependencies
Install the required Python packages from `requirements.txt`:

**Using `pip`:**
```bash
pip install -r requirements.txt
```

**Using `uv`:**
```bash
uv pip install -r requirements.txt
```
The `requirements.txt` includes: `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `pgvector`, `numpy`, `python-dotenv`.

### 4. Configure Environment Variables (`.env` file)
Create a `.env` file in the root of the `RAGdoll` directory. It should contain your database connection URL and your OpenAI API Key.

Copy the example below and update it with your actual database credentials and OpenAI API Key:
```env
# .env
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydatabase
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE # Add your OpenAI API Key
EMBEDDING_DIMENSION=1536 # Updated to reflect the model used (text-embedding-3-small)
```
The `EMBEDDING_DIMENSION` is set to 1536 in `app/core/config.py` to match the `text-embedding-3-small` OpenAI model.

**Obtaining an OpenAI API Key:**
1.  Go to [https://platform.openai.com/](https://platform.openai.com/).
2.  Sign up or log in to your account.
3.  Navigate to the API keys section of your account settings (usually under "API Keys" or your organization settings).
4.  Create a new secret key. **Copy this key immediately and store it securely.** You will not be able to see it again.
5.  Add this key to your `.env` file as `OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE`.

The application uses the `text-embedding-3-small` model from OpenAI for generating message embeddings.

### 5. Set Up PostgreSQL Database with pgvector

#### Option A: Using Docker (Recommended for Development)
This is the easiest way to get a PostgreSQL instance with the `pgvector` extension running.

1.  **Ensure Docker is installed and running.**
2.  **Run the PostgreSQL container with pgvector:**
    ```bash
    docker run -d --name ragdoll-postgres-db -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 -v ragdoll-pgdata:/var/lib/postgresql/data pgvector/pgvector:pg16
    ```
    *   Replace `myuser`, `mypassword`, `mydatabase` if you wish, but ensure they match your `.env` file.
    *   `ragdoll-pgdata` is a Docker volume to persist data.

3.  **Connect and enable the `vector` extension:**
    ```bash
    docker exec -it ragdoll-postgres-db psql -U myuser -d mydatabase
    ```
    When prompted for the password, enter it (e.g., `mypassword`).
    Inside `psql`, run:
    ```sql
    CREATE EXTENSION IF NOT EXISTS vector;
    \q
    ```

#### Option B: Manual PostgreSQL Setup
If you have an existing PostgreSQL server:
1.  Ensure PostgreSQL is version 11 or higher.
2.  Install the `pgvector` extension. Instructions vary by OS and PostgreSQL version. Refer to the [official pgvector documentation](https://github.com/pgvector/pgvector).
3.  Create a database, user, and grant permissions.
4.  Update your `.env` file with the correct `DATABASE_URL`.

### 6. Create Database Tables
Once your `.env` file is configured and the database is running with the `pgvector` extension enabled, run the following script from the `RAGdoll` root directory to create the necessary tables:

```bash
python -c "from app.db.models import Base; from app.core.database import engine; Base.metadata.create_all(bind=engine); print('Tables created (if they didn\'t exist).')"
```

## Running the Application

With the setup complete and your virtual environment activated:

1.  Navigate to the `RAGdoll` root directory.
2.  Run the FastAPI application using Uvicorn:
    ```bash
    PYTHONPATH=$PYTHONPATH:. uvicorn app.main:app --reload
    ```
    *   `PYTHONPATH=$PYTHONPATH:.` helps Python find the `app` module correctly.
    *   `--reload` enables auto-reloading on code changes, useful for development.

The service should now be running on `http://127.0.0.1:8000`.

## Basic API Usage

You can interact with the API using tools like `curl`, Postman, or by visiting the auto-generated interactive documentation at `http://127.0.0.1:8000/docs`.

### Store a User Message and Get Context
```bash
curl -X POST http://127.0.0.1:8000/message \\
-H "Content-Type: application/json" \\
-d '{
    "session_id": "chat_session_123",
    "content": "Hello, how does this context retrieval work?",
    "user_id": "user_alpha"
}'
```
**Expected Response (example):**
```json
{
    "status": "success",
    "message": "User message stored and relevant context retrieved.",
    "stored_message_id": 1,
    "session_id": "chat_session_123",
    "role": "user",
    "retrieved_context": [
        // ... list of {"role": "...", "content": "..."} objects
    ]
}
```

### Store a Model Response
```bash
curl -X POST http://127.0.0.1:8000/response \\
-H "Content-Type: application/json" \\
-d '{
    "session_id": "chat_session_123",
    "content": "This service uses vector embeddings of messages to find semantically similar past messages within the same session."
}'
```
**Expected Response (example):**
```json
{
    "status": "success",
    "message": "Model response stored successfully.",
    "stored_response_id": 2,
    "session_id": "chat_session_123",
    "role": "model"
}
```
