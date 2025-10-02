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
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    item_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    category = Column(String(100), nullable=False)
    stock_status = Column(Enum('in_stock', 'out_of_stock'), default='in_stock')
    stock_quantity = Column(Integer, default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

def get_db_session():
    return SessionLocal()

# Create tables if needed
# Comment out table creation on import to avoid startup issues
# Base.metadata.create_all(bind=engine)