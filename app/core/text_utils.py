import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def download_nltk_data():
    """
    Downloads necessary NLTK data packages if not already present.
    This makes the application robust for local development setups.
    """
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)

# Ensure required NLTK data is available upon module import.
download_nltk_data()

def extract_keywords(text: str, num_keywords: int = 3) -> list[str]:
    """
    Extracts the most frequent nouns from a block of text after normalizing
    and removing stopwords.
    """
    stop_words = set(stopwords.words('english'))
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    nouns = [
        word for word, pos in pos_tags
        if pos.startswith('NN') and word.isalpha() and word not in stop_words
    ]
    return [word for word, _ in Counter(nouns).most_common(num_keywords)]