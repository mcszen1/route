import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import numpy as np

class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")

        # Processamento de imagem aqui
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 3)

        return image

st.title("Detecção de Linhas em Tempo Real")

# Iniciando o processamento de vídeo
webrtc_streamer(key="example",
                video_transformer_factory=VideoTransformer,
                media_stream_constraints={
                    "video": {
                        "width": {"ideal": 320},
                        "height": {"ideal": 240},
                        "frameRate": {"ideal": 15}
                    }
                },
                )
