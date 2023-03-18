import asyncio
import websockets
import nest_asyncio
import ast
import json

nest_asyncio.apply()

async def handle_state(data):
    inventory = ast.literal_eval(data['inventory'])
    valid_movements = ast.literal_eval(data['valid_movements'])
    hitpoints = data['hitpoints']
    print(hitpoints)

async def handle_status(data):
    zoom = data['zoom']
    print(zoom)

async def handle_data(data):
    data = json.loads(data)
    if data['type']:
        await handle_status(data)
    else:
        await handle_state(data)


async def handle_message(websocket):
    try:
        async for message in websocket:
            await handle_data(message)
    except websockets.exceptions.ConnectionClosedError:
        print('Connection closed')

async def start_websocket_server():
    async with websockets.serve(handle_message, "localhost", 8765):
        await asyncio.get_event_loop().run_forever()

def run_websocket_loop():
    try:
        asyncio.run(start_websocket_server())
    except KeyboardInterrupt:
        print('Exiting...')
