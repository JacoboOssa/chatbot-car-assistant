import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class MongoDBConnection:
    def __init__(self):
        try:
            #db = os.getenv("MONGO_URL")
            db = "mongodb+srv://myAtlasDBUser:378Y5IPc9gz2in3t@myatlasclusteredu.mdgvmn3.mongodb.net/CarAssistanChatbot?retryWrites=true&w=majority&appName=myAtlasClusterEDU"
            #name = os.getenv("DB_NAME")
            name = "CarAssistanChatbot"
            self.client = MongoClient(db)
            self.db = self.client[name] 
            print("MongoDB connected successfully!")
        except Exception as e:
            print(f"Error connecting to Mongo DB: {e}")

    def get_collection(self, collection_name):
        return self.db[collection_name]

# Usage Example
# if __name__ == "__main__":
#     mongo = MongoDBConnection()

