from aiohttp import web
import socketio

sio = socketio.AsyncServer(
    namespaces=["/chat"]
)
app = web.Application()
sio.attach(app)

@sio.event(namespace="/chat")
async def connect(sid, environ):
    print("connect ", sid)
    await sio.enter_room(sid, "chat_room", namespace="/chat")

@sio.event(namespace="/chat")
async def chat_message(sid, data):
    print("message ", data)
    await sio.emit(
        "chat_message", 
        data,
        namespace="/chat",
        room="chat_room"
    )

@sio.event(namespace="/chat")
async def disconnect(sid):
    print('disconnect ', sid)
    await sio.leave_room(sid, "chat_room", namespace="/chat")

if __name__ == '__main__':
    web.run_app(app)
