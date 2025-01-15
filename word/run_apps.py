import subprocess
import webbrowser
import time
import sys
import os

def main():
    print("Starting Flask server...")
    # Start Flask server with shell=True for Windows compatibility
    flask_process = subprocess.Popen([sys.executable, 'app.py'], 
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    
    # Wait and check if Flask started successfully
    time.sleep(2)
    if flask_process.poll() is not None:
        # Process has terminated
        _, stderr = flask_process.communicate()
        print("Flask server failed to start:")
        print(stderr.decode())
        return
    
    print("Starting Streamlit server...")
    # Start Streamlit server
    streamlit_process = subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'st_app.py'])
    
    # Open browser after a short delay
    time.sleep(3)
    webbrowser.open('http://localhost:8501')
    
    try:
        # Keep the script running
        flask_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        flask_process.terminate()
        streamlit_process.terminate()
        flask_process.wait()
        streamlit_process.wait()
        print("Servers stopped.")

if __name__ == "__main__":
    main() 