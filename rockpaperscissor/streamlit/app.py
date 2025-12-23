import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from ultralytics import YOLO
import cv2
import av

model = YOLO("best.pt") 

class YOLODetector(VideoProcessorBase):
    def __init__(self):
        self.model = model

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        results = self.model(img, conf=0.5)[0] 

        annotated_img = results.plot()  
        return av.VideoFrame.from_ndarray(annotated_img, format="bgr24")

st.title("rock-paper-scissors")
st.write("Turn on camera to play Rock Paper Scissors!")

webrtc_streamer(
    key="rock-paper-scissors",
    video_processor_factory=YOLODetector,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)