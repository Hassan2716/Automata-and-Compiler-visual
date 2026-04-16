"""
SQLAlchemy models for storing automata and test cases
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from models.database import Base


class Automata(Base):
    """Model for storing automata"""
    __tablename__ = "automata"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # 'nfa', 'dfa', 'regex', 'cfg'
    data = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TestCase(Base):
    """Model for storing test cases"""
    __tablename__ = "test_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    automata_id = Column(Integer, index=True)
    input_string = Column(String)
    expected_result = Column(String)  # 'accept' or 'reject'
    actual_result = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

