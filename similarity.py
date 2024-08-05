import numpy as np
from nltk.util import ngrams
from text_processing import preprocess_text, extract_key_phrases
from gensim.models import KeyedVectors
import gensim.downloader as api

# Load word vectors
# The 'word2vec-google-news-300' model is a pre-trained word embedding model with 300-dimensional vectors
# trained on Google News data. This model provides semantic word embeddings useful for various NLP tasks.
# print("Loading word vectors...")
word_vectors = api.load("word2vec-google-news-300")
# print("Word vectors loaded.")

def improved_semantic_similarity(resume_text, job_description):
    """
    Computes the semantic similarity between the resume text and the job description
    using word embeddings and vector space operations.
    
    Parameters:
    - resume_text (str): The text of the resume.
    - job_description (str): The text of the job description.
    
    Returns:
    - float: A value between -1 and 1 representing the cosine similarity between
      the resume and job description texts.
    """
    def text_to_vec(text):
        """
        Converts text to a vector representation by combining word embeddings
        for the words, key phrases, and bigrams in the text.
        
        Parameters:
        - text (str): The input text to be converted to a vector.
        
        Returns:
        - np.ndarray: A vector representation of the input text.
        """
        # Preprocess the text (e.g., tokenization, lowercasing, removing punctuation)
        words = preprocess_text(text)
        # Extract key phrases (important phrases or terms) from the text
        key_phrases = extract_key_phrases(text)
        # Generate bigrams (two-word sequences) from the tokenized words
        bigrams = [' '.join(bg) for bg in ngrams(words, 2)]
        
        # Combine words, key phrases, and bigrams into a single list of features
        all_features = words + key_phrases + bigrams
        
        # Obtain vector representations for each feature
        vectors = [word_vectors[word] for word in all_features if word in word_vectors.key_to_index]
        
        # If no vectors are found, return a zero vector
        if not vectors:
            return np.zeros(word_vectors.vector_size)
        
        # Compute the mean vector for all features
        return np.mean(vectors, axis=0)
    
    # Convert both the resume text and the job description to vector representations
    vec1 = text_to_vec(resume_text)
    vec2 = text_to_vec(job_description)
    
    # Compute cosine similarity between the two vectors
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
