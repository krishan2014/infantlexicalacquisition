import numpy, scipy, matplotlib.pyplot as plt, sklearn, librosa, mir_eval, urllib
from scipy.io.wavfile import write
import os

#given the right directory, detect syllable onsets using onset detection function and combine to one file
def create_syllables(inputDir, inputPathName):

	onset_times = list()
	for filename in os.listdir(inputDir + "/" + inputPathName + "/"):
		if filename.endswith(".wav"): #for each .wav file under right directory
	    	
			fullfile = inputDir + "/" + inputPathName + "/" + filename
			x, fs = librosa.load(fullfile)

			librosa.display.waveplot(x, fs) 

			#use onset detection from librosa to detect them
			o_env = librosa.onset.onset_strength(x, sr=fs, detrend = True)
			onset_frames = librosa.onset.onset_detect(x, onset_envelope = o_env)
			this_onset_times = librosa.frames_to_time(onset_frames, sr=fs)
			onset_times.append(this_onset_times)

			#DUMP FROM PRE-UCS
			#onset_samples = librosa.frames_to_samples(onset_frames)
			#librosa.output.times_csv('audio/output/onset_detection/' + inputFileName + '_times.csv', onset_times)
			#x_with_beeps = mir_eval.sonify.clicks(this_onset_times, fs, length=len(x))
			#write("audio/output/syllables/" + inputPathName + '/' + filename + "_with_beeps.wav", fs, x+x_with_beeps)

	# Contains timing data (of when syllable begins / ends)
	return onset_times 
