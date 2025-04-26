from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
from key import TOKEN


client = genai.Client(api_key=TOKEN)

#initial read

for i i n
image = Image.open("/screenshot")
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-04-17",  contents=[image, "Gather the necessary/relevant text in the image."]
)

#fill in the gaps/bad data
img_response = client.models.generate_content(
    model="gemini-2.5-flash-preview-04-17",  contents=[response, "find and fix errors in the data. If unclear, label it"]
)


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



print(response.text)
print(img_response.text)
