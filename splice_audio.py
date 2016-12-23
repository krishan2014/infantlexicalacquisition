from pydub import AudioSegment
import numpy, scipy, matplotlib.pyplot as plt, sklearn, librosa, mir_eval, urllib
import os


def splice(audioFile, times):
	audio = AudioSegment.from_wav(audioFile)
	syllables = []
	for i in range(len(times)):
		t = times[i]
		t = t * 1000 #set to milliseconds, might have to drop sig figs
		if i == 0:
			syllables.append(audio[:t])
		else:
			t_prev = times[i - 1] * 1000
			syllables.append(audio[t_prev:t])
			print str(t_prev) + " " + str(t)

		if i == len(times) - 1:
			syllables.append(audio[t:])
	return syllables

def get_times(timeFile):
	times = []
	with open(timeFile) as f:
		for line in f:
			times.append(float(line.strip()))
	return times

def splice_audio(inputDir, inputPathName, onset_times):

	index = 0
	raw_syllables = list()
	#print times
	for filename in os.listdir(inputDir + "/" + inputPathName + '/'):
	    if filename.endswith(".wav"):

		syllables = splice(inputDir + '/' + inputPathName + '/' + filename, onset_times[index])
		
		for i, syllable in enumerate (syllables):
			out_file = "./audio/output/syllables/" + inputPathName + "/" + filename.rstrip('.wav') + "{0}.wav".format(i)
			if not os.path.exists(os.path.dirname(out_file)):
			    try:
			        os.makedirs(os.path.dirname(out_file))
			    except OSError as exc: # Guard against race condition
			        if exc.errno != errno.EEXIST:
			            raise
			syllable.export(out_file, format="wav")
			x, fs = librosa.load(out_file)
			raw_syllables.append(x)

		index += 1

	#return syllables as vector
	return raw_syllables



