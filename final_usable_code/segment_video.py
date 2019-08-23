import os
import cv2
import face_recognition
import numpy as np
import argparse
from utils import *
from celebDetect import *
from face_utils import *
from show_utils import *

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_video", help = "Path to the input video")
    parser.add_argument("output_path", help = 'Path at which to store the output cuts and their .txt files')
    parser.add_argument('--verbose', help = 'Print verbose statements to check the progress of the program', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    vid_path, output_path, verbose = args.input_video, args.output_path, args.verbose
    
    def _print(text):
        if(verbose):
            print(text)

    _print('Done importing modules')
    if not os.path.exists(output_path):
        _print('Output path doesn\'t exist, making output path directory')
        os.mkdir(output_path)

    _print('Finding all faces present in the video | This step will take a long time (about 1/5th the size of the video)')
    allEncodings = findFaces(vid_path)
    _print('Clustering the faces...')
    face_list, face_encodings = clusterFaces(allEncodings)

    _print('Filtering out shows present in the video')
    shows = getShowIntervals(face_list)
    shows = filterShows(shows)
    _print('{} shows found in the video'.format(len(shows)))
    shows = findHostNames(shows, face_encodings)

    vid_width, vid_height = getMetadata(vid_path)

    filename = os.path.splitext(os.path.basename(vid_path))[0]
    attributes = filename.split('_')
    pulldate, barcode = attributes[0], attributes[3]
    vid_txt3_path = os.path.splitext(vid_path)[0]+'.txt3'
    txt3_subtitles = None

    #common headers for all cuts - default values (to be used if this column is not present in the txt3)
    OVD = 'OVD|'+filename+'.mp4'  
    OID = 'OID|'
    COL = 'COL|Communication Studies Archive, UCLA'
    SRC = 'SRC|Rosenthal Collection, UCLA'
    LAN = 'LAN|ENG'
    LBT = 'LBT|'

    if os.path.exists(vid_txt3_path):
        txt3_lines = open(vid_txt3_path, 'r').read().splitlines()
        
        for i in range(len(txt3_lines)):
            if txt3_lines[i][3]!='|': #Header lines end
                txt3_headers = txt3_lines[:i]
                txt3_subtitles = txt3_lines[i:] #Subtitles' lines start here
                break
                
        for header in txt3_headers:
            if header[:3]=='TOP':
                OVD = 'OVD|'+header[4:]
            elif header[:3]=='UID':
                OID = 'OID|'+header[4:]
            elif header[:3]=='COL':
                COL = header
            elif header[:3]=='SRC':
                SRC = header
            elif header[:3]=='LAN':
                LAN = header
    else:
        _print('.txt3 file not found for the input video, using default values for headers')
    
    #Cutting shows from the main video + making a .txt file for each
    for n_show, show in enumerate(shows):
        _print('Cutting out show no. {} from the video'.format(n_show+1))
        channel = 'unknown-channel' #until the work with IMDb is done
        channel = channel.replace(' ', '_')
        
        main_host = show.hosts[0][0]
        if main_host[1] > 0.45: #If majority predictions are of the same person
            host_name = main_host[0]
        else:
            host_name = 'unknown-host'
    #     host_name = show.hosts[0][0][0]
        host_name = host_name.replace(' ', '_')
        cut_filename = '_'.join((pulldate, barcode, '-'.join((str(n_show+1), str(len(shows)))), channel, host_name))
        cut_path = os.path.join(output_path, cut_filename)
        cut_starttime = (int(max(0, show.start_time - 60))) #using a buffer of 1 minute
                                
        if n_show==len(shows)-1: #last show                            
            cut_endtime = (int(min(show.end_time + 60, vid_duration)))
        else:
            cut_endtime = (int(shows[n_show+1])) #till the start of next show
        
        cut_duration = sec2HMS(cut_endtime - cut_starttime)
        cut_starttime = sec2HMS(cut_starttime)
        
    #     ffmpeg_command = 'ffmpeg -ss {} -t {} -i {} -vcodec copy -acodec copy {}.mp4'.format(cut_starttime, cut_duration, vid_path, cut_path)
    #     os.system(ffmpeg_command)
        
        TOP = 'TOP|'+cut_filename+'.mp4'
        UID = 'UID|' #TODO: Generate UUID in the cluster
        TTL = 'TTL|'
        PID = 'PID|'
        CMT = 'CMT|'
        INF = 'INF|'
        for i, host in enumerate(show.hosts):
            INF += 'probable_host'+str(i+1)+':'+'_'.join([pred[0].replace(' ','-') for pred in host][:5])+'_'
        INF = INF[:-1]        
        DUR = 'DUR|'+cut_duration
        TMS = 'TMS|'+cut_starttime+'-'+sec2HMS(cut_endtime)
        VID = 'VID|{}x{}'.format(vid_width, vid_height)
        
        #initializing with headers
        cut_txt_lines = [TOP, COL, UID, SRC, TTL, PID, CMT, DUR, VID, LAN, LBT, OVD, OID, TMS, INF] 
        
        sub_starttime = pulldate.replace('-','') + cut_starttime.replace(':','')
        sub_endtime = pulldate.replace('-','') + sec2HMS(cut_endtime).replace(':','')
        
        
        if txt3_subtitles:
            for sub_idx in range(len(txt3_subtitles)): #TODO: maybe make the starting time 0 for each?
                curr_sub = txt3_subtitles[sub_idx]
                
                if curr_sub[:14] >= sub_starttime:
                    if curr_sub[:14] <= sub_endtime:
                        cut_txt_lines.append(txt3_subtitles[sub_idx])
                    else:
                        break

        with open(cut_path+'.txt', 'w') as f:
            for line in cut_txt_lines:
                f.write("%s\n" % line)