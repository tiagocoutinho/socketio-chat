import asyncio
import socketio

sio = socketio.AsyncClient()

@sio.event(namespace="/chat")
async def connect():
    print('connection established')

@sio.event(namespace="/chat")
async def chat_message(data):
    print('message received with ', data)
    #await sio.emit('my response', {'response': 'my response'})

@sio.event(namespace="/chat")
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('http://localhost:8080', namespaces=["/chat"])
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())