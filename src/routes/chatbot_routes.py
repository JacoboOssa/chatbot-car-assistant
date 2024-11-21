import uuid
from fastapi import APIRouter, HTTPException, Header, Request, Body, Security
from fastapi.encoders import jsonable_encoder
from ..models.users import User
from ..models.requests import QuestionRequest
from typing import Annotated
from passlib.context import CryptContext
import jwt
from fastapi.security import HTTPBearer
from ..services.user_services import UserServices
#from services.user_services import UserServices
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#SECRET_KEY = os.getenv("SECRET_KEY", "secretkey")
SECRET_KEY = "4h8j9k6B$1!2dLqVzR@5pNcX"
ALGORITHM = "HS256"
security = HTTPBearer()

router = APIRouter()
# db_connection = MongoDBConnection()
# dal = CarTroubleshootingDAL(db_connection)
async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    
    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        db = request.app.state.db
        user = db.get_collection("users").find_one({"_id": payload["user_id"]})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

@router.post("/user/")
async def create_user(request: Request, user: User = Body(...)):
    user_dict = jsonable_encoder(user)
    user_dict["password"] = pwd_context.hash(user.password)  # Encriptar contraseña
    db = request.app.state.db
    try:
        new_user = db.get_collection("users").insert_one(user_dict)
        created_user = db.get_collection("users").find_one({"_id": new_user.inserted_id})
        return created_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    
    
@router.post("/login/")
async def login(request: Request, email: str = Body(...), password: str = Body(...)):
    db = request.app.state.db
    user = db.get_collection("users").find_one({"email": email})
    
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = jwt.encode({"user_id": str(user["_id"]),"name": user["name"],"email": user["email"]}, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token, "name": user["name"], "email": user["email"]}

@router.post("/user/requests/")
async def create_request(request: Request, question_request: QuestionRequest = Body(...), current_user: dict = Security(get_current_user)):
    db = request.app.state.db

    user_service = UserServices()
    
    question = question_request.question
    evidence = user_service._parse_user_input_starting(question)

    
    # Manejo de la solicitud
    if "help" in question.lower():  # Caso 1: Solicitud de ayuda
        help_message = """
        Welcome to the Car Troubleshooting Chatbot!
        Here are some examples of keywords you can use:
        
        - "starter doesn't crank" (The starter motor does not turn over)
        - "low battery" (The battery voltage is low)
        - "high battery" (The battery voltage is high, potentially overcharged)
        - "no spark" (No spark at the spark plugs)
        - "fuel present" (Fuel is reaching the system)
        - "stalls in rain" (The engine stalls when it rains)
        - "engine doesn't fire" (The engine doesn’t start firing at all)

        Just type one of these or similar phrases to get help with your car's problem.
        """
        return {"message": "Help response", "help": help_message}
    elif evidence:
        problem, diagnosis, probability, generalProblem, generalDiagnosis = user_service.process_question(question)
        
        new_request = {
            "inputQuestion": question,
            "speceficproblem": problem,
            "specificdiagnosis": diagnosis,
            "probability": probability,
            "generalProblem": generalProblem,
            "generalDiagnosis": generalDiagnosis,
            "createdAt": datetime.now(),
            "_id": uuid.uuid4().hex
        }
        
        db.get_collection("users").update_one(
            {"_id": current_user["_id"]},
            {"$push": {"requests": new_request}}
        )
        
        return {"message": "Request added successfully", "request": new_request}
    else:
        return {"message": "Invalid input. Please provide a valid question or ask for 'help'."}

@router.get("/user/requests/")
async def get_requests(request: Request, current_user: dict = Security(get_current_user)):
    db = request.app.state.db
    requests = db.get_collection("users").find_one({"_id": current_user["_id"]})
    if not requests:
        return {"message": "User not found", "requests": []}
    
    return {"requests": requests["requests"]}

@router.get("/user/requests/{request_id}")
async def get_request(request: Request, request_id: str, current_user: dict = Security(get_current_user)):
    db = request.app.state.db
    request = db.get_collection("users").find_one({"_id": current_user["_id"], "requests._id": request_id}, {"requests.$": 1})
    if not request:
        return {"message": "Request not found"}
    
    return request["requests"][0]






    
