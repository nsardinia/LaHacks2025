
# server.py
import asyncio
import websockets
import cv2
import numpy as np

import time



# --- your code here ---
time.sleep(3)  # simulate some work

end = time.time()

print(f"Elapsed time: {end - start:.2f} seconds")


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
                if frame_counter >= 600: #this captures a frame every 20 seconds.
                    gemini_.process(frame)
                    frame_counter = 0
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        cv2.destroyAllWindows() 


async def main(gemin):
    #FILL IN THIS IP ADDRESS 



    async def handler(websocket):
        await video_receiver(websocket, gemin) # Pass the instance

    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    gemin = gemini(TOKEN)
    asyncio.run(main(gemin))


