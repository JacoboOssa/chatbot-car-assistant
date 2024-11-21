#from chatbot.dialog_manager import ChatbotDialogManager
from fastapi import FastAPI
from .routes.chatbot_routes import router as chatbot_router
from .database.db import MongoDBConnection
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Car Troubleshooting Chatbot API",
    description="A backend API for a car troubleshooting chatbot using MongoDB, FastAPI, and AI techniques.",
    version="1.0.0"
)
'''
origins = [
    "https://integrative-task-2-nextjs-apo-b4gj.vercel.app",
    "http://localhost:8000", 
    "http://0.0.0.0:8000",
    
]
'''

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

db = MongoDBConnection()
app.state.db = db  # Guardar la conexión en el estado de la aplicación
app.include_router(chatbot_router)


@app.head('/')
@app.get('/')
async def main():
    return {'message': 'Welcome to the Automotive Assistance ChatBot'}

#if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    #chatbot = ChatbotDialogManager()
    #chatbot.start()
