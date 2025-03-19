from io import BytesIO
from urllib.request import urlopen

import librosa
import numpy as np


def process_audio_info(conversations: list[dict] | list[list[dict]], use_audio_in_video: bool):
    audios = []
    if isinstance(conversations[0], dict):
        conversations = [conversations]
    for conversation in conversations:
        for message in conversation:
            if not isinstance(message["content"], list):
                continue
            for ele in message["content"]:
                if ele["type"] == "audio":
                    if "audio" in ele:
                        path = ele["audio"]
                        if path.startswith("http://") or path.startswith("https://"):
                            audios.append(librosa.load(BytesIO(urlopen(path).read()), sr=16000)[0])
                        elif isinstance(path, np.ndarray):
                            if path.ndim > 1:
                                raise ValueError("Support only mono audio")
                            audios.append(path)
                        elif path.startswith("file://"):
                            audios.append(librosa.load(path[len("file://") :], sr=16000)[0])
                        else:
                            audios.append(librosa.load(path, sr=16000)[0])
                    else:
                        raise ValueError("Unknown audio {}".format(ele))
                if use_audio_in_video and ele["type"] == "video":
                    if "video" in ele:
                        path = ele["video"]
                        if path.startswith("http://") or path.startswith("https://"):
                            audios.append(librosa.load(BytesIO(urlopen(path).read()), sr=16000)[0])
                        elif path.startswith("file://"):
                            audios.append(librosa.load(path[len("file://") :], sr=16000)[0])
                        else:
                            audios.append(librosa.load(path, sr=16000)[0])
                    else:
                        raise ValueError("Unknown video {}".format(ele))
    if len(audios) == 0:
        audios = None
    return audios
