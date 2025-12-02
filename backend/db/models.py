from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tokens = relationship("OAuthToken", back_populates="user")
    memories = relationship("AgentMemory", back_populates="user")

class OAuthToken(Base):
    __tablename__ = "oauth_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service = Column(String, index=True)  # e.g., 'google'
    access_token = Column(Text, nullable=False)  # Encrypted
    refresh_token = Column(Text, nullable=True)  # Encrypted
    token_type = Column(String, default="Bearer")
    expires_at = Column(DateTime(timezone=True))
    scopes = Column(Text)  # JSON or comma-separated list of scopes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="tokens")

class AgentMemory(Base):
    __tablename__ = "agent_memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    memory_type = Column(String)  # 'short_term', 'long_term', 'reflection'
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="memories")

# Knowledge Graph Models (Postgres Adjacency)
class KGNode(Base):
    __tablename__ = "kg_nodes"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)  # e.g., 'Person', 'Email', 'File'
    name = Column(String, index=True)
    properties = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class KGEdge(Base):
    __tablename__ = "kg_edges"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("kg_nodes.id"))
    target_id = Column(Integer, ForeignKey("kg_nodes.id"))
    relation_type = Column(String, index=True)  # e.g., 'SENT_BY', 'MENTIONS'
    properties = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
