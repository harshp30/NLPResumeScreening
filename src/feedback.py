import requests
import json
from resume_screening import extract_text_from_pdf, calculate_match_percentage

class NvidiaNeMoClient:
    def __init__(self, base_url, api_key):
        """
        Initializes the NvidiaNeMoClient with the base URL and API key.

        Args:
        base_url (str): The base URL for the Nvidia NeMo API.
        api_key (str): The API key for authentication.
        """
        self.base_url = base_url
        self.api_key = api_key
    
    def chat_completions_create(self, model, messages, temperature=0.2, top_p=0.7, max_tokens=1024, stream=False):
        """
        Sends a request to the Nvidia NeMo API to create chat completions.

        Args:
        model (str): The model to use for generating completions.
        messages (list): List of message dictionaries for the chat prompt.
        temperature (float): Sampling temperature for the model.
        top_p (float): Nucleus sampling probability.
        max_tokens (int): Maximum number of tokens to generate.
        stream (bool): If True, returns a streaming response.

        Returns:
        dict or requests.Response: The response from the API if not streaming, or the raw response if streaming.
        """
        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "stream": stream
        }
        response = requests.post(url, headers=headers, json=payload, stream=stream)
        if stream:
            return response
        else:
            return response.json()

def generate_feedback(prompt):
    """
    Generates feedback using Nvidia NeMo's chat completions.

    Args:
    prompt (str): The prompt to send to the model for feedback generation.

    Returns:
    str: The feedback content from the model.
    """
    client = NvidiaNeMoClient(
        base_url="https://integrate.api.nvidia.com",
        api_key=""
    )
    
    completion = client.chat_completions_create(
        model="meta/llama-3.1-8b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=0.7,
        max_tokens=500,
        stream=False  # Set to True if you want streaming responses
    )
    
    return completion['choices'][0]['message']['content']

def get_feedback_on_resume(resume_path, job_description_path, job_category):
    """
    Retrieves feedback on a resume based on a job description.

    Args:
    resume_path (str): The file path to the resume PDF.
    job_description_path (str): The file path to the job description text file.
    job_category (str): The category of the job.

    Returns:
    str: The feedback generated for the resume.
    """
    # Extract text from the resume PDF
    resume_text = extract_text_from_pdf(resume_path)
    
    # Read the job description from the file
    with open(job_description_path, 'r') as file:
        job_description = file.read()

    # Calculate the match percentage between the resume and the job description
    match_percentage = calculate_match_percentage(resume_text, job_description, job_category)
    
    # Prepare the prompt for feedback generation
    feedback_prompt = f"""
    Resume Text: {resume_text}
    Job Description: {job_description}
    The resume match percentage is {match_percentage:.2f}%. 
    Given the job description, provide feedback on the RESUME.
    """
    
    # Generate and return feedback using Nvidia NeMo
    feedback = generate_feedback(feedback_prompt)
    return feedback
