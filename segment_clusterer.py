#from pydub import AudioSegment
import numpy, scipy, matplotlib.pyplot as plt, sklearn, librosa, mir_eval, urllib
from scipy.io.wavfile import write
import os,sys

#feature extractor
def extract_features(x, fs):
    zcr = librosa.zero_crossings(x).sum()
    energy = scipy.linalg.norm(x)
    return [zcr, energy]

#These parameters are for testing.
#inputpath should be audio/output/self_recorded_files
#inputpathname should be eechunk
#outputpath should be audio/clustered/self_recorded_files
#outputpathname would be eecluster

#def getInputFiles(inputPath, inputPathName):
    

def clusterAudioSegments(inputPath, inputPathName, outputPath, outputFileName, k):

    features = numpy.empty((0, 2))
    segments = list()
    #looping through each segmented file
    for file in os.listdir(inputPath):
        if file.startswith(inputPathName):
            #for each segmented file
            x, fs = librosa.load(inputPath + "/" + file)
            feature = extract_features(x,fs)
            features = numpy.vstack((features, feature))
            segments.append(x)

    #scale features from -1 to 1
    min_max_scaler = sklearn.preprocessing.MinMaxScaler(feature_range=(-1, 1))
    features_scaled = min_max_scaler.fit_transform(features)

    #PyPlot this
    plt.scatter(features_scaled[:,0], features_scaled[:,1])
    plt.xlabel('Zero Crossing Rate (scaled)')
    plt.ylabel('Spectral Centroid (scaled)')
    plt.show()

    #kmeans 

    data = numpy.random.rand(10, 3)
    kmeans = sklearn.cluster.KMeans(n_clusters = 5).fit_predict(data)
    print("Before scaling inertia is ", kmeans)

    data = data + 5
    kmeans = sklearn.cluster.KMeans(n_clusters = 5).fit_predict(data)
    print("after scaling inertia is ", kmeans)



    model = sklearn.cluster.AffinityPropagation()
    kmeansLabels = model.fit_predict(features_scaled)
    print ("Kmeans with k = ", k, " result: ", kmeansLabels)

    '''
    #affinity propogation
    model = sklearn.cluster.AffinityPropagation()
    apLabels = model.fit_predict(features_scaled)
    print ("Affinity propogation result: ", apLabels)
    '''

    #combine files in cluster
    results = [list() for _ in range(k)]
    padding = 1000; #padding within breaks
    for i in range(features.shape[0]):
        segment_to_attach = numpy.hstack(([0 for _ in range(padding)], segments[i]))
        results[kmeansLabels[i]] = numpy.hstack((results[kmeansLabels[i]], segment_to_attach))

    for i in range(k):
        out_file = outputPath + "/" + outputFileName + str(i) + ".wav"
        write(out_file, fs, results[i])


####################
#SCRIPT STARTS HERE#
####################

clusterAudioSegments("audio/input/self_recorded_syllables", "jh", "audio/clustered/self_recorded_syllables", "jhcluster", 3)



