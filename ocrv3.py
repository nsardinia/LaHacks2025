#THIS ONE FAILS, IT ONLY LOOKS FOR TEXT


# from paddlex import create_pipeline
# chat_bot_config={
#     "module_name": "chat_bot",
#     "model_name": "ernie-3.5-8k",
#     "base_url": "https://qianfan.baidubce.com/v2",
#     "api_type": "openai",
#     "api_key": "api_key" # your api_key
# }

# retriever_config={
#     "module_name": "retriever",
#     "model_name": "embedding-v1",
#     "base_url": "https://qianfan.baidubce.com/v2",
#     "api_type": "qianfan",
#     "api_key": "api_key" # your api_key
# }

# pipeline = create_pipeline(pipeline="PP-ChatOCRv3-doc", initial_predictor=False)

# visual_predict_res = pipeline.visual_predict(
#     input="./Screenshot.png",
#     use_doc_orientation_classify=False,
#     use_doc_unwarping=False,
#     use_common_ocr=True,
#     use_seal_recognition=True,
#     use_table_recognition=True,
# )

# visual_info_list = []
# for res in visual_predict_res:
#     visual_info_list.append(res["visual_info"])
#     layout_parsing_result = res["layout_parsing_result"]

# vector_info = pipeline.build_vector(
#     visual_info_list,
#     flag_save_bytes_vector=True,
#     retriever_config=retriever_config,
# )
# chat_result = pipeline.chat(
#     key_list=["驾驶室准乘人数"],
#     visual_info=visual_info_list,
#     vector_info=vector_info,
#     chat_bot_config=chat_bot_config,
#     retriever_config=retriever_config,
# )
# print(chat_result)