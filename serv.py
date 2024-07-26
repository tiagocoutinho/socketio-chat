import aiohttp.web
import socketio

CHAT_ROOM = "chat_room"
EVENT = "chat_message"

app = aiohttp.web.Application()
sio = socketio.AsyncServer()
sio.attach(app)

USERS = {}

async def send_message(message):
    await sio.emit(EVENT, message, room=CHAT_ROOM)

@sio.event
async def connect(sid, environ):
    print(f"{sid} connected")

@sio.event
async def chat_register(sid, name):
    print(f"{sid} registered as {name}")
    USERS[sid] = name
    await sio.enter_room(sid, "chat_room")
    await send_message(f"{name} entered chat")

@sio.event
async def chat_message(sid, message):
    name = USERS.get(sid)
    if name is None:
        return
    await send_message(f"{name}: {message}")

@sio.event
async def disconnect(sid):
    name = USERS.pop(sid, None)
    print(f"{sid} ({name}) disconnected")
    if name:
        await sio.leave_room(sid, "chat_room")

if __name__ == '__main__':
    aiohttp.web.run_app(app)
