import json
import os




# open up the jsons and loop thru em
# since they are on the same data, the jsons should be the same length

def summarize_trans(transcription_json):
    with open(transcription_json, 'r') as f:
        if not os.path.exists(transcription_json):
            print(f"File {transcription_json} not found!")
            return
        data_trans = json.load(f)
        data_trans = data_trans.split()   
        return data_trans
    
def summarize_video(video_json):
    with open(video_json, 'r') as f:
        if not os.path.exists(video_json):
            print(f"File {video_json} not found!")
            return
        data_vid = json.load(f)
        data_vid = data_vid.split()   
        return data_vid

def combine_jsons(trans_arr, vid_arr):
    keyword_dict = {}
    for i in range(len(trans_arr)):
        #combine the jsons
        #create a separate thing for the keywords
        #
        print(i)



def create_time_frames(key_dict):
    pass


if __name__ == "__main__":
    trans = summarize_trans("src/videos.json")
    vid = summarize_video("src/videos.json")



#We'll query the gemini here.
# 