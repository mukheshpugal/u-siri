import numpy as np
import pyaudio
import sys
import time

# Some constants for setting the PyAudio and the
# Aubio.
BUFFER_SIZE             = 512
CHANNELS                = 1
FORMAT                  = pyaudio.paFloat32
SAMPLE_RATE             = 44100
PERIOD_SIZE_IN_FRAME    = BUFFER_SIZE//2

def main(args):

    mic = pyaudio.PyAudio().open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=PERIOD_SIZE_IN_FRAME)
    maxval = 0
    while True:
    	t1 = time.time()
    	data = mic.read(PERIOD_SIZE_IN_FRAME, exception_on_overflow=False)
    	samples = np.frombuffer(data, dtype=np.float32)[::2]
    	volume = np.sum(samples**2)/len(samples)
    	if maxval < volume:
    		maxval = volume
    	volume = "{:6f}".format(volume)
    	mm = "{:6f}".format(maxval)
    	print(f'{volume} : {mm} : {(time.time() - t1)}')

if __name__ == "__main__": main(sys.argv)