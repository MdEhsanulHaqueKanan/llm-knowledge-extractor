import json
from flask_sqlalchemy import SQLAlchemy

# We create a database instance that will be linked to our Flask app later
db = SQLAlchemy()

class Analysis(db.Model):
    """
    Represents a single analysis record in our database.
    Each attribute of this class corresponds to a column in the 'analysis' table.
    """
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200), nullable=True) # Title might not always be present
    topics = db.Column(db.Text, nullable=False)     # We will store the list of topics as a JSON string
    sentiment = db.Column(db.String(50), nullable=False)
    keywords = db.Column(db.Text, nullable=False)   # We will store the list of keywords as a JSON string
    confidence = db.Column(db.Float, nullable=True) # Bonus: The confidence score

    def to_dict(self):
        """
        Helper method to convert the Analysis object into a dictionary.
        This is useful for serializing the data into a JSON format for our API responses.
        """
        return {
            'id': self.id,
            'summary': self.summary,
            'title': self.title,
            'topics': json.loads(self.topics), # Convert JSON string back to a Python list
            'sentiment': self.sentiment,
            'keywords': json.loads(self.keywords), # Convert JSON string back to a Python list
            'confidence': self.confidence
        }