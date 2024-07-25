import asyncio
import socketio

CHAT_NAMESPACE = "/chat"

sio = socketio.AsyncClient()
chat_event = sio.event(namespace=CHAT_NAMESPACE)


@chat_event
async def connect():
    print('connection established')

@chat_event
async def chat_message(data):
    print('message received with ', data)

@chat_event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('http://localhost:8080', namespaces=[CHAT_NAMESPACE])
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())