import collections
from math import log 

#given a list of segment assignments
#build a dictionary of all possible word combinations and its likeliness
#maxSyllableLength is how much syllables in a word max are we assuming?
def dictionary_builder(labels, maxSyllableLength):

	dictionary = collections.Counter() #number of occurences for each collection of words
	for i in range(len(labels)):
		for j in range(maxSyllableLength):
			if((i+j+1) < len(labels)):
				subSeg = labels[i:i+j+1]
				dictionary[subSeg] += 1


	totalOccur = sum(dictionary.values())
	#processing to turn into cost 
	for key in dictionary: 
		# The cost is 1 over probability of occurence * log(length of key)
		# Occurs more often = lest cost
		# longer = less cost
		dictionary[key] = 1/((dictionary[key]/float(totalOccur))*log(len(key)+0.2)) #the constant 0.2 is arbitrary
	return dictionary

