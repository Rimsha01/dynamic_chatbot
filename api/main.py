from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .import models, upload
from .database import  engine


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




@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
     await websocket.accept()
     while True :
         try:
             user_msg = await websocket.receive_text()
             bot_reply = get_bot_response(user_msg)
             await websocket.send_text(bot_reply)
         except Exception as e:
             await websocket.close()
         break

