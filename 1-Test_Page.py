import streamlit as st
from openai import OpenAI

def initialize_openai_client(api_key):
    """Initialize and return the OpenAI client."""
    return OpenAI(api_key=api_key)

def get_or_create_session_state(key, default):
    """Get or create a session state variable."""
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]

def display_previous_messages(messages):
    """Display all previous messages."""
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def add_and_display_new_message(role, content, messages):
    """Add a new message and display it."""
    messages.append({"role": role, "content": content})
    with st.chat_message(role):
        st.markdown(content)

def main():
    st.set_page_config(layout="wide")
    st.header(':blue[Pagina Principală]', divider='rainbow')
    st.write(':violet[Bine ați venit la asistentul Caietului de Sarcini -]')

    with st.expander(" ℹ️ Mesaj Informativ ℹ️  "):
        st.write("""
            Vă informăm că aceasta aplicatie se află într-o fază incipientă de dezvoltare. 
            În acest moment, funcționalitatea este limitată la furnizarea de răspunsuri generale.
        """)

    with st.sidebar:
        openai_api_key = st.text_input("Access Key", key="chatbot_api_key", type="password")
    
    if not openai_api_key:
        st.info("Vă rugăm să introduceți cheia de acces în bara laterală.")
        return

    client = initialize_openai_client(openai_api_key)
    openai_model = get_or_create_session_state("openai_model", "gpt-4-1106-preview")
    messages = get_or_create_session_state("messages", [])

    display_previous_messages(messages)

    prompt = st.chat_input("Adaugati mesajul aici.")
    if prompt:
        add_and_display_new_message("user", prompt, messages)

        # Generate and display the assistant's response
        response = client.chat.completions.create(
            model=openai_model,
            messages=messages,
            stream=True,
        )
        # Assuming `st.write_stream` is a hypothetical function to handle streaming responses.
        # In practice, you might need to handle the stream response differently.
        response_content = next(response)  # Get the first response from the stream
        add_and_display_new_message("assistant", response_content, messages)

if __name__ == "__main__":
    main()
