import os
import streamlit as st
import shutil
from PIL import Image
from lyzr import QABot

os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

st.set_page_config(
    page_title="Lyzr",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png",
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Medical Assistant 🏥")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown("Introducing the Lyzr Medical Assistant! Seamlessly analyze your medical records with cutting-edge AI technology. Simply upload your documents, and unlock detailed insights instantly!")

def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")


# Set the local directory
data_directory = "data"

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Remove existing files in the data directory
remove_existing_files(data_directory)

# Streamlit app header
# st.title("PDF File Uploader")

# File upload widget
uploaded_file = st.file_uploader("Choose PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded PDF file to the data directory
    file_path = os.path.join(data_directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    
    # Display the path of the stored file
    st.success(f"File successfully saved")


def get_files_in_directory(directory="data"):
    # This function help us to get the file path along with filename.
    files_list = []

    # Ensure the directory exists
    if os.path.exists(directory) and os.path.isdir(directory):
        # Iterate through all files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Check if the path points to a file (not a directory)
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list


def rag_implementation():
    # This function will implement RAG Lyzr QA bot
    path = get_files_in_directory()
    path = path[0]

    rag = QABot.pdf_qa(
        input_files=[str(path)],
        llm_params={"model": "gpt-3.5-turbo"},
        # vector_store_params=vector_store_params
    )

    return rag


def resume_response():
    rag = rag_implementation()
    prompt = """  Give the description of the given record in these bullet points,
                    - Medication List: List current prescriptions, note any allergies, and assess compliance.
                    - Vital Signs: Review recent measurements such as blood pressure, heart rate, and temperature.
                    - Diagnostic Tests: Examine results of recent tests like blood work, imaging, or ECGs for any abnormalities.
                    - Progress Notes: Evaluate physician's observations, treatment plans, and any referrals made."""

    
    response = rag.query(prompt)
    return response.response

if uploaded_file is not None:
    automatice_response = resume_response()
    st.markdown(f"""{automatice_response}""")


# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown(
        """
     
The Lyzr Medical Assistant, powered by Lyzr QABot, streamlines the analysis of medical records by providing users with detailed insights in a user-friendly interface.For any inquiries or issues, please contact Lyzr.

    """
    )
    st.link_button("Lyzr", url="https://www.lyzr.ai/", use_container_width=True)
    st.link_button(
        "Book a Demo", url="https://www.lyzr.ai/book-demo/", use_container_width=True
    )
    st.link_button(
        "Discord", url="https://discord.gg/nm7zSyEFA2", use_container_width=True
    )
    st.link_button(
        "Slack",
        url="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw",
        use_container_width=True,
    )