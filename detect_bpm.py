import numpy as np
import matplotlib.pyplot as plt

def LPF(data, samplerate, threshold):
    fft = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), 1/samplerate)
    # plt.plot(freqs, fft)
    # plt.show()

    error = 1
    pos_index = int(np.where(np.abs(freqs - threshold) < error)[0][0])
    #print(pos_index)
    neg_index = len(freqs)-pos_index
    #rint(neg_index)

    fft[pos_index+1: neg_index-1] = 0

    # plt.plot(freqs, fft)
    # plt.show()

    filtered_data = np.fft.ifft(fft)
    return filtered_data

def detect_spikes(data):
    spikes = np.zeros(len(data))
    rms_mag = np.max(data) * 0.25

    for i in range(len(data)):
        if data[i] > rms_mag:
            spikes[i] = 1
        else:
            spikes[i] = 0
    return spikes


def calculate_bpm(spike_data, samplerate):
    periods = []
    last_spike_start = 0
    last_read_one = 0
    in_spike = False
    error = 10000

    for i in range(1,len(spike_data)):
        if spike_data[i] == 1:
            last_read_one = i

        if spike_data[i] == 1 and not in_spike and (i-last_spike_start) > error:
            #print("Spike Started")
            in_spike = True
            periods.append(i-last_spike_start)
            last_spike_start = i
        elif spike_data[i] == 0 and in_spike and (i-last_read_one) > error:
            #print("Spike Ended")
            in_spike = False
    
    best_period = np.median(periods)
    bpm = round(60 * samplerate / best_period)

    return bpm

def detect_bpm(data, samplerate):
    f = LPF(data, samplerate, 200)
    f = np.power(f, 2) * 100
    # plt.plot(f)
    spikes = detect_spikes(f)
    # plt.plot(np.multiply(spikes, np.max(f)))
    # plt.show()
    bpm = calculate_bpm(spikes, samplerate)
    return bpm
    # splices_size = round(60*samplerate/bpm)
    # num_splices = len(f)//splices_size
    # splices = [i*splices_size for i in range(num_splices)]





# plt.plot(f)
# for i in range(len(splices)):
#     plt.axvline(x=splices[i], color="r")

# plt.show()
