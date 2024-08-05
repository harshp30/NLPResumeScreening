import os
import csv
import spacy
from text_processing import preprocess_text

# Load spaCy model for named entity recognition
# The 'en_core_web_sm' model is a small English model provided by spaCy, which includes tokenization,
# part-of-speech tagging, named entity recognition (NER), and other linguistic features.
nlp = spacy.load("en_core_web_sm")

def load_skills_database(category):
    """
    Loads the skills database for a given job category from a text file.
    
    Parameters:
    - category (str): The job category for which to load the skills database.
    
    Returns:
    - set: A set of skills relevant to the given category.
    """
    # Construct the file path based on the job category
    skills_file = f"/Users/harsh/Desktop/NLPResumeScreening/skill_database/{category.lower().replace(' ', '_')}.txt"
    
    # Check if the file exists
    if os.path.exists(skills_file):
        # Open and read the content of the file
        with open(skills_file, 'r') as file:
            content = file.read()
            # Use csv.reader to read the content as a CSV format
            reader = csv.reader([content], skipinitialspace=True)
            # Extract skills from the CSV content, strip extra spaces and convert to lowercase
            skills = set(skill.strip().lower() for skill in next(reader) if skill.strip())
        return skills
    else:
        # Print a warning message if the file does not exist
        print(f"Warning: Skills database file for {category} not found.")
        return set()

def extract_skills(text, category_skills):
    """
    Extracts skills from a given text based on named entity recognition and token matching.
    
    Parameters:
    - text (str): The text from which to extract skills.
    - category_skills (set): A set of predefined skills for the job category.
    
    Returns:
    - set: A set of extracted skills from the text.
    """
    # Process the text using spaCy's NLP pipeline
    doc = nlp(text)
    skills = set()
    
    # Extract named entities from the text
    for ent in doc.ents:
        # Check if the entity label is either an organization or product, which might indicate a skill
        if ent.label_ in ["ORG", "PRODUCT"]:
            skills.add(ent.text.lower())
    
    # Preprocess the text to obtain a set of tokens (words)
    tokens = set(preprocess_text(text))
    # Update the skill set with tokens that match predefined category skills
    skills.update(tokens.intersection(category_skills))
    
    return skills
