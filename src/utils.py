from typing import List, Dict, TypedDict

class Tag(TypedDict):
    tag: str
    score: float

class Clip(TypedDict):
    video_path: str
    start_time: int
    end_time: int
    transcription: str
    tags: List[Tag]
