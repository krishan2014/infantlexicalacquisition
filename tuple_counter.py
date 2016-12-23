import collections

#INPUT: a list of integers, each number representing each k-means cluster assignmnet
def tuple_counter(segmentClusters):
	pairCount = collections.Counter() #number of occurences for each pair of words
	for i in range(len(segmentClusters)-1):
		thisAssign = (segmentClusters[i], segmentClusters[i+1]) #this tuple
		pairCount[thisAssign] += 1 #count 

	print("Sum of pairCOunt is", sum(pairCount.values()))
	#devide number of occurances by total number of occurances
	transProb = {k: float(v) / (sum(pairCount.values())) for k, v in pairCount.items()} 
	print("Final value of transProb is ", transProb)
	return transProb
