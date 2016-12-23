#from pydub import AudioSegment
import numpy, scipy, matplotlib.pyplot as plt, sklearn, librosa, mir_eval, urllib
from scipy.io.wavfile import write
from scipy import sparse
from scikits.talkbox.features import mfcc
import os,sys
 
#feature extractor
def extract_features(x):
    ceps, mspec, spec = mfcc(x)
    num_ceps = len(ceps)
    X = []
    X.append(numpy.mean(ceps[int(num_ceps / 10):int(num_ceps * 9 / 10)], axis=0))
    Vx = numpy.array(X)
    return Vx


#These parameters are for testing.
def clusterAudioSegments( syllables, outputPath, outputFileName, fs, k):

    features = numpy.empty((0, 13))
    segments = list()
    #looping through each segmented file
    for syllable in syllables:
        feature = extract_features(syllable)
        features = numpy.vstack((features, feature))
        segments.append(syllable)

    #scale features from -1 to 1
    min_max_scaler = sklearn.preprocessing.MinMaxScaler(feature_range=(-1, 1))
    features_scaled = min_max_scaler.fit_transform(features)

    #DEPRECATED: PYPLOT IS BUGGY? 
    #PyPlot this
    #plt.scatter(features_scaled[:,0], features_scaled[:,1])
    #plt.xlabel('Zero Crossing Rate (scaled)')
    #plt.ylabel('Spectral Centroid (scaled)')
    #plt.show()

    #CHOOSE MODEL BELOW
    #model = sklearn.cluster.MeanShift(bandwidth=None, seeds=None, bin_seeding=False, min_bin_freq=1, cluster_all=True, n_jobs=1)
    #model = sklearn.cluster.KMeans(n_clusters=k)
    model = sklearn.cluster.AffinityPropagation(damping = 0.9)
    labels = model.fit_predict(features_scaled)

    #combine files in cluster
    results = [list() for _ in range(max(labels)+1)] #this is for the output file, to check segmentation
    listOfResults = [list() for _ in range(max(labels)+1)] #this will be a list of audio segments for future use
    padding = 30000 #padding within breaks
    for i in range(features.shape[0]):
        segment_to_attach = numpy.hstack(([0 for _ in range(padding)], segments[i]))
        results[labels[i]] = numpy.hstack((results[labels[i]], segment_to_attach))
        # listofresults are just list of segments for one cluster, for future use by build_final_lexicon
        listOfResults[labels[i]].append(segments[i])

    # output clusters, mostly for debugging purposes
    for i in range(len(results)):
        out_file = outputPath + "/" + outputFileName + "/" + outputFileName + str(i) + ".wav"
        if not os.path.exists(os.path.dirname(out_file)):
                try:
                    os.makedirs(os.path.dirname(out_file))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
        write(out_file, fs, results[i])

    return (labels, listOfResults)
