# models.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    short_id = Column(String, unique=True)
    project_type = Column(String)
    brief = Column(String)
    tags = Column(JSON)
    deliverables = relationship("Deliverable", back_populates="project", cascade="all, delete-orphan")

class Deliverable(Base):
    __tablename__ = 'deliverables'

    id = Column(Integer, primary_key=True)
    short_id = Column(String, unique=True)
    brief = Column(String)
    tags = Column(JSON)
    team = Column(JSON)
    effort = Column(Integer)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="deliverables")
    tasks = relationship("Task", back_populates="deliverable", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    short_id = Column(String, unique=True)
    brief = Column(String)
    team = Column(JSON)
    effort = Column(Integer)
    deliverable_id = Column(Integer, ForeignKey('deliverables.id'))
    deliverable = relationship("Deliverable", back_populates="tasks")

# Initialize database
engine = create_engine('sqlite:///project_management.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
