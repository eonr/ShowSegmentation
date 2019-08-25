# ShowSegmentation
GSoC 2019 project with Red Hen Lab. The goal is to create an algorithm that can automatically find boundaries between TV shows in unannotated recordings, by identifying facial and logo cues of various shows and using binary search to get to the boundary. More information about the project can be found <a href="https://sites.google.com/site/distributedlittleredhen/home/the-cognitive-core-research-topics-in-red-hen/the-barnyard/tv-show-segmentation">here</a>. 

### Blogs detailing weekly progress can be found at <a href="eonr.github.io">eonr.github.io</a>

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
