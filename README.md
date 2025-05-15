# TalentScout Hiring Assistant

A sophisticated chatbot that acts as an intelligent hiring assistant for TalentScout, a fictional technology recruitment agency. This assistant gathers candidate information and asks relevant technical questions based on the candidate's declared tech stack.

## Features

### Core Functionality
- **Information Collection**: Gathers essential candidate details including name, contact information, experience, desired position, location, and tech stack.
- **Technical Assessment**: Generates relevant technical questions based on the candidate's specified technologies and experience level.
- **Conversation Flow Management**: Maintains context throughout the conversation to provide a natural interview experience.
- **Result Storage**: Saves candidate data and responses for later evaluation.

### Enhanced Input Handling Features
- **Repetitive Text Detection**: Identifies when users paste repetitive content and extracts meaningful information.
- **Assignment Text Handling**: Detects when users paste assignment text instead of providing their own information, and extracts relevant technology mentions.
- **Simple Acknowledgment Processing**: Provides helpful prompts when users respond with simple acknowledgments (like "ok") when specific information is needed.
- **Mixed Input Management**: Extracts multiple pieces of information when users provide a mix of instructions and personal data in a single response.
- **Content Validation**: Validates email addresses, phone numbers, and other inputs to ensure proper format.

## Installation

### Prerequisites
- Python 3.8 or higher
- Pip package manager

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure
- `app.py`: Main Streamlit application
- `chatbot.py`: Core chatbot logic and handling functionality
- `utils.py`: Utility functions for data processing and validation
- `demo.py`: Demonstration script showcasing various features
- `requirements.txt`: Project dependencies
- `data/`: Directory for storing candidate responses and analysis

## Demo Scenarios

The demo script (`demo.py`) showcases how the assistant handles various scenarios:

1. **Basic Interview Flow**: Standard workflow for gathering candidate information
2. **Repetitive Text Handling**: Detecting and managing repetitive patterns
3. **Assignment Text Pasting**: Extracting useful information when assignment details are pasted
4. **Simple Acknowledgments**: Providing guidance when users give simple responses like "ok"
5. **Mixed Input Handling**: Processing messages containing both instructions and information

To run the demo:
```bash
streamlit run demo.py
```

## Technical Implementation

### Problematic Input Handling
- **Pattern Detection**: Uses regex and pattern matching to identify repetitive content, assignment text pasting, and mixed inputs.
- **Content Extraction**: Employs natural language processing techniques to extract relevant information even from problematic inputs.
- **User Guidance**: Provides specific guidance to help users provide the requested information.

### Technology Stack
- **Framework**: Streamlit for the user interface
- **Language Processing**: Custom-built detection algorithms with regex pattern matching
- **Data Storage**: JSON-based storage for candidate information

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- Streamlit for the intuitive UI framework
- Python community for the robust libraries that made this project possible

## Features in Detail

### 1. Information Gathering
The chatbot collects the following information from candidates:
- Full Name
- Email Address
- Phone Number
- Years of Experience
- Desired Position(s)
- Current Location
- Tech Stack (programming languages, frameworks, tools)

### 2. Technical Assessment
- Dynamically generates questions tailored to the candidate's declared tech stack
- Adapts question difficulty based on experience level
- Analyzes response quality, including:
  - Detail level
  - Code snippet inclusion
  - Example usage
  - Response length and complexity

### 3. Context Handling
- Maintains conversation context throughout the interaction
- Provides personalized follow-up questions based on previous responses
- Ensures a natural, flowing conversation experience

### 4. Response Analysis
Candidate responses are analyzed for:
- Technical proficiency
- Response quality metrics
- Relevance to the question
- Overall communication effectiveness

## Technical Implementation

### Language Model Integration
This project leverages Hugging Face Transformers to:
1. Generate natural conversational responses
2. Create relevant technical questions based on the candidate's tech stack
3. Maintain context awareness throughout the interaction

The implementation uses a distilled GPT-2 model, providing a good balance between:
- Performance
- Response quality
- Resource requirements

### Fallback Mechanisms
The system includes rule-based fallbacks for:
- Network connectivity issues
- Model loading failures
- Response generation problems

This ensures the chatbot remains functional even when LLM services are unavailable.

### Data Privacy & Security
- Input sanitization prevents injection attacks
- Structured data storage with proper formatting
- Optional data encryption capabilities

## Challenges & Solutions

1. **Context Management**
   - Solution: Implemented structured conversation flow
   - Tracked conversation state
   - Maintained candidate information throughout the session

2. **Technical Question Generation**
   - Solution: Combined LLM and template approaches
   - Dynamically generated questions based on tech stack
   - Adjusted question complexity based on experience level

3. **Response Quality Analysis**
   - Solution: Multi-dimensional analysis
   - Tracked technical content, examples, and code snippets
   - Provided quality metrics for evaluation

4. **LLM Integration**
   - Solution: Implemented fallback mechanisms
   - Optimized prompts for better responses
   - Cached model for improved performance

## Running the Project

### Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Testing
To run the automated demo with simulated responses:
```bash
python demo.py --auto
```

## Acknowledgments

- Streamlit for the excellent UI framework
- Hugging Face for transformer models and tokenizers
- PyTorch for deep learning capabilities

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or suggestions, please open an issue in the repository. 