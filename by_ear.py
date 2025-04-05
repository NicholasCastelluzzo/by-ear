import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import csv
import sys
import os
import re

import detect_bpm
import detect_pitch

def remove_useless_rests(beat_pitches):
    while not beat_pitches[0]:
        beat_pitches = beat_pitches[1:]
    while not beat_pitches[-1]:
        beat_pitches = beat_pitches[:-1]
    return beat_pitches

def notate_rests(beat_pitches):
    for i in range(len(beat_pitches)):
        if not beat_pitches[i]:
            beat_pitches[i].append("R")
    return beat_pitches

def calc_durations(beat_pitches, energies):
    last_beat_start = 0
    curr_dur = 1
    durations = [0]*len(energies)
    #print(len(energies), len(beat_pitches))
    for i in range(len(energies)):
        if set(beat_pitches[last_beat_start]) == set(beat_pitches[i]) and energies[i] <= energies[last_beat_start] * 0.33:
            curr_dur +=1
            continue
        else:
            durations[last_beat_start] = curr_dur
            last_beat_start = i
            curr_dur = 1
    if curr_dur:
        durations[last_beat_start] = curr_dur
    
    return durations


if len(sys.argv) != 2:
    print("Usage: python ./parse_music <music_file>")
    exit(-1)

music_file = sys.argv[1]
data, samplerate = sf.read(music_file, always_2d=True)
mono_data = data[:,0]

bpm = detect_bpm.detect_bpm(mono_data, samplerate)
#print(bpm)

splices_size = round(60*samplerate/bpm)
num_splices = len(mono_data)//splices_size
splices = [i*splices_size for i in range(num_splices+1)]
plt.plot(mono_data)
for i in range(len(splices)):
    plt.axvline(x=splices[i], color="r")
plt.show()

beat_pitches = []
energies = []
for i in range(1, num_splices+1):
    spliced = mono_data[(i-1)*splices_size : i*splices_size]
    # plt.plot(spliced)
    # plt.ylim(0, 1)
    # plt.show()
    beat_pitches.append(detect_pitch.detect_pitches(spliced, samplerate))
    energies.append(detect_pitch.calc_avg_energy(spliced))
    energy = detect_pitch.calc_avg_energy(spliced)
    # plt.plot(spliced)
    # plt.axhline(y=0.6, color="r")
    # plt.axhline(y=energy, color="g")
    # plt.axhline(y=0.01, color="y")
    # plt.show()

beat_pitches = remove_useless_rests(beat_pitches)
beat_pitches = notate_rests(beat_pitches)
#print(beat_pitches)
energies = remove_useless_rests(energies)
#print(energies)


sum_octaves = 0
num_octaves = 0
for beat in beat_pitches:
    for pitch in beat:
        sum_octaves += detect_pitch.get_octave(pitch)
        num_octaves += 1

avg_octave = round(sum_octaves/num_octaves)
#print(beat_pitches)
beat_pitches = [[pitch[:-1]+str(avg_octave) for pitch in beat] for beat in beat_pitches]
#print(beat_pitches)

durations = calc_durations(beat_pitches, energies)
#print(durations)

file_name_no_extension = re.sub(r"[.][^\/\\]*$", "", music_file)
file_name_no_extension = re.sub(r".*[\\\/]", "", file_name_no_extension)
print(file_name_no_extension)
save_directory = "temp/"
os.makedirs(save_directory, exist_ok=True)
new_file_name = save_directory + file_name_no_extension + ".music"


MEASURES_PER_LINE = 4
BEATS_PER_MEASURE = 4
with open(new_file_name, "w") as file:
    file.write("T 4/4 Q=" + str(bpm) + "\n")
    total_beats = len(beat_pitches)
    total_measures = total_beats//BEATS_PER_MEASURE
    total_lines = total_measures//MEASURES_PER_LINE

    for line in range(total_lines):
        for measure in range(MEASURES_PER_LINE):
            for beat in range(BEATS_PER_MEASURE):
                beat_index = beat+measure*BEATS_PER_MEASURE+line*MEASURES_PER_LINE*BEATS_PER_MEASURE

                pitch_list = beat_pitches[beat_index]
                for pitch_index in range(len(pitch_list)):
                    duration = durations[beat_index]
                    if duration == 0:
                        continue
                    pitch = pitch_list[pitch_index]
                    file.write(pitch + ":" + str(duration))
                    if pitch_index != len(pitch_list)-1:
                        file.write(",")
                if beat != BEATS_PER_MEASURE-1:
                    file.write(";")
            if measure != MEASURES_PER_LINE-1:
                file.write("|")
        file.write("\n")


with open(new_file_name, "r+") as file:
    data = file.read()
    data = re.sub("[;]+", ";", data)
    file.seek(0)
    file.write(data)
    file.truncate()
