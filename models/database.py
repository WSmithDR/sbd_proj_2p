"""Database connection and operations."""
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

class DatabaseConnection:
    """Handles database connection and operations."""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Establish database connection using environment variables."""
        try:
            load_dotenv()
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT', '3306')),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("✓ Connected to database")
        except Error as e:
            print(f"✗ Error connecting to database: {e}")
            raise
    
    def execute_query(self, query, params=None, fetch=True):
        """Execute a SQL query and return results."""
        try:
            self.cursor.execute(query, params or ())
            if fetch:
                return self.cursor.fetchall()
            self.connection.commit()
            return True
        except Error as e:
            print(f"✗ Error executing query: {e}")
            return None
    
    def close(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("✓ Database connection closed")
