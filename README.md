# ShowSegmentation
GSoC 2019 project with Red Hen Lab. The goal is to create an algorithm that can automatically find boundaries between TV shows in unannotated recordings and also find the names of the shows identified. The final method uses face recognition to find all the faces present in the video and clusters them to group the faces by persons. We then separate anchors/hosts of shows from those persons that are not anchors/hosts using a few rules. All anchors found using this method are named using our custom classifier built on the MS-Celeb dataset. More information about the project statement can be found <a href="https://sites.google.com/site/distributedlittleredhen/home/the-cognitive-core-research-topics-in-red-hen/the-barnyard/tv-show-segmentation">here</a>. 

<b>Mentors:</b> <a href="https://sites.google.com/site/annabonazzi8/">Anna Bonazzi</a>, <a href="https://github.com/saisumit">Sumit Vohra</a>


### Blog detailing the research and working can be found at <a href="https://eonr.github.io">eonr.github.io</a>
<i>You can skip the first 4 weeks if you only want to read about the final product.</i>

## Usage
1. Clone the repo to your machine
```bash
git clone https://www.github.com/eonr/ShowSegmentation
```
2. Install the required python packages using either of these commands
```bash
pip install numpy pandas matplotlib opencv-python scikit-learn face_recognition
``` 

```bash
pip install -r requirements.txt
```
3. Download the anchors-encodings pickle and place it in the mentioned location. <a href="https://drive.google.com/open?id=1AAkCoH1FDuJz4pTOyZv9QCUFPZAHECRI">ShowSegmentation/final_usable_code/final_celeb_detection/final_pickles/anchors-with-TV-encodings.pickle</a>

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

## Singularity Usage
### Setup
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
6. I have made <a href="https://github.com/eonr/ShowSegmentation/blob/master/final_usable_code/segment_video.py">segment_video.py</a> for <b>testing</b> and <a href="https://github.com/eonr/ShowSegmentation/blob/master/final_usable_code/segment_Rosenthal.py">segment_Rosenthal.py</a> for final <b>production</b>. After setup, read the Testing section or the Production section according to the requirement.

### Testing
1. segment_video.py is made to work on a single video file. It takes 3 inputs (in this order)
*  ```path/to/input/video.mp4```
*  ```path/to/output/directory``` (where the output will be stored)
*  ```--verbose``` (an optional flag which will make the program print progress statements like 'done extracting faces', 'done clustering faces' etc.
2. So the main command is of the form
```bash
singularity exec -B /mnt ../segmentation_production.simg python3 segment_video.py {INPUT_VIDEO_PATH} {OUTPUT_PATH} {--verbose}
```
3. The Rosenthal dataset is present at ```/mnt/rds/redhen/gallina/Rosenthal```, we can take some video file from this as our input.
4. An example command for the file ```1998-01/1998-01-01/1998-01-01_0000_US_00019495_V3_VHS50_MB20_H17_WR.mp4``` is
```bash
singularity exec -B /mnt ../segmentation_production.simg python3 segment_video.py /mnt/rds/redhen/gallina/Rosenthal/1998/1998-01/1998-01-01/1998-01-01_0000_US_00019495_V3_VHS50_MB20_H17_WR.mp4 mnt/path/to/output/directory --verbose
```

### Production
1. segment_Rosenthal.py is made to work recursively on all the video files present in ```/mnt/rds/redhen/gallina/Rosenthal/``` and store the outputs in ```/mnt/rds/redhen/gallina/RosenthalSplit/```
2. ```--verbose``` flag mentioned earlier is set to False by default for production.
3. Run the script using
```bash
singularity exec -B /mnt ../segmentation_production.simg python3 segment_Rosenthal.py
```
Please raise an issue if you run into any errors.

## Future work
* Explore subtitle analysis to identify anchor/show names.
* Using IMDb dataset to identify show names from anchors’ names (identified using MSCeleb).
* If possible, replace the current celeb detection method with Azure’s Computer Vision service.
* Currently the most time consuming process in the program is that of going frame by frame and extracting faces. This can be sped up using multi-threading or any other means possible.
