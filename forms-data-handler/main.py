from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import os
import requests


# app = FastAPI(docs_url=None, redoc_url=None)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_POST_URL = os.environ.get('GOOGLE_POST_URL')

class FormData(BaseModel):
    service: str
    sent_from: str
    name: str
    phone_or_email: str
    phone: str
    email: str
    message: str

def correct_data_check(data: FormData):
    if re.match(r'^[A-Za-zА-Яа-я -]{2,}$', data.name) is None:
        raise HTTPException(
            status_code=400, 
            detail={
                "error": True,
                "message": "Некорректное имя",
                "field": "name"
            }
        )
    if len(data.name) > 50:
        raise HTTPException(
            status_code=400, 
            detail={
                "error": True,
                "message": "Имя слишком длинное",
                "field": "name"
            }
        ) 
    if data.phone_or_email not in ['phone', 'email']:
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": "Некорректный тип контакта",
                "field": "phone_or_email"
            }
        )
    if data.phone_or_email == 'phone' and re.match(r'^\+?[1-9][0-9]{7,14}$', data.phone) is None:
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": "Некорректный номер телефона",
                "field": "phone"
            }
        )
    if data.phone_or_email == 'email' and re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', data.email) is None:
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": "Некорректный email",
                "field": "email"
            }
        )
    if len(data.message) > 1000:
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": "Сообщение слишком длинное",
                "field": "message"
            }
        )
    
def send_to_google(data: FormData):
    to_send_data = {
        "service": data.service,
        "sent_from": data.sent_from,
        "name": data.name,
        "message": data.message
    }

    if data.phone_or_email == 'phone':
        to_send_data["phone"] = data.phone 
    else:
        to_send_data["email"] = data.email
    
    return requests.post(GOOGLE_POST_URL, data=to_send_data)
    
@app.post("/send_data")
async def send_data(data: FormData):
    correct_data_check(data)
    try:
        send_to_google(data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": "Произошла ошибка отправки данных",
                "detail": str(e)
            }
        )
    return {"status": "ok", "message": "Данные успешно отправлены"}