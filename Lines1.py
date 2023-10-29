import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import numpy as np


def callback(frame):
    img = frame.to_ndarray(format="bgr24")

    # Redimensiona a imagem para diminuir a carga de processamento
    img = cv2.resize(img, (320, 240))

    # Aplica o filtro Canny para detecção de bordas
    edges = cv2.Canny(img, 100, 200)
    edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    return av.VideoFrame.from_ndarray(edges_color, format="bgr24")

st.title("Detecção de Linhas em Tempo Real")

# Iniciando o processamento de vídeo
webrtc_streamer(key="example", 
                video_frame_callback=callback,
                media_stream_constraints={
                    "video": {
                        "width": {"ideal": 320},
                        "height": {"ideal": 240},
                        "frameRate": {"ideal": 15}
                    }
                })
