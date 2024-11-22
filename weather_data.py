import subprocess
from multiprocessing import Process
import time
from pymongo import MongoClient

#client = MongoClient("mongodb://localhost:27017/")
#db = client['accident_db']
#collection = db['accidents']

# Data Upload Function
def upload_data_to_mongodb():
    
    """
    Simulates uploading data to MongoDB every minute.
    Replace the example data with your actual data upload logic.
    """
    while True:
        '''
        # Example data to insert
        data = {
            "Street": "Main St",
            "City": "Sample City",
            "County": "Sample County",
            "State": "Sample State",
            "Description": "Test accident description",
            "Severity": 3,
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Insert data into MongoDB
        collection.insert_one(data)
        print(f"Data uploaded to MongoDB: {data}")
        
        # Wait for 1 minute before the next upload
        '''
        print("hi\n")
        time.sleep(5)