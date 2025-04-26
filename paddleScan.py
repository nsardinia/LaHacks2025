'''

from paddleocr import PaddleOCR, draw_ocr

# Paddleocr supports Chinese, English, French, German, Korean and Japanese
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order
ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
img_path = './Screenshot.png'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# # draw result
# from PIL import Image
# result = result[0]
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/fonts/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')


'''
from paddlex import create_pipeline


#for pipeline data, https://paddlepaddle.github.io/PaddleOCR/latest/en/paddlex/quick_start.html#python-script-usage
pipeline = create_pipeline(pipeline="doc_preprocessor")
output = pipeline.predict('./Screenshot2.png')
for res in output:
    res.print()
    res.save_to_img("./output/")
    res.save_to_json("./output/")


from paddlex import create_pipeline

pipeline = create_pipeline(pipeline="layout_parsing")

output = pipeline.predict(
    input="./Screenshot2.png",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)
for res in output:
    res.print()  ## Print the structured output of the prediction
    res.save_to_img(save_path="./layout_parse/")  ## Save the visualized image results of all submodules for the current image
    res.save_to_json(save_path="./layout_parse/")  ## Save the structured JSON results for the current image
    res.save_to_xlsx(save_path="./layout_parse/")  ## Save the sub-table results in XLSX format for the current image
    res.save_to_html(save_path="./layout_parse/")  ## Save the sub-table results in HTML format for the current image
