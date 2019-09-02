import pickle
import time as tm
import cv2
def loadPickle(filename):
    infile = open(filename,'rb')
    return pickle.load(infile, encoding='latin1')

def storePickle(filename, data):
    file = open(filename,'wb')
    pickle.dump(data, file)
    file.close() 

def sec2HMS(seconds):
    return tm.strftime('%H:%M:%S', tm.gmtime(seconds))

def HMS2sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def getMetadata(vid_path):
    vcap = cv2.VideoCapture(vid_path)
    vid_width, vid_height = int(vcap.get(3)), int(vcap.get(4))
    vcap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
    vid_duration = int(vcap.get(cv2.CAP_PROP_POS_MSEC)/1000)
    cv2.destroyAllWindows()
    vcap.release()
    return vid_width, vid_height, vid_duration

class Show:
    def __init__(self, hosts, start_time, end_time):
        self.hosts = hosts
        self.start_time = start_time
        self.end_time = end_time