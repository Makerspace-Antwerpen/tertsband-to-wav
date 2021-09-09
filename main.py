#!/usr/bin/env python3

from sys import audit
import numpy as np
import sounddevice as sd
import soundfile as sf
import math

centerFreqs = [20, 25, 32.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000]

samplerate = 48000
tertsPerSecond = 8
samplesPerLine = int(samplerate/tertsPerSecond)

num_lines = sum(1 for line in open('infile.meta'))

totalSamples = num_lines * samplesPerLine
sampleSum = 0
outputList = list()
for line in open('infile.meta'):
    lineVals = line.split("\t")
    freqAmps = list()
    for i in range(len(centerFreqs)):
        freqAmps.append(math.pow(10,float(lineVals[i])/20))
    t =(sampleSum + np.arange(samplesPerLine)) / samplerate
    t = t.reshape(-1, 1)
    sampleSum += samplesPerLine
    freqList = list()
    for i in range(len(centerFreqs)):
        outdata = np.zeros((samplesPerLine,1))
        outdata[:] = freqAmps[i] * np.sin(2 * np.pi * centerFreqs[i] * t)
        freqList.append(outdata)
    lineOutput = np.sum(freqList,axis=0)
    outputList.append(lineOutput)

output = np.concatenate(outputList, axis=0)
# print(output)
audio = output.copy()
audio /= np.max(np.abs(audio), axis=0)
# print(audio.shape)

# sd.play(audio, samplerate=samplerate)
# input()
# sd.stop()
sf.write('test.wav', audio, 48000, 'PCM_24')
