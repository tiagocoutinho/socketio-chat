import asyncio
import socketio
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

EVENT = "chat_message"
REGISTER = "chat_register"
NAME = sys.argv[1]

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established')
    await sio.emit(REGISTER, NAME)

@sio.event
async def chat_message(message):
    print(message)

@sio.event
async def disconnect():
    print('disconnected from server')

async def interactive_shell():
    session = PromptSession("Say something: ")
    while True:
        message = await session.prompt_async()
        await sio.emit(EVENT, message)

async def main():
    with patch_stdout():
        await sio.connect('http://localhost:8080')
        shell = asyncio.create_task(interactive_shell())
        await sio.wait()
    shell.cancel()

if __name__ == '__main__':
    asyncio.run(main())