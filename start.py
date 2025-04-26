#pip install paddle
#pip install paddleocr

import cv2



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
            print(line)
            string += line[1][0]
    print(string)


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
        res.print()
        # res.save_to_img(save_path="./layout_output/")
        res.save_to_json(save_path="./layout_output/")

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_number = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_number % 480 == 0:
            frame_filename = f"frame_{frame_number:04d}.jpg"
            cv2.imwrite(frame_filename, frame)
            PaddleProcessWords(frame_filename)

        frame_number += 1


# def PaddleLayout():
#     from pathlib import Path
#     from paddlex import create_pipeline

#     pipeline = create_pipeline(pipeline="PP-StructureV3")

#     input_file = "./Screenshot1.pdf"
#     output_path = Path("./layout_output/")

#     output = pipeline.predict(
#         input=input_file,
#         use_doc_orientation_classify=False,
#         use_doc_unwarping=False,
#         use_textline_orientation=False)

#     markdown_texts = ""
#     markdown_list=[]
#     markdown_images = []

#     for res in output:
#         md_info = res.markdown
#         markdown_list.append(md_info)
#         markdown_images.append(md_info.get("markdown_images", {}))

#     mkd_file_path = output_path / f"{Path(input_file).stem}.md"
#     mkd_file_path.parent.mkdir(parents=True, exist_ok=True)
#     with open(mkd_file_path, "w", encoding="utf-8") as f:
#         f.write(markdown_texts)

#     for item in markdown_images:
#         if item:
#             for path, image in item.items():
#                 file_path = output_path / path
#                 file_path.parent.mkdir(parents=True, exist_ok=True)
#                 image.save(file_path)

    """"
sample output
[[[442.0, 173.0], [1169.0, 173.0], [1169.0, 225.0], [442.0, 225.0]], ['ACKNOWLEDGEMENTS', 0.99283075]]
[[[393.0, 340.0], [1207.0, 342.0], [1207.0, 389.0], [393.0, 387.0]], ['We would like to thank all the designers and', 0.9357758]]
[[[399.0, 398.0], [1204.0, 398.0], [1204.0, 433.0], [399.0, 433.0]], ['contributors whohave been involved in the', 0.9592447]]
......"""



if __name__== '__main__':
    PaddleProcessWords('./Screenshot.png')

    # PaddleLayout()

