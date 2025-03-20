# resume_processor/processor.py
import re

def extract_skills(resume_text, known_skills=None):
    """
    Extracts candidate skills from the resume text.
    
    :param resume_text: The text content of the resume.
    :param known_skills: Optional set/list of known skills to match against.
                         If not provided, a default set of skills is used.
    :return: A set of skills found in the resume.
    """
    # Define a default set of skills if not provided.
    if known_skills is None:
        known_skills = {
            "python", "django", "rest", "aws", "sql", "javascript",
            "html", "css", "java", "c++", "node.js", "flask", "docker",
            "kubernetes", "git"
        }
    
    # Convert resume text to lower case for case-insensitive matching.
    text = resume_text.lower()
    
    # Use regex to extract words (this can be refined as needed).
    words = re.findall(r'\b\w+\b', text)
    
    # Intersect with the known skills set.
    extracted_skills = set(words) & set(known_skills)
    
    return extracted_skills

def evaluate_candidate(candidate_skills, required_skills, threshold=3):
    """
    Compares candidate skills with job's required skills.
    
    :param candidate_skills: A set of skills extracted from the candidate's resume.
    :param required_skills: A list or set of skills required by the job.
    :param threshold: Minimum number of required skills that must match.
    :return: True if candidate meets or exceeds the threshold, False otherwise.
    """
    # Convert required_skills to lower case to ensure case-insensitive matching.
    required_set = {skill.lower() for skill in required_skills}
    matching_skills = candidate_skills & required_set
    return len(matching_skills) >= threshold, matching_skills
