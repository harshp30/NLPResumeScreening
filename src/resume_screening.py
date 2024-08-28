import os
from text_processing import extract_text_from_pdf
from similarity import improved_semantic_similarity
from skills_extraction import load_skills_database, extract_skills
from settings import DB_SKILL_THRESHOLD, JOB_SKILL_THRESHOLD, SEMANTIC_WEIGHT, SKILLS_WEIGHT

def calculate_match_percentage(resume_text, job_description, job_category):
    """
    Calculates the match percentage between a resume and a job description based on semantic similarity
    and skills extracted from the text.
    
    Parameters:
    - resume_text (str): The text content of the resume.
    - job_description (str): The text content of the job description.
    - job_category (str): The job category used to load the relevant skills database.
    
    Returns:
    - float: The match percentage as a float value.
    """
    # Load the skills database for the given job category
    category_skills = load_skills_database(job_category)
    
    # Calculate semantic similarity between the resume and the job description
    semantic_score = improved_semantic_similarity(resume_text, job_description)
    
    # Extract skills from the resume and job description
    resume_skills = extract_skills(resume_text, category_skills)
    job_skills = extract_skills(job_description, category_skills)
    
    # Find the intersection of skills between the resume and job description
    matching_skills = resume_skills.intersection(job_skills)
    
    # Calculate the number of skill matches in the resume versus the skills database
    db_skill_matches = len(resume_skills.intersection(category_skills))
    # Calculate the number of skill matches between the resume and the job description
    job_skill_matches = len(matching_skills)
    
    # Normalize the skill scores based on predefined thresholds
    db_score = min(db_skill_matches / DB_SKILL_THRESHOLD, 1.0)
    job_score = min(job_skill_matches / JOB_SKILL_THRESHOLD, 1.0)
    
    # Calculate the average skill score
    skills_score = (db_score + job_score) / 2
    
    # Calculate the total score by combining semantic and skills scores with their respective weights
    total_score = (
        semantic_score * SEMANTIC_WEIGHT +
        skills_score * SKILLS_WEIGHT
    )
    
    # Return the total score as a percentage
    return total_score * 100

def screen_resume(resume_path, job_category):
    """
    Screens a resume against a job description to calculate the match percentage.
    
    Parameters:
    - resume_path (str): The file path to the resume PDF.
    - job_category (str): The job category used to load the relevant skills database and job description.
    
    Returns:
    - float: The match percentage as a float value.
    """
    # Extract text from the resume PDF
    resume_text = extract_text_from_pdf(resume_path)
    
    # Construct the file path for the job description based on the job category
    job_description_path = f"/Users/harsh/Desktop/NLPResumeScreening/job_description/{job_category}.txt"
    
    # Read the job description text from the file
    with open(job_description_path, 'r') as file:
        job_description = file.read()
    
    # Calculate the match percentage
    match_percentage = calculate_match_percentage(resume_text, job_description, job_category)
    
    return match_percentage
