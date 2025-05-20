from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from app.core.database import get_db
from app.core.embedding import generate_embedding
from app.services import context_service
from app.db.models import Message as MessageModel

# Pydantic model for request body
class MessageCreate(BaseModel):
    session_id: str
    content: str
    user_id: Optional[str] = None

# Pydantic model for context messages in the response
class ContextMessageResponse(BaseModel):
    role: str
    content: str

# Pydantic model for /response request body
class ModelResponseCreate(BaseModel):
    session_id: str
    content: str

router = APIRouter()

@router.post("/message", tags=["Context Management"], status_code=201)
async def handle_message(message_data: MessageCreate, db: Session = Depends(get_db)):
    try:
        # Step 1: Store the incoming user message
        stored_message = context_service.store_user_message(
            db=db,
            session_id=message_data.session_id,
            content=message_data.content,
            user_id=message_data.user_id
        )

        # Step 2: Retrieve relevant context
        # Generate embedding for the new message
        new_message_embedding = generate_embedding(stored_message.content)
        
        retrieved_context_messages: List[MessageModel] = context_service.get_relevant_context(
            db=db,
            session_id=stored_message.session_id,
            new_message_embedding=new_message_embedding,
            limit=10 # Default limit as per task description for get_relevant_context
        )

        # Filter out the newly added message from the context results
        relevant_context_excluding_new = [
            msg for msg in retrieved_context_messages if msg.id != stored_message.id
        ]
        
        # Step 3: Format the retrieved context for the response
        formatted_context = [
            ContextMessageResponse(role=msg.role, content=msg.content)
            for msg in relevant_context_excluding_new
        ]

        return {
            "status": "success", 
            "message": "User message stored and relevant context retrieved.", 
            "stored_message_id": stored_message.id,
            "session_id": stored_message.session_id,
            "role": stored_message.role,
            "retrieved_context": formatted_context # Added formatted context
        }
    except Exception as e:
        # In a real app, you'd have more specific error handling
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@router.post("/response", tags=["Context Management"], status_code=201)
async def handle_response(response_data: ModelResponseCreate, db: Session = Depends(get_db)):
    try:
        stored_model_response = context_service.store_model_response(
            db=db,
            session_id=response_data.session_id,
            content=response_data.content
        )
        return {
            "status": "success",
            "message": "Model response stored successfully.",
            "stored_response_id": stored_model_response.id,
            "session_id": stored_model_response.session_id,
            "role": stored_model_response.role
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store model response: {str(e)}") 