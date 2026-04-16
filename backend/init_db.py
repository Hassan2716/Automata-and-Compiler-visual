"""
Initialize the database with tables
"""
from models.database import Base, engine

if __name__ == "__main__":
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

