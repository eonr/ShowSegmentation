# ShowSegmentation
GSoC 2019 project with Red Hen Lab. The goal is to create an algorithm that can automatically find boundaries between TV shows in unannotated recordings and also find the names of the shows identified. The final method uses face recognition to find all the faces present in the video and clusters them to group the faces by persons. We then separate anchors/hosts of shows from those persons that are not anchors/hosts using a few rules. All anchors found using this method are named using our custom classifier built on the MS-Celeb dataset. More information about the project can be found <a href="https://sites.google.com/site/distributedlittleredhen/home/the-cognitive-core-research-topics-in-red-hen/the-barnyard/tv-show-segmentation">here</a>. 

### Blogs detailing weekly progress can be found at <a href="https://eonr.github.io">eonr.github.io</a>

## Usage:
1. Clone the repo to your machine
```bash
git clone https://www.github.com/eonr/ShowSegmentation
```
2. Install the required python packages
```bash
pip install numpy pandas matplotlib opencv-python scikit-learn face_recognition
```
3. Download the anchors-encodings pickle and place it in the mentioned location. <a href="https://drive.google.com/open?id=1AAkCoH1FDuJz4pTOyZv9QCUFPZAHECRI">ShowSegmentation/final_usable_code/final_pickles/anchors-with-TV-encodings.pickle</a>

4. Navigate to ShowSegmentation/final_usable_code/
```bash
cd ShowSegmentation/final_usable_code
```
5. segment_video.py takes 3 inputs, the path to the input video, path to the output location and a flag --verbose.
```python
python3 segment_video.py path/to/input/video.mp4 path/to/store/output --verbose
```
6. Make sure that the input video's name follows RedHenLab's Rosenthal dataset's format. Here's an example
```
1980-06-03_0000_US_00020088_V0_U2_M9_EG1_DB.mp4
```

## Singularity Usage:
<i> **This is for those using the singularity image (segmentation_production.simg) on the CWRU HPC Cluster.</i>
1. Connect to the <a href="https://vpnsetup.case.edu/">CWR VPN</a>.
2. Login to the cluster using your CWR ID and your credentials. Example:
```bash
ssh abc12@rider.case.edu
```
3. Navigate to the project's location on the cluster.
```bash
cd /mnt/rds/redhen/gallina/Singularity/Show_Segmentation/final_usable_code
```
4. Request a computing node using
```bash
srun --mem=16gb --pty /bin/bash
```
5. Load <a href="http://singularity.lbl.gov/">singularity</a> 2.5.1 to your environment using
```bash
module load singularity/2.5.1
```
6. The singularity file (.simg) takes 3 inputs (in this order)
*  ```path/to/input/video.mp4```
*  ```path/to/output/directory``` (where the output will be stored)
*  ```--verbose``` (an optional flag which will make the program print progress statements like 'done extracting faces', 'done clustering faces' etc.
7. So the main command is of the form
```bash
singularity exec -B /mnt ../segmentation_production.simg python3 segment_video.py {INPUT_VIDEO_PATH} {OUTPUT_PATH} {--verbose}
```
8. The Rosenthal dataset is present at /mnt/rds/redhen/gallina/Rosenthal, we can take some video file from this as our input.
9. An example command for the file <i>1998-01/1998-01-01/1998-01-01_0000_US_00019495_V3_VHS50_MB20_H17_WR.mp4</i> is
```bash
singularity exec -B /mnt ../segmentation_production.simg python3 segment_video.py /mnt/rds/redhen/gallina/Rosenthal/1998/1998-01/1998-01-01/1998-01-01_0000_US_00019495_V3_VHS50_MB20_H17_WR.mp4 mnt/path/to/output/directory --verbose
```
Please raise an issue if you run into any errors.
