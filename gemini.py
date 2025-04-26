from google import genai
from google.genai import types
from PIL import Image

from key import TOKEN
from paddleocr import PaddleOCR

class gemini:
    def __init__(self, token, text=None):
        self.client = genai.Client(api_key=token)
        self.content=[]
        self.summary = None
        self.text = text
        self.files = []


    def process(self, string):

        #not used anymore because we use paddle for word recog
        # #initial read
        # image = Image.open("/screenshot")
        # response = self.client.models.generate_content(
        #     model="gemini-2.5-flash-preview-04-17",  contents=[image, "gather the information available in the text"]
        # )

        #fill in the gaps/bad data
        img_response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",  contents=[img_response, "find and fix errors in the text. If unclear, label it"]
        )

        self.content.append(img_response)

    def process_all(self):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",  contents=['\n'.join(self.content), "summarize the information in this text"]
        )

        self.summary = response
    
    def get_summary(self):
        return self.summary
    
    def refine(self, text):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17", contents=f"Based on the following texts and their confidence score, refine them. The lower the confidence score, the more you have to correct it to make sense and repair any hallucinations. For example, if a math equation is written erroneously and also has a low confidence score, you should correct the text to make the math equation correct. If the confidence score is high and the text makes sense, do nothing to it. {text}"
        )
        print(response.text)

    def prompt(self, string):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",  contents=['\n'.join(self.content), string]
        )
        return response

    def toJson(self):
        import json
        frame_counter =0
        for i in self.content:
            
            filename = f"ocr_frame_{frame_counter}.json"
            data = {
                "start_time":frame_counter*10,
                "end_time": frame_counter*10 + 10,
                "text": i
            }
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            frame_counter += 1

import cv2



def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    slides_info = ""
    frame_number = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_number % 480 == 0:
            frame_filename = f"frame_{frame_number:04d}.jpg"
            cv2.imwrite(frame_filename, frame)
            formatted = PaddleProcessWords(frame_filename)
            slides_info += f"Frame Number: {frame_number}\n"
            slides_info += f"{formatted}\n"
        frame_number += 1
    
    return slides_info




import cv2
from paddleocr import PaddleOCR

# Paddleocr supports Chinese, English, French, German, Korean and Japanese
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order



def PaddleProcessWords(img_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory


    # img_path = '/Users/bensirivallop/LA HACKS/LaHacks2025/Screenshot1.png'

    result = ocr.ocr(img_path, cls=True)

    res =0
    for idx in range(len(result)):
        res = result[idx]
    res_sorted = None
    if res is not None:
        res_sorted = sorted(res, key=lambda x: (x[0][0][1], x[0][0][1]))

    string = ''
    if res_sorted is not None:
        for line in res_sorted:
            formatted_line = f"Text: {line[1][0]}, Confidence: {line[1][1]}"
            print(formatted_line)
            string += formatted_line
            string += "\n"
    return string



if __name__ == "__main__":
    text = process_video("videoplayback.mp4")
    ai = gemini(TOKEN, text)
    ai.refine(text)

'''
EXMAPLE JSON
"video_path": "./data/test_lecture.mp4",
        "start_time": 0,
        "end_time": 10,
        "transcription": " So today we're going to go over some D-Log concepts. So the first thing that we're going to talk about today is just how to wire up a switch.",
        "tags": [
            {
                "tag": "D-Log",
                "score": 0.9
            },
            {
                "tag": "switch wiring",
                "score": 0.7
            }
        ]

    def refine(self, text):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17", contents=f"Based on the following texts and their confidence score, refine them. The lower the confidence score, the more you have to correct it to make sense and repair any hallucinations. For example, if a math equation is written erroneously and also has a low confidence score, you should correct the text to make the math equation correct. If the confidence score is high and the text makes sense, do nothing to it. {text}"
        )
        print(response.text)


if __name__ == "__main__":
    text = start.process_video("videoplayback.mp4")
    ai = gemini(TOKEN, text)
    ai.refine(text)


'''

#This generates an image.
'''
img_gen_response = client.models.generate_content(
    model="gemini-2.5-flash-exp-image-generation",
    contents=[image, 'Crop the image to exclude any unrelated texts and include only diagrams/graphs.'],
    config=types.GenerateContentConfig(
      response_modalities=['TEXT', 'IMAGE']
    )
)
'''


#this prints the cropped image 
'''
for part in img_gen_response.candidates[0].content.parts:
  if part.text is not None:
    print(part.text)
  elif part.inline_data is not None:
    image = Image.open(BytesIO((part.inline_data.data)))
    image.save('gemini-native-image.png')
    image.show()

'''




