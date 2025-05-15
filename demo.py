"""
TalentScout Hiring Assistant Demo Script

This script demonstrates how the chatbot would interact with a candidate
without requiring the full Streamlit app to be running.
"""

import os
import sys
from dotenv import load_dotenv
from chatbot import TalentScoutChatbot
from utils import parse_tech_stack, format_candidate_summary
import streamlit as st
import time
import random
from utils import sanitize_input

# Load environment variables
load_dotenv()

def run_demo():
    """
    Run a demonstration of the TalentScoutChatbot with examples of problematic inputs
    and how the system handles them.
    """
    st.title("TalentScout Hiring Assistant - Demo")
    
    st.markdown("""
    ## Demo Overview
    This demonstration showcases how the TalentScout Hiring Assistant handles various challenging scenarios:
    
    1. **Basic Information Collection**: Standard workflow for gathering candidate information
    2. **Repetitive Text Handling**: Detecting and managing repetitive patterns
    3. **Assignment Text Pasting**: Extracting useful information when a user pastes assignment details
    4. **Simple Acknowledgments**: Providing guidance when users give simple responses like "ok"
    5. **Mixed Input Handling**: Processing messages containing both instructions and information
    """)
    
    demo_options = [
        "Basic Interview Flow",
        "Repetitive Text Handling",
        "Assignment Text Pasting",
        "Simple Acknowledgment Handling",
        "Mixed Input Detection"
    ]
    
    selected_demo = st.selectbox("Select a demo scenario:", demo_options)
    
    if st.button("Start Demo"):
        if selected_demo == "Basic Interview Flow":
            run_basic_interview_demo()
        elif selected_demo == "Repetitive Text Handling":
            run_repetitive_text_demo()
        elif selected_demo == "Assignment Text Pasting":
            run_assignment_text_demo()
        elif selected_demo == "Simple Acknowledgment Handling":
            run_acknowledgment_demo()
        elif selected_demo == "Mixed Input Detection":
            run_mixed_input_demo()

def simulate_typing(message, delay=0.05):
    """Simulate typing animation for chatbot messages."""
    container = st.empty()
    full_message = ""
    for char in message:
        full_message += char
        container.markdown(full_message + "▌")
        time.sleep(delay)
    container.markdown(full_message)
    return container

def run_basic_interview_demo():
    """Run a basic interview flow demonstration."""
    chatbot = TalentScoutChatbot()
    
    st.subheader("Demo: Basic Interview Flow")
    st.info("This demo shows the standard interview flow for collecting candidate information.")
    
    # Initial greeting
    simulate_typing(chatbot.get_initial_greeting())
    
    # Name step
    simulate_typing("John Smith")
    simulate_typing("Thanks, John! Could you please share your email address for further communication?")
    
    # Email step
    simulate_typing("john.smith@example.com")
    simulate_typing("Great! Could you please provide your contact number where we can reach you?")
    
    # Phone step
    simulate_typing("555-123-4567")
    simulate_typing("Thank you. Now I'd like to know about your professional experience. Please describe your experience in detail, including years of experience, types of projects, technologies used, and role responsibilities.")
    
    # Experience step
    simulate_typing("I have 5 years of experience working as a software developer. I've primarily worked on web applications using JavaScript, React, and Node.js. I've also worked with Python for data analysis and automation scripts.")
    simulate_typing("That's excellent experience! Which position(s) are you interested in applying for at TalentScout? Please also tell us why you're interested in this role.")
    
    # Position step
    simulate_typing("I'm interested in the Senior Frontend Developer position. I'm looking for a role where I can utilize my React expertise and mentor junior developers.")
    simulate_typing("Great choice! What's your current location? Are you open to relocation or remote work?")
    
    # Location step
    simulate_typing("I'm based in Seattle, WA. I prefer remote work but am open to hybrid arrangements.")
    simulate_typing("""Thank you for sharing your location preference. Now, please list your technical skills in detail:
- Programming languages and your proficiency level
- Frameworks and libraries you've used
- Development tools and environments
- Databases and other technologies
- Any certifications or specialized training

Please separate each item with commas and include your experience level with each.""")
    
    # Tech stack step
    simulate_typing("JavaScript (Expert, 5 years), React (Advanced, 4 years), Node.js (Intermediate, 3 years), Python (Intermediate, 2 years), HTML/CSS (Expert, 5 years), Git (Advanced), AWS (Basic), MongoDB (Intermediate), MySQL (Intermediate)")
    
    # Technical questions
    tech_questions_response = """Based on your experience with React, here are some technical questions:

Question 1: Can you explain the React component lifecycle methods and how they've changed with React Hooks? Please provide examples of how you've used them in your projects.

Question 2: Describe how you approach state management in large React applications. What libraries or patterns do you prefer and why?

Question 3: How do you optimize performance in React applications? Please share specific techniques you've implemented.

I'd like to start with the first question. Please provide a detailed response based on your experience."""
    
    simulate_typing(tech_questions_response)
    
    # Final message
    st.success("Basic interview flow completed successfully!")

