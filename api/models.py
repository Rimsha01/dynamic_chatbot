from sqlalchemy import String, Integer, Column, ForeignKey, Boolean,DateTime
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime
from .database import Base

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer , index = True , primary_key=True , autoincrement=True)
    file_name = Column(String, index = True)
    file_type = Column(String) # csv or txt file
    description = Column(String, nullable = True)
    uploaded_at = Column(DateTime, default = datetime.now)

    chunks = relationship("DocumentChunk", back_populates="source_file" )
    conversations = relationship("Conversation", back_populates="source_file")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, index = True, primary_key=True)
    file_id = Column(Integer, ForeignKey("uploaded_files.id"))
    chunk_text = Column(String)
    embeddings = Column(Vector)
    chunk_index = Column(Integer, autoincrement=True)

    source_file = relationship("UploadedFile", back_populates="chunks")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("uploaded_files.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    title = Column(String, nullable=True)

    source_file = relationship("UploadedFile", back_populates="conversations")
    messages = relationship("ChatMessage", back_populates="conversation")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(String)
    is_user_message = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.now)

    conversation = relationship("Conversation", back_populates="messages")
