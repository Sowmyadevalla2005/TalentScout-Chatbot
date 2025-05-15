import re
from typing import List, Dict, Any
import hashlib
import json

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Remove any non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    # Check if we have 10-15 digits (international numbers)
    return 10 <= len(digits) <= 15

def validate_tech_stack(tech_stack: str) -> List[str]:
    """Validate and clean tech stack input."""
    # Split by commas and clean each technology
    techs = [tech.strip().lower() for tech in tech_stack.split(',')]
    # Remove empty strings and duplicates
    return list(set(tech for tech in techs if tech))

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    # Remove any potential HTML/script tags
    text = re.sub(r'<[^>]*>', '', text)
    # Remove any special characters that could be used for injection
    text = re.sub(r'[;\\\\/]', '', text)
    return text.strip()

def hash_sensitive_data(data: str) -> str:
    """Hash sensitive data for storage."""
    return hashlib.sha256(data.encode()).hexdigest()

def format_candidate_summary(info: Dict[str, Any]) -> str:
    """Format candidate information for display."""
    summary = []
    
    if info.get("name"):
        summary.append(f"**Name:** {info['name']}")
    if info.get("email"):
        # Show only first 3 chars of email local part
        email_parts = info['email'].split('@')
        masked_email = f"{email_parts[0][:3]}...@{email_parts[1]}"
        summary.append(f"**Email:** {masked_email}")
    if info.get("phone"):
        # Show only last 4 digits
        digits = ''.join(filter(str.isdigit, info['phone']))
        masked_phone = f"****-****-{digits[-4:]}"
        summary.append(f"**Phone:** {masked_phone}")
    if info.get("experience"):
        summary.append(f"**Experience:** {info['experience']}")
    if info.get("position"):
        summary.append(f"**Position:** {info['position']}")
    if info.get("location"):
        summary.append(f"**Location:** {info['location']}")
    if info.get("tech_stack"):
        summary.append("**Tech Stack:**")
        for tech in info['tech_stack']:
            summary.append(f"- {tech}")
    
    return "\n".join(summary)

def save_candidate_data(info: Dict[str, Any], filename: str = "candidates.json") -> None:
    """Save candidate data securely."""
    # Hash sensitive information
    secure_info = info.copy()
    if "email" in secure_info:
        secure_info["email"] = hash_sensitive_data(secure_info["email"])
    if "phone" in secure_info:
        secure_info["phone"] = hash_sensitive_data(secure_info["phone"])
    
    try:
        # Load existing data
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        # Add new candidate
        data.append(secure_info)
        
        # Save updated data
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
    except Exception as e:
        print(f"Error saving candidate data: {str(e)}")

def analyze_sentiment(text: str) -> str:
    """Basic sentiment analysis of candidate responses."""
    # Define sentiment keywords
    positive_words = {'great', 'good', 'excellent', 'amazing', 'love', 'enjoy', 'passionate'}
    negative_words = {'bad', 'difficult', 'hard', 'problem', 'issue', 'challenging'}
    
    # Convert to lowercase and split into words
    words = set(text.lower().split())
    
    # Count sentiment matches
    positive_count = len(words.intersection(positive_words))
    negative_count = len(words.intersection(negative_words))
    
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    return "neutral"

def get_experience_level(years: str) -> str:
    """Determine experience level from years of experience."""
    try:
        years_num = int(''.join(filter(str.isdigit, years)))
        if years_num < 2:
            return "junior"
        elif years_num < 5:
            return "mid-level"
        else:
            return "senior"
    except:
        return "mid-level"  # Default if parsing fails