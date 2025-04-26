
# server.py
import asyncio
import websockets
import cv2
import numpy as np
from main import PaddleProcessWords
import time
from main import gemini
from key import TOKEN

async def video_receiver(websocket, gemini_):
    print("Client connected")
    try:
        frame_counter = 0
        while True:
            data = await websocket.recv()
            # Data is expected to be binary (a JPEG image)
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is not None:
                frame_counter+=1
                if frame_counter >= 300: #this captures a frame every 20 seconds.
                    gemini_.process(PaddleProcessWords(frame))
                    frame_counter = 0
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        cv2.destroyAllWindows() 


async def main(gemin):
    #FILL IN THIS IP ADDRESS 
    start = time.time()


    async def handler(websocket):
        await video_receiver(websocket, gemin) # Pass the instance

    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started")
        await asyncio.Future()  # run forever

    end = time.time()

if __name__ == "__main__":
    gemin = gemini(TOKEN)
    asyncio.run(main(gemin))


