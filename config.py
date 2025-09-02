import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dictionary.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WORDS_API_KEY = os.getenv('WORDS_API_KEY', 'your_api_key_here')  # Replace with actual key
