from typing import Dict, List, Any
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import os

class TalentScoutChatbot:
    """
    TalentScout Hiring Assistant chatbot that uses Hugging Face's transformers.
    """
    
    def __init__(self):
        """Initialize the chatbot with a free model from Hugging Face."""
        # Using a very small but effective model for chat
        model_name = "distilgpt2"
        
        print("Loading model and tokenizer... This might take a few minutes...")
        try:
            # Create cache directory if it doesn't exist
            cache_dir = os.path.join(os.getcwd(), "model_cache")
            os.makedirs(cache_dir, exist_ok=True)
            
            # Determine device
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using device: {self.device}")
            
            # Initialize tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=cache_dir
            )
            
            # Initialize model with device placement
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                cache_dir=cache_dir,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float32
            ).to(self.device)
            
            # Initialize conversation state
            self.conversation_started = False
            self.current_step = "name"
            self.tech_questions_cache = {}
            self.current_question_index = 0
            
            print("Model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise

    def get_initial_greeting(self) -> str:
        """Return the initial greeting message."""
        return """Hello! I'm the TalentScout Hiring Assistant. I'll be helping with your initial screening process. 
Could you please tell me your full name to get started?"""

    def get_next_question(self, current_step: str) -> str:
        """Get the next question based on the current step."""
        questions = {
            "name": "Could you please tell me your full name?",
            "email": "What's your email address?",
            "phone": "What's your phone number?",
            "experience": "How many years of experience do you have in your field?",
            "position": "What position(s) are you interested in?",
            "location": "What's your current location?",
            "tech_stack": "Please list your tech stack (programming languages, frameworks, databases, tools), separated by commas:"
        }
        return questions.get(current_step, "")

    def validate_response(self, step: str, response: str) -> bool:
        """Validate user response based on the current step."""
        if not response:
            return False
            
        if step == "email":
            return "@" in response and "." in response
        elif step == "phone":
            # Basic phone number validation
            digits = ''.join(filter(str.isdigit, response))
            return len(digits) >= 10
        elif step == "experience":
            # Check if response contains a number
            return any(char.isdigit() for char in response)
        return True

    def get_response(self, messages: List[Dict[str, str]], candidate_info: Dict[str, Any]) -> str:
        """Get a response from the chatbot based on the conversation history and candidate information."""
        # Start conversation if not started
        if not self.conversation_started:
            self.conversation_started = True
            return self.get_initial_greeting()

        # Get the last user message
        last_message = messages[-1]["content"] if messages else ""

        # Check for exit command
        if self.should_end_conversation(last_message):
            return "Thank you for your time. The conversation has ended. Have a great day!"

        # Handle tech questions phase
        if self.current_step == "tech_questions":
            return self.handle_tech_questions(candidate_info, last_message)

        # Validate current step response
        if not self.validate_response(self.current_step, last_message):
            return f"I'm sorry, but I need a valid {self.current_step}. {self.get_next_question(self.current_step)}"

        # Update candidate info
        candidate_info = self.update_candidate_info(self.current_step, last_message, candidate_info)

        # Move to next step
        self.current_step = self.determine_next_step(self.current_step)

        # If moving to tech questions, initialize them
        if self.current_step == "tech_questions":
            return self.handle_tech_questions(candidate_info, "")

        # Return next question
        return f"Thank you. {self.get_next_question(self.current_step)}"

    def handle_tech_questions(self, candidate_info: Dict[str, Any], user_response: str) -> str:
        """Handle the technical questions phase of the conversation."""
        if not self.tech_questions_cache:
            # Generate questions if not cached
            self.tech_questions_cache = self.generate_tech_questions(
                candidate_info["tech_stack"],
                candidate_info["experience"]
            )
            self.current_question_index = 0
            return (f"Great! Based on your tech stack ({', '.join(candidate_info['tech_stack'])}), "
                    f"I'd like to ask you a few technical questions.\n\n"
                    f"Question 1: {self.tech_questions_cache[0]}")

        # Process answer and move to next question
        self.current_question_index += 1

        # If we've asked all questions, end the technical portion
        if self.current_question_index >= len(self.tech_questions_cache):
            candidate_info["tech_questions_asked"] = True
            return ("Thank you for answering all the technical questions. "
                    "Your responses have been recorded. The TalentScout team will review your "
                    "application and get back to you soon. Is there anything else you'd like to mention?")

        # Return the next question
        return (f"Thank you for your answer.\n\n"
                f"Question {self.current_question_index + 1}: "
                f"{self.tech_questions_cache[self.current_question_index]}")

    def generate_tech_questions(self, tech_stack: List[str], experience_level: str) -> List[str]:
        """Generate technical questions based on the candidate's tech stack and experience."""
        # Use predefined questions for better reliability
        questions = []
        for tech in tech_stack[:3]:  # Use up to 3 technologies
            questions.extend([
                f"What are the main features and benefits of {tech}?",
                f"Can you describe a challenging problem you solved using {tech}?",
                f"What are some best practices when working with {tech}?"
            ])
        
        # Add some general questions
        questions.extend([
            "How do you approach learning new technologies?",
            "How do you ensure code quality in your projects?"
        ])
        
        return questions[:5]  # Return only 5 questions

    def should_end_conversation(self, user_input: str) -> bool:
        """Check if the conversation should end based on user input."""
        exit_keywords = ["exit", "quit", "stop", "bye", "goodbye"]
        return any(keyword in user_input.lower() for keyword in exit_keywords)

    def update_candidate_info(self, current_step: str, user_input: str, candidate_info: Dict[str, Any]) -> Dict[str, Any]:
        """Update candidate information based on the current step and user input."""
        updated_info = candidate_info.copy()
        
        # Initialize fields if they don't exist
        if "tech_stack" not in updated_info:
            updated_info["tech_stack"] = []
        if "tech_questions_asked" not in updated_info:
            updated_info["tech_questions_asked"] = False
            
        # Update the current step's information
        if current_step == "name":
            updated_info["name"] = user_input
        elif current_step == "email":
            updated_info["email"] = user_input
        elif current_step == "phone":
            updated_info["phone"] = user_input
        elif current_step == "experience":
            updated_info["experience"] = user_input
        elif current_step == "position":
            updated_info["position"] = user_input
        elif current_step == "location":
            updated_info["location"] = user_input
        elif current_step == "tech_stack":
            updated_info["tech_stack"] = [tech.strip() for tech in user_input.split(',')]
        
        return updated_info

    def determine_next_step(self, current_step: str) -> str:
        """Determine the next step in the conversation flow."""
        step_sequence = ["name", "email", "phone", "experience", "position", "location", "tech_stack", "tech_questions"]
        try:
            current_index = step_sequence.index(current_step)
            return step_sequence[current_index + 1] if current_index < len(step_sequence) - 1 else current_step
        except ValueError:
            return "name"