import streamlit as st
import requests
import time

# Set page config for title and favicon
st.set_page_config(
    page_title="✍️ Assignment Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            color: #1E88E5;
            text-align: center;
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title with emojis
    st.markdown("<h1 class='main-header'>📚 Assignment Buddy ✍️</h1>", unsafe_allow_html=True)
    st.markdown("### Transform your documents into handwritten notes ✨")
    
    uploaded_file = st.file_uploader("Upload your PDF or DOCX file 📂", type=['pdf', 'docx'])
    
    if uploaded_file:
        if st.button("✨ Generate Handwritten Notes"):
            with st.spinner("🔮 Working on your magic handwritten notes..."):
                # Upload file
                response = requests.post(
                    "http://localhost:5000/upload",
                    files={"file": uploaded_file}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    
                    # Poll for status
                    while True:
                        status_response = requests.get(f"http://localhost:5000{data['check_status']}")
                        status_data = status_response.json()
                        
                        if status_data['status'] == 'completed':
                            progress_bar.progress(100)
                            st.success("✨ Your handwritten notes are ready!")
                            st.markdown(f"### [📥 Download your handwritten notes](http://localhost:5000{status_data['download_link']})")
                            break
                        elif status_data['status'] == 'error':
                            st.error(f"❌ Error: {status_data.get('error', 'Unknown error')}")
                            break
                        
                        progress_bar.progress(50)
                        time.sleep(1)
                else:
                    st.error(f"❌ Error: {response.json().get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()