from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .import models, upload, chat
from .database import engine,SessionLocal
from .response import generate_response


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],

)

app.include_router(upload.router)
app.include_router(chat.router)


@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
     await websocket.accept()
     file_id = int(websocket.query_params.get("file_id", 1))  # fallback to 1
     db = SessionLocal()
     try:
        while True :
            user_msg = await websocket.receive_text()
            print("generating response")
            bot_reply = generate_response(user_msg,db,file_id)
            await websocket.send_text(bot_reply)
     except Exception as e:
        #await websocket.close()
        ...
     finally:
         db.close()