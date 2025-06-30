from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from auth import hash_pwd, verify_pwd
from db import Session, User, Chat, Conversation
from groq_client import ask_groq
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_303_SEE_OTHER
from fastapi import APIRouter
import random

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = Session()
    user = db.query(User).filter(User.username == username).first()
    if user and verify_pwd(password, user.password):
        request.session["user_id"] = user.id
        return RedirectResponse("/chat", status_code=HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Usuario o contraseña incorrecta"})

@app.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...)):
    db = Session()
    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse("login.html", {"request": request, "error": "El usuario ya existe"})
    new_user = User(username=username, password=hash_pwd(password))
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return templates.TemplateResponse("login.html", {"request": request, "error": "El usuario ya existe (error de base de datos)"})
    request.session["user_id"] = new_user.id
    return RedirectResponse("/chat", status_code=HTTP_303_SEE_OTHER)

@app.get("/chat")
def chat_page(request: Request, conversation_id: int = None):
    db = Session()
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login")
    user = db.query(User).get(user_id)
    conversations = db.query(Conversation).filter_by(user_id=user_id).order_by(Conversation.created_at.desc()).all()
    if conversation_id:
        conversation = db.query(Conversation).filter_by(id=conversation_id, user_id=user_id).first()
        if not conversation:
            return RedirectResponse("/chat")
    else:
        conversation = conversations[0] if conversations else None
    chats = conversation.chats if conversation else []
    return templates.TemplateResponse("chat.html", {"request": request, "chats": chats, "conversations": conversations, "active_conversation": conversation})

@app.post("/chat")
def send_message(request: Request, message: str = Form(None), conversation_id: int = Form(None)):
    db = Session()
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login", status_code=HTTP_303_SEE_OTHER)
    if not conversation_id:
        # Si no hay conversación, crea una nueva
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
    else:
        conversation = db.query(Conversation).filter_by(id=conversation_id, user_id=user_id).first()
        if not conversation:
            conversation = Conversation(user_id=user_id)
            db.add(conversation)
            db.commit()
    if message is None:
        return RedirectResponse(f"/chat?conversation_id={conversation.id}", status_code=HTTP_303_SEE_OTHER)
    reply = ask_groq(message)
    db.add(Chat(user_id=user_id, conversation_id=conversation.id, user_msg=message, ai_response=reply))
    db.commit()
    return RedirectResponse(f"/chat?conversation_id={conversation.id}", status_code=HTTP_303_SEE_OTHER)

@app.post("/new_chat")
def new_chat(request: Request):
    db = Session()
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login", status_code=HTTP_303_SEE_OTHER)
    # Generar título con IA (o placeholder si no hay IA)
    try:
        first_message = "Crea un título breve para una conversación de chat con IA."
        ai_title = ask_groq(first_message)
        title = ai_title.strip().split('\n')[0][:40]
    except Exception:
        title = f"Chat IA #{random.randint(1000,9999)}"
    conversation = Conversation(user_id=user_id, title=title)
    db.add(conversation)
    db.commit()
    return RedirectResponse(f"/chat?conversation_id={conversation.id}", status_code=HTTP_303_SEE_OTHER)

@app.post("/delete_chat")
def delete_chat(request: Request, conversation_id: int = Form(...)):
    db = Session()
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login", status_code=HTTP_303_SEE_OTHER)
    conversation = db.query(Conversation).filter_by(id=conversation_id, user_id=user_id).first()
    if conversation:
        db.query(Chat).filter_by(conversation_id=conversation_id).delete()
        db.delete(conversation)
        db.commit()
    return RedirectResponse("/chat", status_code=HTTP_303_SEE_OTHER)

@app.post("/rename_chat")
def rename_chat(request: Request, conversation_id: int = Form(...), new_title: str = Form(...)):
    db = Session()
    user_id = request.session.get("user_id")
    if not user_id:
        return JSONResponse({"success": False, "error": "No autorizado"}, status_code=401)
    conversation = db.query(Conversation).filter_by(id=conversation_id, user_id=user_id).first()
    if conversation:
        conversation.title = new_title
        db.commit()
        return JSONResponse({"success": True, "title": new_title})
    return JSONResponse({"success": False, "error": "No encontrado"}, status_code=404)

@app.get("/new_chat")
def new_chat_get(request: Request):
    # Redirigir a POST para evitar error si se accede por GET
    return RedirectResponse("/chat", status_code=HTTP_303_SEE_OTHER)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")