def run_repetitive_text_demo():
    """Run a demonstration for handling repetitive text patterns."""
    st.subheader("Demo: Repetitive Text Handling")
    st.info("This demo shows how the system handles repetitive text patterns in user responses.")
    
    chatbot = TalentScoutChatbot()
    
    # Initial greeting
    simulate_typing("Which position(s) are you interested in applying for at TalentScout? Please also tell us why you're interested in this role.")
    
    # User inputs repetitive text
    repetitive_text = """I am interested in the full stack developer position. I am interested in the full stack developer position. I believe I am a good fit because I have experience with both frontend and backend technologies. I believe I am a good fit because I have experience with both frontend and backend technologies. I would like to work at TalentScout because of the innovative projects. I would like to work at TalentScout because of the innovative projects. I have worked on similar applications before and I enjoy creating full-stack solutions. I have worked on similar applications before and I enjoy creating full-stack solutions."""
    
    st.text_area("User input with repetition:", repetitive_text, height=150)
    
    # Sanitized version
    sanitized_text = sanitize_input(repetitive_text)
    
    # Show what the system does with it
    st.warning("System detects repetitive patterns and sanitizes the input:")
    st.text_area("Sanitized input:", sanitized_text, height=100)
    
    # Chatbot processes the response
    response = """I see you're interested in the Full Stack Developer position! Your experience with both frontend and backend technologies makes you a potential fit.

To better understand your background, could you tell me about your current location? Are you open to relocation or remote work?"""
    
    simulate_typing(response)
    
    st.success("The system successfully processed the input by removing repetitive patterns while preserving the key information!")

def run_assignment_text_demo():
    """Run a demonstration for handling assignment text pasting."""
    st.subheader("Demo: Assignment Text Pasting")
    st.info("This demo shows how the system handles cases where users paste assignment text instead of providing the requested information.")
    
    # Show the chatbot asking for tech stack
    simulate_typing("""Please list your technical skills in detail:
- Programming languages and your proficiency level
- Frameworks and libraries you've used
- Development tools and environments
- Databases and other technologies
- Any certifications or specialized training

Please separate each item with commas and include your experience level with each.""")
    
    # User pastes assignment text
    assignment_text = """Assignment Overview
You are tasked with developing an intelligent Hiring Assistant chatbot for "TalentScout," a fictional recruitment agency specializing in technology placements. The chatbot should assist in the initial screening of candidates by gathering essential information and posing relevant technical questions based on the candidate's declared tech stack.

Requirements
Functionality
- User Interface: Develop a clean and intuitive UI using Streamlit or Gradio where candidates can interact with the chatbot.
- Chatbot Capabilities: Greeting, information gathering, tech stack declaration, technical question generation.
- Technical Specifications: Python, Streamlit, Large Language Models (e.g., GPT-3/4, llama, etc).

Deliverables
- Source Code
- Documentation
- Demo
"""
    
    st.text_area("User pastes assignment text:", assignment_text, height=200)
    
    # Show what the system detects
    detection_result = """Assignment text detected!
- Technologies found: Python, Streamlit, GPT, LLM
- Position detected: Hiring Assistant
- Assignment type: Chatbot Development"""
    
    st.info(detection_result)
    
    # Chatbot response
    response = """I notice you've shared what appears to be assignment details rather than your personal information.

Let's focus on your application. Could you please provide your tech stack information? I can see this assignment involves Python, Streamlit, and LLMs - are these technologies you're familiar with? Please list your technical skills with your proficiency level for each."""
    
    simulate_typing(response)
    
    st.success("The system successfully detected the assignment text and extracted relevant information!")

def run_acknowledgment_demo():
    """Run a demonstration for handling simple acknowledgments."""
    st.subheader("Demo: Simple Acknowledgment Handling")
    st.info("This demo shows how the system handles simple acknowledgments when specific information is requested.")
    
    # Email request
    simulate_typing("Great! Could you please share your email address for further communication?")
    
    # User responds with just "ok"
    st.text_area("User response:", "Ok", height=50)
    
    # System detects acknowledgment
    st.info("System detects this is a simple acknowledgment, not an email address")
    
    # Chatbot provides more specific guidance
    response = "I need your email address for further communication. Could you please provide it?"
    simulate_typing(response)
    
    # User now provides email
    st.text_area("User provides email:", "jane.doe@example.com", height=50)
    
    # Chatbot continues with phone request
    simulate_typing("Thank you! Could you please provide your contact number where we can reach you?")
    
    st.success("The system successfully handled the simple acknowledgment and guided the user to provide the required information!")

def run_mixed_input_demo():
    """Run a demonstration for handling mixed inputs (instructions and information)."""
    st.subheader("Demo: Mixed Input Detection")
    st.info("This demo shows how the system handles messages containing both instructions and partial information.")
    
    # Chatbot asks for experience
    simulate_typing("Please describe your experience in detail, including years of experience, types of projects, technologies used, and role responsibilities.")
    
    # User provides mixed input with both instructions and information
    mixed_input = "I want to apply for the Data Scientist position. I have 3 years of experience working with Python and machine learning. My email is data.scientist@example.com and I'm based in Boston."
    
    st.text_area("User mixed input:", mixed_input, height=100)
    
    # System detects mixed input
    detection_info = """Mixed input detected:
- Contains position information: Data Scientist
- Contains experience information: 3 years
- Contains email: data.scientist@example.com
- Contains location: Boston
- Contains tech stack: Python, machine learning
- Contains instruction: "I want to apply for..."
"""
    
    st.info(detection_info)
    
    # Chatbot processes the information and continues
    response = """Thank you for sharing your experience with Python and machine learning, and I've noted your interest in the Data Scientist position.

I've recorded your email (data.scientist@example.com) and location (Boston) for our records.

Could you provide more details about your specific role responsibilities and the types of projects you've worked on?"""
    
    simulate_typing(response)
    
    st.success("The system successfully extracted multiple pieces of information from the mixed input!")

if __name__ == "__main__":
    run_demo()