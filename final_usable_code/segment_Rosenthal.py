"""
This file is made specifically to work on the Rosenthal dataset present
on the CWRU HPC Cluster.

Recursively works on all .mp4 files present in the CWRU Rosenthal dataset.
"""
import os
from segment_video import segment_video
from os.path import join as join

dataset = '/mnt/rds/redhen/gallina/Rosenthal/'
split   = '/mnt/rds/redhen/gallina/RosenthalSplit/'

for y in os.listdir(dataset):
    for y_m in os.listdir(join(dataset, y)):
        for y_m_d in os.listdir(join(dataset, y, y_m)):
            for video in os.listdir(join(dataset, y, y_m, y_m_d)):
                vid_path    = join(dataset, y, y_m, y_m_d, video)
                output_path = join(split, y, y_m, y_m_d) # Exact same tree structure as Rosenthal/ is to be used in RosenthalSplit/

                if not os.path.exists(output_path): 
                    os.makedirs(output_path) # os.makedirs creates all missing directories in the path recursively

                try:
                    segment_video(vid_path, output_path)
                except:
                    print("Error segmenting {}, possible problems: \n1. Video is too small (<20 minutes)\n2. Video file_name doesn\'t follow the Rosenthal naming convention\n3. Video .txt3 file doesn\'t follow the Rosenthal format\n4. Raise an issue on github if any other error exists".format(video))
