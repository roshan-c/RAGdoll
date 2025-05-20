import openai
from openai import AsyncOpenAI
import numpy as np
from app.core.config import settings

# Initialize the OpenAI client
# Make sure OPENAI_API_KEY is set in your environment variables or .env file
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_embedding(text: str) -> list[float]:
    """
    Generates an embedding for the given text using the OpenAI API.
    """
    try:
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        # The embedding is a list of floats.
        embedding = response.data[0].embedding
        return embedding
    except openai.APIError as e:
        # Handle API errors (e.g., network issues, invalid key)
        print(f"OpenAI API error: {e}")
        # Depending on the desired error handling strategy,
        # you might want to raise the exception, return None, or an empty list.
        # For now, let's re-raise to make the caller aware.
        raise e
    except Exception as e:
        # Handle other potential errors
        print(f"An unexpected error occurred during embedding generation: {e}")
        raise e

# Example usage (for testing purposes, can be removed or commented out)
# This will need to be updated to be async if kept
# if __name__ == '__main__':
#     import asyncio
#
#     async def main():
#         try:
#             test_embedding = await generate_embedding("Hello, world!")
#             print(f"Generated embedding length: {len(test_embedding)}")
#             # print(f"Generated embedding (first 5 values): {test_embedding[:5]}")
#             print(f"Embedding dimension from settings: {settings.EMBEDDING_DIMENSION}")
#             # The actual dimension for text-embedding-3-small is 1536.
#             # We will update EMBEDDING_DIMENSION in config.py in a later task.
#             # For now, this assertion might fail or be misleading.
#             # assert len(test_embedding) == settings.EMBEDDING_DIMENSION
#             print("Embedding generation test call succeeded.")
#         except Exception as e:
#             print(f"Embedding generation test failed: {e}")
#
#     asyncio.run(main()) 