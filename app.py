import streamlit as st
from chatbot import TalentScoutChatbot
from utils import (
    validate_email, validate_phone, validate_tech_stack,
    sanitize_input, format_candidate_summary, save_candidate_data,
    analyze_sentiment
)

# Configure Streamlit page
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="👨‍💼",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .stChatInput {
        border-radius: 10px;
    }
    .stMarkdown {
        font-size: 1rem;
    }
    .sentiment-positive {
        color: green;
        font-style: italic;
    }
    .sentiment-negative {
        color: red;
        font-style: italic;
    }
    .sentiment-neutral {
        color: gray;
        font-style: italic;
    }
    .info-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize or reset session state variables."""
    if "initialized" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chatbot = TalentScoutChatbot()
        st.session_state.candidate_info = {
            "name": "",
            "email": "",
            "phone": "",
            "experience": "",
            "position": "",
            "location": "",
            "tech_stack": [],
            "tech_questions_asked": False,
            "sentiment_history": []
        }
        st.session_state.initialized = True

def display_sidebar():
    """Display candidate information and analytics in the sidebar."""
    with st.sidebar:
        st.title("Candidate Information")
        
        # Display current information
        if any(st.session_state.candidate_info.values()):
            with st.expander("Current Information", expanded=True):
                st.markdown(format_candidate_summary(st.session_state.candidate_info))
        
        # Display sentiment analysis
        if st.session_state.candidate_info.get("sentiment_history"):
            with st.expander("Interaction Analysis", expanded=True):
                sentiments = st.session_state.candidate_info["sentiment_history"]
                positive = sentiments.count("positive")
                negative = sentiments.count("negative")
                neutral = sentiments.count("neutral")
                
                st.write("**Sentiment Analysis:**")
                st.progress(positive/len(sentiments), "Positive Responses")
                st.progress(negative/len(sentiments), "Negative Responses")
                st.progress(neutral/len(sentiments), "Neutral Responses")
        
        # Save data button
        if st.button("Save Candidate Data"):
            save_candidate_data(st.session_state.candidate_info)
            st.success("Candidate data saved successfully!")
        
        # Reset button
        if st.button("Reset Conversation"):
            st.session_state.clear()
            st.rerun()

def main():
    st.title("TalentScout Hiring Assistant")
    st.write("Welcome to the TalentScout technical screening process! I'll help evaluate your technical skills and experience.")

    # Initialize session state
    initialize_session_state()

    # Display sidebar
    display_sidebar()

    # Display chat messages with sentiment analysis
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "user" and "sentiment" in message:
                sentiment_class = f"sentiment-{message['sentiment']}"
                st.markdown(f'<p class="{sentiment_class}">Sentiment: {message["sentiment"].title()}</p>', 
                          unsafe_allow_html=True)

    # Get user input
    if prompt := st.chat_input("Type your message here..."):
        # Sanitize input
        clean_input = sanitize_input(prompt)
        
        # Add user message to chat history
        sentiment = analyze_sentiment(clean_input)
        st.session_state.candidate_info["sentiment_history"].append(sentiment)
        
        message = {
            "role": "user",
            "content": clean_input,
            "sentiment": sentiment
        }
        st.session_state.messages.append(message)
        
        with st.chat_message("user"):
            st.write(clean_input)
            sentiment_class = f"sentiment-{sentiment}"
            st.markdown(f'<p class="{sentiment_class}">Sentiment: {sentiment.title()}</p>', 
                       unsafe_allow_html=True)

        try:
            # Get chatbot response
            response = st.session_state.chatbot.get_response(
                st.session_state.messages,
                st.session_state.candidate_info
            )

            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            if st.button("Reset and Try Again"):
                st.session_state.clear()
                st.rerun()

if __name__ == "__main__":
    main()