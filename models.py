from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True, nullable=False)
    definition = db.Column(db.Text, nullable=False)
    ipa = db.Column(db.String(100))
    synonyms = db.Column(db.Text)  # JSON string
    antonyms = db.Column(db.Text)  # JSON string
    examples = db.Column(db.Text)  # JSON string
