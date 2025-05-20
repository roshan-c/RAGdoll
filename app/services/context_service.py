import numpy as np
from sqlalchemy.orm import Session
from app.db.models import Message
from app.core.embedding import generate_embedding

def store_user_message(db: Session, session_id: str, content: str, user_id: str = None) -> Message:
    """
    Stores a user message in the database.

    Args:
        db: The database session.
        session_id: The ID of the current session.
        content: The content of the user's message.
        user_id: The ID of the user (optional).

    Returns:
        The created Message object.
    """
    embedding = generate_embedding(content)
    
    db_message = Message(
        session_id=session_id,
        user_id=user_id,
        role="user",
        content=content,
        embedding=embedding
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)  # To get the ID and other server-generated defaults like timestamp
    return db_message

def store_model_response(db: Session, session_id: str, content: str) -> Message:
    """
    Stores a model response in the database.

    Args:
        db: The database session.
        session_id: The ID of the current session.
        content: The content of the model's response.

    Returns:
        The created Message object.
    """
    embedding = generate_embedding(content)
    
    db_message = Message(
        session_id=session_id,
        role="model",
        content=content,
        embedding=embedding
        # user_id is not applicable for model responses
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_relevant_context(db: Session, session_id: str, new_message_embedding: np.ndarray, limit: int = 10) -> list[Message]:
    """
    Retrieves relevant context messages from the database based on embedding similarity.

    Args:
        db: The database session.
        session_id: The ID of the current session to filter messages.
        new_message_embedding: The embedding of the new message to compare against.
        limit: The maximum number of relevant messages to return.

    Returns:
        A list of Message objects ordered by relevance (cosine distance).
    """
    relevant_messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.embedding.cosine_distance(new_message_embedding))
        .limit(limit)
        .all()
    )
    return relevant_messages 