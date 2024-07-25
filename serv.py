import aiohttp.web
import socketio

CHAT_NAMESPACE = "/chat"

app = aiohttp.web.Application()
sio = socketio.AsyncServer(namespaces=[CHAT_NAMESPACE])
sio.attach(app)
chat_event = sio.event(namespace=CHAT_NAMESPACE)


@chat_event
async def connect(sid, environ):
    print("connect ", sid)
    await sio.enter_room(sid, "chat_room", namespace=CHAT_NAMESPACE)

@chat_event
async def chat_message(sid, data):
    print("message ", data)
    await sio.emit(
        "chat_message", 
        data,
        namespace="/chat",
        room="chat_room"
    )

@chat_event
async def disconnect(sid):
    print('disconnect ', sid)
    await sio.leave_room(sid, "chat_room", namespace=CHAT_NAMESPACE)

if __name__ == '__main__':
    aiohttp.web.run_app(app)
