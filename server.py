# server.py
import asyncio
import websockets
import cv2
import numpy as np


async def video_receiver(websocket):
    print("Client connected")
    try:
        frame_counter = 0
        while True:
            data = await websocket.recv()
            # Data is expected to be binary (a JPEG image)
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is not None:
                frame_counter += 1
                cv2.imshow('Video Stream', frame)

                if frame_counter >= 600:
                    frame_counter = 0

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Quit key pressed")
                    break
            else:
                print("Received empty frame")

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        cv2.destroyAllWindows()


async def main():
    async def handler(websocket):
        await video_receiver(websocket)

    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())