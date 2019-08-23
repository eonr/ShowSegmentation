from utils import loadPickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from collections import Counter
celebs, celeb_encodings = loadPickle('final_celeb_detection/final_pickles/anchors-with-TV-encodings.pickle')
celeb_encodings = np.array([np.array(x) for x in celeb_encodings])

# Populating KNN space with labelled encodings
X = []
Y = []
for i in range(len(celeb_encodings)): #prepare dataset
    for celeb_encoding in celeb_encodings[i]:
        X.append(celeb_encoding)
        Y.append(celebs[i])
    
neigh = KNeighborsClassifier(n_neighbors=30)
neigh.fit(X, Y)

def encoding2name(f_encodings):
        return neigh.predict(f_encodings)

def findHostNames(shows, face_encodings):
    for show in shows:
        hosts = show.hosts.split('&') #getting list of hosts of the show
        hosts = sorted(hosts, key = lambda x: len(face_encodings[int(x)]), reverse=True) #Most occuring anchor is taken as the main anchor
        for i in range(len(hosts)):
            host = hosts[i]
            host_encodings = face_encodings[int(host)]      #Getting all encodings of this host's face
            host_prob_names = Counter(list(encoding2name(host_encodings))) #Getting predictions of all faces
            hosts[i] = [(x,y/len(host_encodings)) for x,y in host_prob_names.most_common()] #sorting the predictions by their frequency
            
        show.hosts = hosts
    
    return shows