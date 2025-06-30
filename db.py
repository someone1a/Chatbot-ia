from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from datetime import datetime

if not os.path.exists("data"):
    os.makedirs("data")

engine = create_engine("sqlite:///data/chatbot.db", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    chats = relationship("Chat", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, default="Nuevo chat")
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="conversations")
    chats = relationship("Chat", back_populates="conversation")

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    user_msg = Column(Text)
    ai_response = Column(Text)
    user = relationship("User", back_populates="chats")
    conversation = relationship("Conversation", back_populates="chats")

Base.metadata.create_all(engine)
