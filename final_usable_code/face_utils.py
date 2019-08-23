from utils import *
import face_recognition
import cv2
from sklearn.cluster import DBSCAN
def findFaces(vid_path, skip_seconds=1):
    """ Returns 129D encodings for each face present in the video
        First 128 are the face encodings and the last value is the time.
        
       :param interval: (in seconds) frame interval to skip and look for faces
       :param model: 'hog' is less accurate but faster compared to 'cnn'
       :param store: if True, stores the faces in directory specified by dirName """
    vidcap = cv2.VideoCapture(vid_path)
    cv2.VideoCapture 
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    interval = int(fps+1)*skip_seconds #no. of frames to skip
    # print("FPS of the video: {}".format(fps))
    allEncodings = [] #Dict containing path, box and encoding
    n_frame = 0 # no. of frame being processed

    success, frame = vidcap.read()
    
    while success:
        rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        bboxes = face_recognition.face_locations(rgb,model='hog')
        encodings = face_recognition.face_encodings(rgb,bboxes)
        for i,bbox in enumerate(bboxes): #for each found face in the frame
            # top,right,bottom,left = bbox[0],bbox[1],bbox[2],bbox[3]
            # face_img = frame[top:bottom, left:right]
            
            d = {'time': (n_frame/fps), 'loc': bbox, 'encoding':encodings[i]}
            allEncodings.append(d)
            
        n_frame += interval            
        vidcap.set(cv2.CAP_PROP_POS_FRAMES,n_frame)
        success, frame = vidcap.read()
    
    cv2.destroyAllWindows()
    vidcap.release()
    return allEncodings

def clusterFaces(allEncodings, n_jobs=-1, max_clusters = 100):
    """face_times: a Tuple list with x[0] as face_classes, and x[1] as list of their
    times of occurence in the video.
    
       face_encodings: dict mapping face_class to list of encodings of all occurences 
       of that face in the video"""
    encodings = [d['encoding'] for d in allEncodings]
    times = [d['time'] for d in allEncodings]
    clt = DBSCAN(metric='euclidean', n_jobs=n_jobs, min_samples=5,eps=0.37)
    clt.fit(encodings)
    labels = clt.labels_ #-1 => too small to include in a cluster
    
    face_times = [] #list of tuples, first element is time of occurence, 2nd is the class of the face
    face_encodings = {} #dict mapping from a face_classs to all encodings of that faces (from the images found in the video)
    
    for i,label in enumerate(labels):
        encoding = encodings[i]
        time = times[i]
        if(label!=-1):
            face_times.append((int(time), str(label)))
            
            if label in face_encodings:
                face_encodings[label].append(encoding)
            else:
                face_encodings[label] = [encoding]
    return face_times,face_encodings