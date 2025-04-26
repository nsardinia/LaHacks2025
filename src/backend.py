async def start_websocket():
    async def handler(websocket):
        await video_receiver(websocket)
    
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

def get_videos():
    
