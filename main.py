import importlib.util
import subprocess
import os
from datetime import datetime
import time

if importlib.util.find_spec("pyaudio") is None:
    print("pyaudio is not installed. Installing...")
    subprocess.run(["pip", "install", "pyaudio"])

if importlib.util.find_spec("wave") is None:
    print("wave is not installed. Installing...")
    subprocess.run(["pip", "install", "wave"])

import pyaudio
import wave

def spinner():
    while True:
        for cursor in '|/-\\':
            yield cursor

spinner_handler = spinner()

FORMAT = pyaudio.paInt16
CHANNELS = 1  
RATE = 44100  
CHUNK = 1024  

try:
    RECORD_MINUTES = int(input("enter the number of minutes to record: "))
except ValueError:
    print("ERROR: input Please enter a valid integer.")
    exit()

current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_FILENAME = f"./audios/audio_{current_datetime}.wav"

audio = pyaudio.PyAudio()

mic_device_index = None
for i in range(audio.get_device_count()):
    info = audio.get_device_info_by_index(i)
    if 'microphone' in info['name'].lower(): 
        mic_device_index = i
        break

if mic_device_index is None:
    print("External microphone not found.")
    exit()

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=mic_device_index)

print("Recording....", end='', flush=True)

frames = []
record_frames = int(RATE / CHUNK * 60 * RECORD_MINUTES) 

for i in range(record_frames):
    data = stream.read(CHUNK)
    frames.append(data)
    if i % 100 == 0:
        print(f'\b{next(spinner_handler)}', end='', flush=True)
        time.sleep(0.1)

print("\bFinished recording.")
stream.stop_stream()
stream.close()
audio.terminate()

with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio saved to {OUTPUT_FILENAME}")