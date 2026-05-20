from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship # Object-Relational Mapping
# Raw SQL (Without ORM)Create TableCREATE TABLE users (...)
# With ORM (SQLAlchemy) Base.metadata.create_all(engine)
from database import Base

class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # One user can have many posts
    posts = relationship("DBPost", back_populates="owner")


class DBPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    
    # ForeignKey links a post row straight to a User ID row
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Connects back to the User model
    owner = relationship("DBUser", back_populates="posts")
