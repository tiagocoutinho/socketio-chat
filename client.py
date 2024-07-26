import asyncio
import socketio
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

CHAT_NAMESPACE = "/chat"
EVENT = "chat_message"
REGISTER = "chat_register"
NAME = sys.argv[1]

sio = socketio.AsyncClient()
chat_event = sio.event(namespace=CHAT_NAMESPACE)

async def send_message(message):
    await sio.emit(EVENT, message, namespace=CHAT_NAMESPACE)

async def register(name):
    await sio.emit(REGISTER, name, namespace=CHAT_NAMESPACE)

@chat_event
async def connect():
    print('connection established')
    await register(NAME)

@chat_event
async def chat_message(message):
    print(message)

@chat_event
async def disconnect():
    print('disconnected from server')

async def interactive_shell():
    session = PromptSession("Say something: ")
    while True:
        message = await session.prompt_async()
        await send_message(message)

async def main():
    with patch_stdout():
        await sio.connect('http://localhost:8080', namespaces=[CHAT_NAMESPACE])
        shell = asyncio.create_task(interactive_shell())
        await sio.wait()
    shell.cancel()

if __name__ == '__main__':
    asyncio.run(main())