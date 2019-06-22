import wave
from pyaudio import PyAudio, paInt16
from PIL import ImageGrab
import pyaudio
import numpy as np
import cv2
import time
import os
mkpath="C:\\录屏\\"
os.mkdir(mkpath)
while True:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "C:\\录屏\\output.wav"

    p = pyaudio.PyAudio()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    audio_record_flag = True
    def callback(in_data, frame_count, time_info, status):
        wf.writeframes(in_data)
        if audio_record_flag:
            return (in_data, pyaudio.paContinue)
        else:
            return (in_data, pyaudio.paComplete)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    stream_callback=callback)
    image = ImageGrab.grab()#获得当前屏幕
    length, width = image.size  # 获得当前屏幕的大小w
    fourcc = cv2.VideoWriter_fourcc(*'XVID')#编码格式
    video = cv2.VideoWriter('C:\\录屏\\test.mp4', fourcc, 32, (length, width))

    print("video recording!!!!!")
    stream.start_stream()
    print("audio recording!!!!!")
    record_count = 0
    while True:
        img_rgb = ImageGrab.grab()
        img_bgr=cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)#转为opencv的BGR格式
        video.write(img_bgr)
        record_count += 1
        if(record_count >19200):
            break
        print(record_count, time.time())

    audio_record_flag = False
    while stream.is_active():
        time.sleep(1)

    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()
    print("audio recording done!!!!!")

    video.release()
    cv2.destroyAllWindows()
    print("video recording done!!!!!")
    time.sleep(600)
    os.remove("C:\\录屏\\output.wav")
    os.remove("C:\\录屏\\test.mp4")
    continue
