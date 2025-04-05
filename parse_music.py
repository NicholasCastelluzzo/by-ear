import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import csv
import sys

import detect_bpm
import detect_pitch

def remove_useless_rests(beat_pitches):
    while not beat_pitches[0]:
        beat_pitches = beat_pitches[1:]
    while not beat_pitches[-1]:
        beat_pitches = beat_pitches[:-1]
    return beat_pitches

if len(sys.argv) != 2:
    print("Usage: python ./parse_music <music_file>")
    exit(-1)

wav_file = sys.argv[1]
data, samplerate = sf.read(wav_file, always_2d=True)
mono_data = data[:,0]

bpm = detect_bpm.detect_bpm(mono_data, samplerate)
print(bpm)

splices_size = round(60*samplerate/bpm)
num_splices = len(mono_data)//splices_size
splices = [i*splices_size for i in range(num_splices+1)]
plt.plot(mono_data)
for i in range(len(splices)):
    plt.axvline(x=splices[i], color="r")
plt.show()

print(num_splices+1)
beat_pitches = []
for i in range(1, num_splices+1):
    spliced = mono_data[(i-1)*splices_size : i*splices_size]
    # plt.plot(spliced)
    # plt.ylim(0, 1)
    # plt.show()
    beat_pitches.append(detect_pitch.detect_pitches(spliced, samplerate))

beat_pitches = remove_useless_rests(beat_pitches)

sum_octaves = 0
num_octaves = 0
for beat in beat_pitches:
    for pitch in beat:
        sum_octaves += detect_pitch.get_octave(pitch)
        num_octaves += 1

avg_octave = round(sum_octaves/num_octaves)
print(beat_pitches)
beat_pitches = [[pitch[:-1]+str(avg_octave) for pitch in beat] for beat in beat_pitches]
print(beat_pitches)

