import streamlit as st
from groq import Groq
import os 

# Initialize the Groq client
client = Groq()
import os

# Set the API key
api_key = os.environ.get("GROQ_API_KEY")

# Initialize the Groq client
client = Groq()
client.api_key = api_key

def format_response(response):
    # Split the response into sentences
    sentences = response.split(".")
    
    # Capitalize the first letter of each sentence
    sentences = [s.capitalize() for s in sentences]
    
    # Add periods to the end of each sentence
    sentences = [s.strip() + "." for s in sentences]
    
    # Join the sentences back into a paragraph
    formatted_response = " ".join(sentences)
    
    return formatted_response

def get_response_from_llama3(messages):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = []
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            response.append(content.strip())
    
    # Format the response
    formatted_response = format_response(" ".join(response))
    return formatted_response

# Streamlit app setup
st.title("Infinite Loop Chat with Llama-3")

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "Infinite loop chat with llama-3\n"},
        {"role": "assistant", "content": "A never-ending conversation I'll do my best to keep responding to your messages, and we'll have a chat loop that never ends.\n\nWhat's on your mind?"}
    ]

# Display initial assistant message
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.write(st.session_state.messages[1]["content"])

# Text input for user message
user_input = st.text_input("You: ", "")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.write("You: " + user_input)
    response = get_response_from_llama3(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.write(response)