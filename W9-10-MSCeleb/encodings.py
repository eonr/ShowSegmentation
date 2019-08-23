import os
import face_recognition
import numpy as np
import pandas as pd 
from tqdm import tqdm_notebook as tqdm
import pickle
from os.path import join
root = ''
output_path = ''
celebs = sorted(os.listdir(root))[1:]
encodings = []

def load_pickle(filename):
    infile = open(filename,'rb')
    x = pickle.load(infile)
    infile.close()
    return x

def store_pickle(filename, data):
    file = open(filename,'wb')
    pickle.dump(data, file)
    file.close()

# On the cluster:
#   finish knowledge graph api fetching names
#   read the csv and rename all directories with their celeb name
#   
for celeb in celebs:
    #TODO: GET LARGEST IMAGES
    image_paths = os.listdir(os.path.join(root,celeb))[:5]
    encodings.append([])
    for path in image_paths:
        img = face_recognition.load_image_file(os.path.join(root, celeb, path))
        bboxes = face_recognition.face_locations(img,model='hog') #TODO: Test if works well else take cnn
        enc = face_recognition.face_encodings(img, bboxes)
        encodings[-1].append(enc[0]) #0th value for 1st face - maybe more than 1 face?

store_pickle(output_path, (celebs, encodings))

#TODO: KNN
# convert (celebs, encodings) data into the format required by KNN
# Fill KNN space with encodings of all celebs before looping over all faces
def face2name(face_img):
    # get encodings of face_img
    # pass it through KNN and infer
    # return the found name
    

