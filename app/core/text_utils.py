import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def download_nltk_data():
    """
    Downloads necessary NLTK data packages if they are not already present.
    This makes the application self-contained and prevents errors on first run.
    """
    try:
        # Check if the packages are available, if not, download them.
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        # Using quiet=True to prevent excessive console output
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)

# We call this function once when the module is first imported.
# This ensures the data is ready before any functions are called.
download_nltk_data()

def extract_keywords(text: str, num_keywords: int = 3) -> list[str]:
    """
    Extracts the most frequent nouns from the text, as per the assignment requirements.
    """
    # Get the standard list of English "stopwords" (e.g., 'the', 'a', 'is').
    stop_words = set(stopwords.words('english'))
    
    # Normalize text: convert to lowercase and remove all punctuation.
    text = re.sub(r'[^\w\s]', '', text.lower())
    
    # Tokenize the text into a list of words.
    words = word_tokenize(text)
    
    # Use NLTK's Part-of-Speech (POS) tagger to identify the type of each word.
    pos_tags = nltk.pos_tag(words)
    
    # Filter for words that are nouns ('NN'), not stopwords, and are alphabetic.
    nouns = [
        word for word, pos in pos_tags
        if pos.startswith('NN') and word.isalpha() and word not in stop_words
    ]
    
    # Count the frequency of each noun and return the 3 most common ones.
    return [word for word, _ in Counter(nouns).most_common(num_keywords)]