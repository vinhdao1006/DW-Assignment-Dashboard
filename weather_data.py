import subprocess
from multiprocessing import Process
import time
from pymongo import MongoClient

#mongodb+srv://DSS911:dss911@cluster0.fzsyw.mongodb.net/

client = MongoClient("mongodb+srv://DSS911:dss911@cluster0.fzsyw.mongodb.net/")
db = client['accident_db']
collection = db['accidents']

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


def test_mongodb_connection():
    try:
        # Connect to the MongoDB server
        client = MongoClient("mongodb+srv://DSS911:dss911@cluster0.fzsyw.mongodb.net/")
        
        # Check the server information to test the connection
        client.server_info()
        print("✅ MongoDB connection successful!")

        # Optional: List all databases
        databases = client.list_database_names()
        print("Databases:", databases)
        
        # Optional: List collections in a specific database
        db = client['US_Accidents_db']
        collections = db.list_collection_names()
        print("Collections in 'US_Accidents_db':", collections)
    
    except Exception as e:
        print("❌ MongoDB connection failed!")
        print("Error:", e)

if __name__ == "__main__":
    client = MongoClient("mongodb+srv://DSS911:dss911@cluster0.fzsyw.mongodb.net/")
    db = client['US_Accidents_db']
    collection = db['accidents']
    upload_data_to_mongodb()