# resume_processor/processor.py
import re

class SkillEvaluator:
    def __init__(self, known_skills=None, threshold=3):
        # Use default skills if none provided.
        if known_skills is None:
            self.known_skills = {
                "python", "django", "rest", "aws", "sql", "javascript",
                "html", "css", "java", "c++", "node.js", "flask", "docker",
                "kubernetes", "git"
            }
        else:
            self.known_skills = {skill.lower() for skill in known_skills}
        self.threshold = threshold

    def extract_skills(self, resume_text):
        """Extract skills from resume text (case-insensitive)."""
        text = resume_text.lower()
        words = re.findall(r'\b\w+\b', text)
        return set(words) & self.known_skills

    def evaluate_candidate(self, candidate_skills, required_skills):
        """
        Compare candidate skills with required skills.
        Returns (True, matching_skills) if candidate meets the threshold; otherwise (False, matching_skills).
        """
        required_set = {skill.lower() for skill in required_skills}
        matching_skills = candidate_skills & required_set
        return len(matching_skills) >= self.threshold, matching_skills
