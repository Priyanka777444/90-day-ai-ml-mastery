"""
Authentication Module
User registration, login, and session management
"""
import sqlite3
import bcrypt
from datetime import datetime

DB_NAME = 'mylife.db'

def init_auth_db():
    """Initialize users table"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash a password for storing"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def register_user(username, email, password, full_name):
    """Register a new user"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Hash password
        password_hash = hash_password(password)
        
        # Insert user
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, full_name, str(datetime.now())))
        
        user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return True, user_id, "Registration successful!"
    
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            return False, None, "Username already exists!"
        elif 'email' in str(e):
            return False, None, "Email already exists!"
        else:
            return False, None, "Registration failed!"
    except Exception as e:
        return False, None, f"Error: {str(e)}"

def login_user(username, password):
    """Authenticate user login"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Get user by username
        cursor.execute('SELECT id, password_hash, full_name FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            user_id, password_hash, full_name = user
            
            # Verify password
            if verify_password(password, password_hash):
                return True, user_id, full_name, "Login successful!"
            else:
                return False, None, None, "Incorrect password!"
        else:
            return False, None, None, "Username not found!"
    
    except Exception as e:
        return False, None, None, f"Error: {str(e)}"

def get_user_info(user_id):
    """Get user information"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT username, email, full_name FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    conn.close()
    return user