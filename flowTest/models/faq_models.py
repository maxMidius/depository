from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

# Create Base and export it
Base = declarative_base()
__all__ = ['Base', 'QuestionGroup', 'Question', 'Tag', 'Answer']

# Association table for Question-Tag many-to-many relationship
question_tags = Table('question_tags', Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class QuestionGroup(Base):
    __tablename__ = 'question_groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    questions = relationship("Question", back_populates="group")

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('question_groups.id'))
    question_number = Column(String(10), nullable=False, unique=True)
    text = Column(Text, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    group = relationship("QuestionGroup", back_populates="questions")
    tags = relationship("Tag", secondary=question_tags, back_populates="questions")
    answer = relationship("Answer", back_populates="question", uselist=False)

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    questions = relationship("Question", secondary=question_tags, back_populates="tags")

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    html_content = Column(Text, nullable=False)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    question = relationship("Question", back_populates="answer")