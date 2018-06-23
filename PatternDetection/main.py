'''
Created on 23 Jun 2018

@author: atind
'''
import pyaudio
import wave
import sys
import struct
from DetectionRecognisationSystem import DetectionRecognisationSystem
from Globals import GlobalConfig
CHUNK = 1024


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output2.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

DR = DetectionRecognisationSystem(None)
frames = []

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     testdata = []
#     for i in range(0,len(data),2):
#         testdata += [struct.unpack('<h',data[i:i + 2])]
#     print(testdata)
#     frames.append(data)

print("* done recording")

GlobalConfig().maxval = 32767
GlobalConfig().minval = -32768
GlobalConfig().noisefloor = 50
GlobalConfig().printself()
# while(1):
data = stream.read(CHUNK)
indata = []
for i in range(0,len(data),2):
    indata = struct.unpack('<h',data[i:i + 2])[0]
    realitylist, ddolist = DR.input(indata)
    DR.printinfo(realitylist)
    
        
   
    
# print(len(data))


        

# stream.stop_stream()
# stream.close()
# p.terminate()
# 
# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()