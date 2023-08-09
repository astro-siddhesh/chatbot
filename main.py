from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st
from tempfile import NamedTemporaryFile
import base64

def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        st.error("⚠️ OPENAI_API_KEY is not set")
        return
    
    st.set_page_config(page_title="myCSVBOT", layout="wide")
    st.title("🤖 myCSVBOT: Ask Questions About Your CSV")

    csv_file = st.file_uploader("📂 Upload a CSV file", type="csv")
    if csv_file:
        with NamedTemporaryFile(delete=False) as f:  # Create temporary file
            f.write(csv_file.getvalue())  # Save uploaded contents to file
            f.seek(0)  # Reset the buffer to`` the beginning
            llm = OpenAI(temperature=0)
            user_input = st.text_input("🔍 Ask a question about your CSV:", key="user_input")

            agent = create_csv_agent(llm, f.name, verbose=True)  # Pass temporary filename to create_csv_agent
            
            if user_input:
                response = agent.run(user_input)
                st.subheader("📢 Answer:")
                st.markdown(f"> {response}")

        user_question = st.text_input("🔍 Ask a question about your CSV:", key="user_question")

        if user_question:
            with st.spinner(text="⏳ Searching for an answer..."):
                response = agent.run(user_question)
                st.subheader("📢 Answer:")
                st.markdown(f"> {response}")

        # Display a download link for the uploaded CSV file
        st.markdown(get_download_link(f.name), unsafe_allow_html=True)

def get_download_link(file_path):
    with open(file_path, "rb") as file:
        file_content = file.read()
        base64_encoded = base64.b64encode(file_content).decode("utf-8")
        file_name = os.path.basename(file_path)
        return f'<a href="data:file/csv;base64,{base64_encoded}" download="{file_name}" style="text-decoration: none; color: #0071bd; font-weight: bold;">📥 Download CSV File</a>'

if __name__ == "__main__":
    main()
