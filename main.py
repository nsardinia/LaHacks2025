from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
from key import TOKEN

class gemini:
    def __init__(self, token):
        self.client = genai.Client(api_key=token)


    def process(self, image):

        #initial read
        image = Image.open("/screenshot")
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",  contents=[image, "Gather the necessary/relevant text in the image."]
        )

        #fill in the gaps/bad data
        img_response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",  contents=[response, "find and fix errors in the data. If unclear, label it"]
        )

        print(img_response.text)

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




