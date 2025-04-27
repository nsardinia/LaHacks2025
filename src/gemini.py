import cv2
from key import TOKEN
from google import genai

class gemini:
    def __init__(self, token, text=None):
        self.client = genai.Client(api_key=token)
        self.content=[]
        self.text = text
        self.keywords = []



    def process(self, string):

        #not used anymore because we use paddle for word recog
        # #initial read
        # image = Image.open("/screenshot")
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",  contents=[string, "gather the information available in the text"]
        )

        img_response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",  contents=[response, "find and fix errors in the text. If unclear, label it"]
        )


        self.content.append(img_response)
        return img_response

    def get_keywords(self):
        for i,j in enumerate(self.content):
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-04-17",  contents=["write out 1-3 key words for this text.", j]
            )
            self.keywords[i] = response

        return self.keywords


    

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