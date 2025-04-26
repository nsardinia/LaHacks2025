from google import genai
from google.genai import types
from PIL import Image
import start
from key import TOKEN

class gemini:
    def __init__(self, token, text=None):
        self.client = genai.Client(api_key=token)
        self.content = []
        self.summary = None
        self.text = text


    def process(self, string):

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


if __name__ == "__main__":
    text = start.process_video("videoplayback.mp4")
    ai = gemini(TOKEN, text)
    ai.refine(text)


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




