import os
from sqlalchemy import create_engine
from models.faq_models import Base

# Create database in current directory
db_path = os.path.join(os.path.dirname(__file__), 'faq.db')
engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)