import subprocess
from multiprocessing import Process
import time
from pymongo import MongoClient
from weather_data import upload_data_to_mongodb

# Function to run Streamlit app as a subprocess
def run_streamlit_app():
    """
    Launches the Streamlit app using subprocess.
    """
    subprocess.run(["streamlit", "run", "app.py"])

# Main Function
if __name__ == "__main__":
    # Define two processes: one for the app, one for data upload
    process_streamlit = Process(target=run_streamlit_app)
    process_upload = Process(target=upload_data_to_mongodb)
    
    # Start both processes
    process_streamlit.start()
    process_upload.start()
    
    # Wait for both processes to complete
    process_streamlit.join()
    process_upload.join()
