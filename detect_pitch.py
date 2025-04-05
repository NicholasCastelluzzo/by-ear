import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import csv
import sys

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

def find_freq_from_wav(wav_file: str) -> list:
    data, samplerate = sf.read(wav_file)

    mono_data = data[:,0]

    fft = np.fft.fft(mono_data)
    fft = np.power(fft, 2)
    lp_fft = 10 * np.log10(fft)

    real_lp_fft = lp_fft[:len(lp_fft)//2+1]
    real_lp_fft = [max(val, 0) for val in real_lp_fft]
    

    pot_freqs = np.fft.fftfreq(len(mono_data), 1/samplerate)
    # plt.plot(pot_freqs[:len(pot_freqs)//2+1], real_lp_fft)
    # plt.show()
    pitch_freqs = []
    threshold = 0.9 * np.max(real_lp_fft)
    for i in range(len(real_lp_fft)):
        mag = real_lp_fft[i]
        if mag >= threshold:
            pitch_freqs.append(pot_freqs[i])

    
    return pitch_freqs

def detect_pitches_from_wav(wav_file: str) -> list:
    freqs = find_freq_from_wav(wav_file)
    pitch_dict = create_pitch_dict()
    notes = list({get_note_from_freq(freq, pitch_dict) for freq in freqs})
    return notes

notes = detect_pitches_from_wav("music/CMajor_Test.wav")
print(notes) 
