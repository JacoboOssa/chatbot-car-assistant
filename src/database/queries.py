from pymongo import MongoClient

class CarTroubleshootingDAL:
    def __init__(self, db_connection):
        self.collection = db_connection.get_collection("troubleshooting_logs")

    # CRUD operations
    def log_user_input(self, user_id, symptom, diagnosis=None):
        """Log user input and optional diagnosis."""
        document = {
            "user_id": user_id,
            "symptom": symptom,
            "diagnosis": diagnosis
        }
        result = self.collection.insert_one(document)
        return result.inserted_id

    def update_diagnosis(self, user_id, diagnosis):
        """Update the diagnosis for a specific user."""
        self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"diagnosis": diagnosis}}
        )

    def get_user_logs(self, user_id):
        """Retrieve logs for a specific user."""
        return list(self.collection.find({"user_id": user_id}))

    def get_all_logs(self):
        """Retrieve all logs (for admin or testing purposes)."""
        return list(self.collection.find())

    def delete_user_logs(self, user_id):
        """Delete logs for a specific user."""
        self.collection.delete_many({"user_id": user_id})