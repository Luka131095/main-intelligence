import streamlit as st
import openai
import os
from dotenv import load_dotenv
import base64
import time

# Set the page title for the browser tab
st.set_page_config(page_title="Converter Chatbot")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
print("Script started")  # Debug print

# Static image with CSS to center and shift upward using transform
image_path = "avl_logo.png"
if os.path.exists(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .image-container {{
                text-align: center; /* Center the container */
                padding-top: 0px; /* Ensure no extra padding pushes image down */
            }}
            .image-container img {{
                max-width: 300px;
                height: auto;
                display: block;
                margin: 0 auto; /* Center horizontally */
                transform: translateY(-50px); /* Shift upward by 50 pixels */
                pointer-events: none; /* Disable interactivity */
            }}
            div[data-testid="stChatInput"] {{
                position: fixed !important;
                bottom: 40px !important; /* Chat input position */
                width: 100% !important;
                max-width: 700px !important;
                left: 50% !important;
                transform: translateX(-50%) !important;
                z-index: 1000 !important;
            }}
            .footer-text {{
                position: fixed !important;
                bottom: 10px !important; /* Below chat input */
                width: 100% !important;
                max-width: 700px !important;
                left: 50% !important;
                transform: translateX(-50%) !important;
                z-index: 900 !important;
                text-align: center;
                font-size: 14px;
                color: #666;
            }}
            </style>
            <div class="image-container">
                <img src="data:image/png;base64,{encoded}" alt="Converter Technology Logo">
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.write(f"Debug: Image not found at {image_path}")

# Define type_writer function for model responses and initial message
def type_writer(text):
    for char in text:
        yield char
        time.sleep(0.005)  # Faster speed (0.005s per char)

# Define get_response function before it's called
def get_response():
    print("Processing query with history")  # Debug print
    try:
        # Build the full message history including the system prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Define SYSTEM_PROMPT
SYSTEM_PROMPT = """
You are an expert in the design and manufacturing of power converters specifically used for automotive component testing, with a focus on e-drive testing systems. Respond only to questions related to the design, manufacturing, or testing applications of power converters for high-speed, high-power, and high-torque dynamometer systems. Highlight technical aspects such as SiC MOSFET-based power electronics, switching frequencies up to 48 kHz, control frequencies up to 192 kHz, and integration with dynamometers for e-motor validation. If off-topic (e.g., general electronics or non-automotive converters), politely say: 'Sorry, I specialize in power converters for automotive component testing—please ask about design, manufacturing, or testing for e-drive systems.'
Provide detailed, technical answers based on industry knowledge and typical specifications where applicable.
"""

# Create a container for the chat input and footer to render immediately after logo
input_container = st.container()
with input_container:
    prompt = st.chat_input("Your question...")
    st.markdown(
        '<div class="footer-text">Developed by Luka Vrzogic</div>',
        unsafe_allow_html=True
    )

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# Create a container for chat history
chat_container = st.container()

# Display predefined first message and chat history
with chat_container:
    if not st.session_state.initialized:
        first_message = "Hello! I’m your Power Converter Assistant, specializing in the design, manufacturing, and testing of power converters for automotive component testing, particularly e-drive systems. I can provide detailed insights into high-speed, high-power, and high-torque dynamometer applications, including SiC MOSFET-based electronics, switching frequencies up to 48 kHz, control frequencies up to 192 kHz, and dynamometer integration for e-motor validation. Feel free to ask me anything related to these topics!"
        st.session_state.messages.append({"role": "assistant", "content": first_message})
        with st.chat_message("assistant"):
            "".join(char for char in st.write_stream(type_writer(first_message)))
            print(f"Rendered first message: {first_message}")
        st.session_state.initialized = True
    else:
        # Display chat history with markdown (instant display)
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                print(f"Rendered message: {msg['content']}")

# Handle user input after chat input is rendered
if prompt:
    print(f"Received prompt: {prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)  # Display user query instantly
            print("User message displayed")

        with st.chat_message("assistant"):
            response = get_response()
            "".join(char for char in st.write_stream(type_writer(response)))  # Typing effect for model response
            st.session_state.messages.append({"role": "assistant", "content": response})
            print(f"Assistant response: {response}")