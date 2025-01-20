from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.faq_models import Base, QuestionGroup, Question, Tag, Answer
import datetime

# Create database and tables
engine = create_engine('sqlite:///faq.db')
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Create test data
def init_test_data():
    # Create Groups
    group1 = QuestionGroup(name="General")
    group2 = QuestionGroup(name="Technical")
    session.add_all([group1, group2])
    session.commit()

    # Create Tags
    tag1 = Tag(name="setup")
    tag2 = Tag(name="basics")
    session.add_all([tag1, tag2])
    session.commit()

    # Create Questions with Answers
    q1 = Question(
        group=group1,
        question_number="A:001",
        text="What is Surveillance Studio?",
        tags=[tag1, tag2]
    )
    
    a1 = Answer(
        question=q1,
        html_content="Surveillance Studio is a tool for building monitoring applications."
    )
    
    session.add_all([q1, a1])
    session.commit()

if __name__ == "__main__":
    init_test_data()