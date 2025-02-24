import numpy as np
import sounddevice as sd

def play_note(note, duration=0.5, volume=0.5):
    """Generate and play a sine wave for a given MIDI note."""
    frequency = 440.0 * (2 ** ((note - 69) / 12.0))  # Convert MIDI note to frequency
    sample_rate = 44100  # Samples per second
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(2 * np.pi * frequency * t) * volume
    sd.play(wave, samplerate=sample_rate)
    sd.wait()

def main():
    rickroll_melody = [
        (76, 0.4), (76, 0.4), (74, 0.4), (76, 0.4), (71, 0.4), (69, 0.8),
        (64, 0.4), (64, 0.4), (69, 0.4), (71, 0.4), (69, 0.4), (64, 0.8),
        (76, 0.4), (76, 0.4), (74, 0.4), (76, 0.4), (71, 0.4), (69, 0.8),
        (64, 0.4), (64, 0.4), (69, 0.4), (71, 0.4), (69, 0.4), (64, 0.8),
        (71, 0.4), (71, 0.4), (69, 0.4), (71, 0.4), (64, 0.4), (62, 0.8),
        (57, 0.4), (57, 0.4), (62, 0.4), (64, 0.4), (62, 0.4), (57, 0.8)
    ]
 #it doesnt even sound great
    for note, duration in rickroll_melody:
        play_note(note, duration)

if __name__ == "__main__":
    main()
