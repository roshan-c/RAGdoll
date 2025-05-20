from app.core.config import settings

print(f"Loaded DATABASE_URL: {settings.DATABASE_URL}")
print(f"Loaded OPENAI_API_KEY: {settings.OPENAI_API_KEY}")
print(f"Loaded EMBEDDING_DIMENSION: {settings.EMBEDDING_DIMENSION}")
