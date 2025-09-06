import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Analysis(db.Model):
    """Represents a single analysis record in the database."""
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    topics = db.Column(db.Text, nullable=False)     # Stored as a JSON string
    sentiment = db.Column(db.String(50), nullable=False)
    keywords = db.Column(db.Text, nullable=False)   # Stored as a JSON string
    confidence = db.Column(db.Float, nullable=True)

    def to_dict(self):
        """Serializes the Analysis object into a dictionary."""
        return {
            'id': self.id,
            'summary': self.summary,
            'title': self.title,
            'topics': json.loads(self.topics),
            'sentiment': self.sentiment,
            'keywords': json.loads(self.keywords),
            'confidence': self.confidence
        }