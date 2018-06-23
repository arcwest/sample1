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
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 1
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
maxddoforlearning = 16
GlobalConfig().maxval = 32767
GlobalConfig().minval = -32768
GlobalConfig().noisefloor = 50
GlobalConfig().printself()
GlobalConfig().printenable = 0
# while(1):
# data = stream.read(CHUNK)
# 
# indata = []
# chunkprocessstarttime = time.time()
# f = open('log.txt','w')
# GlobalConfig().logfunc = f.write
# for i in range(0,len(data),2):
#     starttime = time.time()
#     indata = struct.unpack('<h',data[i:i + 2])[0]
#     realitylist, ddolist = DR.input(indata)
#     print('t:',time.time() - starttime)
#     DR.printinfo(realitylist)
#     
# print('t:',time.time() - chunkprocessstarttime)
#     
# GlobalConfig().printself()   
# f.close()
f = open('log.txt','w')
GlobalConfig().logfunc = f.write

def strmatch(str1, str2):
    return(str1 == str2)

while(1):
    
    data = bytes()
    # read one second data
    print('record started')
    stream.start_stream()
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data += stream.read(CHUNK)
        
    print('record stop')
    stream.stop_stream()
    learnlist = {}
    for i in range(0,len(data),2):
        starttime = time.time()
        indata = struct.unpack('<h',data[i:i + 2])[0]
        realitylist, ddolist = DR.input(indata)
        #print('t:',time.time() - starttime)
        DR.printinfo(realitylist)
        
        for el in ddolist:
            learnlist.update({el[1]:el})
     
    learnlistfinal = list(learnlist.values())
    learnlistfinal = sorted(learnlistfinal, key = lambda x:x[1].netpatemp, reverse = True)[0:maxddoforlearning]
    for el in learnlistfinal:
        print('Netpatemp', el[1].netpatemp, ' match%: ', el[0])
        
    
#     print(learnlistfinal)
    reality = input('Reality: ')   
    DR.assignreality(learnlistfinal, reality, strmatch)

rslist = list(DR.RS.keys())
rslist = sorted(rslist, key = lambda x:x.netpatemp, reverse = True)

print(len(rslist))

for i in range(0, 10):
    print(i,': ',rslist[i].netpatemp)    
# print(len(data))


f.close()        

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