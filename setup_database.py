#!/usr/bin/env python3
"""
Setup script to create the products table in the database.
"""
import os
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Create the database and products table."""
    
    # Database connection details
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Empty password for root
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    try:
        # Connect to MySQL server
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS cartdb")
            print("✅ Database 'cartdb' created/verified")
            
            # Use the database
            cursor.execute("USE cartdb")
            
            # Read and execute the schema file
            schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
            
            if os.path.exists(schema_path):
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema_content = f.read()
                
                # Split by semicolons and execute each statement
                statements = schema_content.split(';')
                
                for statement in statements:
                    statement = statement.strip()
                    if statement:  # Skip empty statements
                        try:
                            cursor.execute(statement)
                            print(f"✅ Executed: {statement[:50]}...")
                        except Exception as e:
                            if "already exists" not in str(e).lower():
                                print(f"⚠️  Warning executing statement: {e}")
                
                connection.commit()
                print("✅ Database schema setup completed successfully")
                
            else:
                print(f"❌ Schema file not found: {schema_path}")
                
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False
    
    finally:
        if 'connection' in locals():
            connection.close()
    
    return True

if __name__ == "__main__":
    print("🚀 Setting up database...")
    success = setup_database()
    
    if success:
        print("✅ Database setup completed successfully!")
    else:
        print("❌ Database setup failed!")