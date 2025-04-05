import numpy as np
import matplotlib.pyplot as plt
import csv
import sys

def get_octave(note: str):
    for char in note:
        if char.isnumeric():
            return int(char)
        
def get_pitch(note: str):
    return note[:-1]

def remove_higher_octaves(notes):
    lowest_octaves = {}

    for note in notes:
        pitch = get_pitch(note)
        octave = get_octave(note)
        if pitch not in lowest_octaves:
            lowest_octaves[pitch] = octave
        elif pitch in lowest_octaves and octave < lowest_octaves[pitch]:
            lowest_octaves[pitch] = octave

    #print(lowest_octaves)
    for i in range(len(notes)-1, -1, -1):
        note = notes[i]
        pitch = get_pitch(note)
        octave = get_octave(note)
        #print(note, pitch, octave)
        if lowest_octaves[pitch] != octave:
            notes.pop(i)
    
    return notes

def calc_avg_energy(data):
    n = len(data)
    data = np.power(data, 2)
    data = np.sum(data)
    energy = data / n * 100
    if energy < 0.01:
        energy = 0
    return energy

def get_is_rest(data):
    e = calc_avg_energy(data)
    if e < 0.01:
        return 1
    else:
        return 0


def create_pitch_dict() -> dict:
    pitch_data = csv.DictReader(open("pitch_chart.csv"))
    pitch_dict = {}
    for pitch_row in pitch_data:
        pitch = pitch_row['']
        pitch_row.pop('')
        for (octave, freq) in pitch_row.items():
            pitch_dict[float(freq)] = pitch+octave
    return pitch_dict

def get_note_from_freq(freq: float, pitch_dict: dict) -> str:
    min_dist = sys.float_info.max
    closest_freq = None

    for curr_freq in pitch_dict.keys():
        dist = np.abs(curr_freq - freq)
        if dist < min_dist:
            min_dist = dist
            closest_freq = curr_freq

    if closest_freq and closest_freq in pitch_dict.keys():
        return pitch_dict[closest_freq]

    return None

def find_freqs(data, samplerate) -> list:
    if get_is_rest(data):
        return []
    fft = np.fft.fft(data)
    fft = np.power(fft, 2)
    lp_fft = 10 * np.log10(fft)

    real_lp_fft = lp_fft[:len(lp_fft)//2+1]
    real_lp_fft = [max(val, 0) for val in real_lp_fft]
    

    pot_freqs = np.fft.fftfreq(len(data), 1/samplerate)
    # plt.plot(pot_freqs[:len(pot_freqs)//2+1], real_lp_fft)
    # plt.show()
    pitch_freqs = []
    threshold = 0.99 * np.max(real_lp_fft)
    for i in range(len(real_lp_fft)):
        mag = real_lp_fft[i]
        if mag >= threshold:
            pitch_freqs.append(pot_freqs[i])

    
    return pitch_freqs

def detect_pitches(data, samplerate) -> list:
    freqs = find_freqs(data, samplerate)
    pitch_dict = create_pitch_dict()
    notes = list({get_note_from_freq(freq, pitch_dict) for freq in freqs})
    notes = remove_higher_octaves(notes)
    return notes

# notes = detect_pitches_from_wav("music/Mary_Had_A_Little_Lamb.mp3")
# print(notes) 
