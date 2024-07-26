import aiohttp.web
import socketio

CHAT_NAMESPACE = "/chat"
CHAT_ROOM = "chat_room"
EVENT = "chat_message"

app = aiohttp.web.Application()
sio = socketio.AsyncServer(namespaces=[CHAT_NAMESPACE])
sio.attach(app)
chat_event = sio.event(namespace=CHAT_NAMESPACE)

USERS = {}

async def send_message(message):
    await sio.emit(EVENT, message, namespace=CHAT_NAMESPACE, room=CHAT_ROOM)

@chat_event
async def connect(sid, environ):
    print(f"{sid} connected")

@chat_event
async def chat_register(sid, name):
    print(f"{sid} registered as {name}")
    USERS[sid] = name
    await sio.enter_room(sid, "chat_room", namespace=CHAT_NAMESPACE)
    await send_message(f"{name} entered chat")

@chat_event
async def chat_message(sid, message):
    name = USERS.get(sid)
    if name is None:
        return
    await send_message(f"{name}: {message}")

@chat_event
async def disconnect(sid):
    name = USERS.pop(sid, None)
    print("{sid} ({name}) disconnected")
    if name:
        await sio.leave_room(sid, "chat_room", namespace=CHAT_NAMESPACE)

if __name__ == '__main__':
    aiohttp.web.run_app(app)
