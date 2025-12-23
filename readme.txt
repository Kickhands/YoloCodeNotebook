For Study I recommend u watch all of this video 
the video is all of tutorial but after u following the tutorial u will recognise the pattern and easier to understand how to modify your detection

1. Track Video by Python Script ( use yolo12 model )
https://www.youtube.com/watch?v=ISz00D1glPQ

2. Track and Count Video without training use yolo8x 
this version is kinda old so u may change some code like sv.tools and other cause it already non exist
https://youtu.be/OS5qI9YBkfk?si=0I9n7RR-DJX_pOS2

3. Object Counting real time with webcam , this one kinda interesting , and its new in 2025 so u may not find a problem for following 
https://www.youtube.com/watch?v=QV85eYOb7gk&list=PLZCA39VpuaZZJ-aS7B7pZVrD9AtRx8-7u&index=19


## Step run Folder Track & Count main.py
We must create a venv for easier cause py3.12 may cause troble with current package
py -m venv yolo-env
yolo-env\Scripts\activate
pip install ultralytics opencv-python supervision
pip install cvzone --no-cache-dir

for running file just
py namefile.py