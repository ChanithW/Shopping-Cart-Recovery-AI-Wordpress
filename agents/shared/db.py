from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Enum, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:pass@localhost/woocommerce_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class CartLog(Base):
    __tablename__ = "wp_cart_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255))
    email = Column(String(255))
    items = Column(Text)  # JSON
    timestamp = Column(DateTime)
    abandoned = Column(Integer)
    email_sent = Column(Integer, default=0)
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)
    converted = Column(Integer, default=0)

class Product(Base):
    __tablename__ = 'wp_posts'
    __table_args__ = {'extend_existing': True}

    # Map WordPress post fields to our Product model
    id = Column('ID', Integer, primary_key=True)
    item_name = Column('post_title', String(255))
    # We'll need to get description and price from postmeta, not direct columns
    # These will be populated in the recommendation engine

def get_db_session():
    return SessionLocal()

# Create tables if needed
# Comment out table creation on import to avoid startup issues
# Base.metadata.create_all(bind=engine)