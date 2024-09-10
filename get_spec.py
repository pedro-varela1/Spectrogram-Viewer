# Ethogenesis Lab - 2024

# Script to get the spectrum of a given audio file
# on a given time window

import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import sys
from pydub import AudioSegment
import os


def get_spec(audio_file, start_time, end_time):
    # Load the audio file with pydub
    audio = AudioSegment.from_file(audio_file)

    # Check if the time window is valid
    if end_time <= start_time:
        raise ValueError("End time must be greater than start time")
    if end_time > audio.duration_seconds:
        raise ValueError("End time must be less than the duration of the audio")

    audio = audio[int(start_time*1000):int(end_time*1000)]
    samples = np.array(audio.get_array_of_samples())
    y = samples.astype(np.float32) / np.iinfo(samples.dtype).max

    # Get the spectrum
    D = np.abs(librosa.stft(y, n_fft=512))
    return D

def plot_spec(D, start_time, end_time, output_folder=None):
    # Plot the spectrum
    plt.figure(figsize=(12, 8))
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), y_axis='log', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.tight_layout()
    ticks = plt.gca().get_xticks()
    ticks = ticks[1:-1]
    labels_x = np.linspace(float(start_time), float(end_time), ticks.size)
    labels_x = [f"{label:.2f}" for label in labels_x]
    plt.xticks(ticks, labels_x)
    # Show only frequencies above 128 Hz
    plt.ylim(128, None)
    # Save the plot
    if output_folder is not None:
        spectrogram_path = os.path.join(output_folder, 'spectrum.png')
    else:
        spectrogram_path = 'spectrum.png'
    plt.savefig(spectrogram_path, dpi=300)
    plt.close()
    return spectrogram_path

def main():
    audio_file = sys.argv[1]
    start_time = float(sys.argv[2])
    end_time = float(sys.argv[3])
    D = get_spec(audio_file, start_time, end_time)
    plot_spec(D, start_time, end_time)

if __name__ == '__main__':
    main()
