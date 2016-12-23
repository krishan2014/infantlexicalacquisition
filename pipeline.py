#this scripts run every step that's required, given input audio
import create_syllables
import mfcc_clusterer
import splice_audio
import tuple_counter
import word_segmenter  
import dictionary_builder
import ucs_word_segmenter
import build_final_lexicon

inputDir = 'audio/input/multisyllabic'
inputPathName = 'multisyllabic_numWords2'

#detect syllables
print "Running onset detection..."
onset_times = create_syllables.create_syllables(inputDir, inputPathName)

#splice audio by syllable
print "Splicing Audio File..."
syllables = splice_audio.splice_audio(inputDir, inputPathName, onset_times)

#cluster syllables
print "Clustering syllables..." 
labels, segResults = mfcc_clusterer.clusterAudioSegments(syllables, "audio/clustered/syllables", inputPathName, 22050, 12) #k number is arbitrary for now
labelsTuple = tuple(labels.tolist())

#create dictionary of costs, a.e. how often each syllable combination occurs
#print "Creating dictionary..."
#cost_dictionary = dictionary_builder.dictionary_builder(labelsTuple, 4)

#run ucs based on the cost dictionary above, segment audio into appropriate parts
#print "Running ucs..."
#word_sequence = ucs_word_segmenter.segmentWord(labelsTuple, cost_dictionary, 4)

# use ucs action data to re-build the final lexicon
#print "Building final lexicon..."
#lexicon = build_final_lexicon.build_final_lexicon(word_sequence)

#referencing final lexicon, create example audio segments using randomly sampled syllable audio from each cluster
#build_final_lexicon.generate_word_audio(segResults, 5, lexicon, 10, "audio/clustered/words/ucs", inputPathName, 22050)


#PROCESS BEFORE UCS WAS IMPLEMENTED
transProb = tuple_counter.tuple_counter(labels)
words = word_segmenter.word_segmenter(syllables, labels, transProb, 0.01)
wordClusters = mfcc_clusterer.clusterAudioSegments(words, "audio/clustered/words", inputPathName, 22050, 6)

