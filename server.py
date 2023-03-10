import asyncio
import websockets
import nest_asyncio
import ast
import json

nest_asyncio.apply()

async def handle_data(data):
    state = json.loads(data)
    print(state)
    inventory = ast.literal_eval(state['inventory'])
    valid_movements = ast.literal_eval(state['valid_movements'])
    hitpoints = state['hitpoints']
    print('Inventory: ', inventory)
    print(len(valid_movements))

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
