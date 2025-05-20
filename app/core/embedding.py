import numpy as np
from app.core.config import settings

def generate_embedding(text: str) -> np.ndarray:
    """
    Placeholder function to generate a random embedding.
    In a real application, this would call an actual embedding model API.
    """
    # Ensure the random seed is consistent for potential repeatable tests if needed,
    # though for a pure placeholder, it's not strictly necessary.
    # np.random.seed(42) # Optional: for deterministic random numbers
    return np.random.rand(settings.EMBEDDING_DIMENSION).astype(np.float32)

# Example usage (for testing purposes, can be removed or commented out)
if __name__ == '__main__':
    test_embedding = generate_embedding("Hello, world!")
    print(f"Generated embedding shape: {test_embedding.shape}")
    print(f"Generated embedding dtype: {test_embedding.dtype}")
    print(f"Embedding dimension from settings: {settings.EMBEDDING_DIMENSION}")
    assert test_embedding.shape == (settings.EMBEDDING_DIMENSION,)
    print("Embedding generation test passed.") 