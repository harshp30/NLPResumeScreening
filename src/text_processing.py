import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import string

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    
    Parameters:
    - pdf_path (str): Path to the PDF file.
    
    Returns:
    - str: Extracted text from the PDF.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        # Iterate through each page of the PDF
        for page in reader.pages:
            # Extract text from the page
            text += page.extract_text()
    return text

def preprocess_text(text):
    """
    Preprocesses text by tokenizing, removing stopwords and punctuation, and lemmatizing.
    
    Parameters:
    - text (str): The text to be processed.
    
    Returns:
    - list: List of preprocessed tokens.
    """
    # Tokenize text into words and convert to lowercase
    tokens = word_tokenize(text.lower())
    
    # Get English stopwords
    stop_words = set(stopwords.words('english'))
    
    # Remove punctuation and stopwords from tokens
    tokens = [word for word in tokens if word not in string.punctuation and word not in stop_words]
    
    # Initialize lemmatizer
    lemmatizer = WordNetLemmatizer()
    
    # Lemmatize each token
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    return tokens

def extract_key_phrases(text):
    """
    Extracts key phrases from text using named entity recognition and POS tagging.
    
    Parameters:
    - text (str): The text from which key phrases are to be extracted.
    
    Returns:
    - list: List of key phrases extracted from the text.
    """
    noun_phrases = []
    # Split text into sentences
    sentences = sent_tokenize(text)
    
    for sentence in sentences:
        # Tokenize sentence into words
        words = word_tokenize(sentence)
        # POS tagging
        tagged = nltk.pos_tag(words)
        # Named entity recognition
        chunk = nltk.ne_chunk(tagged)
        
        current_chunk = []
        for i in chunk:
            # If the chunk is a named entity, add it to the current chunk
            if type(i) == nltk.Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            # If the current chunk is not empty, add it to noun_phrases
            elif current_chunk:
                noun_phrases.append(" ".join(current_chunk))
                current_chunk = []
            # If the token is a noun or adjective, add it to the current chunk
            elif i[1] in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']:
                current_chunk.append(i[0])
        # Add the last chunk if any
        if current_chunk:
            noun_phrases.append(" ".join(current_chunk))
    
    return noun_phrases
