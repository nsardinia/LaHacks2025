
# server.py
import asyncio
import websockets
import cv2
import numpy as np
import time
from gemini import gemini
from key import TOKEN

async def video_receiver(websocket, gemini_):
    print("Client connected")
    try:
        frame_counter = 0 #it gets like 15 fps
        while True:
            data = await websocket.recv()
            # Data is expected to be binary (a JPEG image)
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is not None:
                frame_counter+=1
                if frame_counter >= 100: 
                    print("PROCESSING A FRAME")
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

    async def handler(websocket):
        await video_receiver(websocket, gemin) # Pass the instance

    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started")
        await asyncio.Future()  # run forever










if __name__ == "__main__":
    gemin = gemini(TOKEN)
    asyncio.run(main(gemin))


'''
    # below was unused


    def PaddleProcessMath():
    from paddlex import create_pipeline

    pipeline = create_pipeline(pipeline="formula_recognition")

    output = pipeline.predict(
        input="./Screenshot1.png",
        use_layout_detection=True ,
        use_doc_orientation_classify=False, #we can say yes, but prolly inef
        use_doc_unwarping=False, # we can do yes, but probably inef
        layout_threshold=0.5,
        layout_nms=True,
        layout_unclip_ratio=1.0,
        layout_merge_bboxes_mode="large"
    )
    for res in output:
        # res.print()
        # res.save_to_img(save_path="./layout_output/")
        res.save_to_json(save_path="./layout_output/")











'''