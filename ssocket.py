
# server.py
import asyncio
import websockets
import cv2
import numpy as np

from main import gemini
from key import TOKEN

async def video_receiver(websocket):
    print("Client connected")
    try:
        while True:
            data = await websocket.recv()
            # Data is expected to be binary (a JPEG image)
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is not None:
                # process(frame)
                print("RECEIVED a frame")
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        cv2.destroyAllWindows()

# def run():
#     gemin.process()

async def main():
    #FILL IN THIS IP ADDRESS
    async with websockets.serve(video_receiver, "0.0.0.0", 8765):
        print("WebSocket server started")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    gemin = gemini(TOKEN)
    asyncio.run(main(),)


