import streamlit as st
from PIL import Image
import requests
import io
import copy
import numpy as np

st.sidebar.title("불법복제품 판독 시스템")
st.sidebar.info("Mobile-Demo")

image_files = st.file_uploader('물품 이미지 선택', type=['jpg', 'png', 'bmp', 'jpeg'], accept_multiple_files=True)
cached_images = {}
image_types = []
models = ["supervised", "unsupervised"]

if len(image_files) != 0:
	cols = st.columns(len(image_files))
	for i, img in enumerate(image_files):
		img_byte_arr = io.BytesIO()
		pil_img = Image.open(img).convert('RGB')
		cached_images[img.name] = np.array(pil_img)
		image_types.append(img.type)
		cols[i].image(pil_img, caption=img.name, width=100)

	choice = st.selectbox('모델 선택', models)
	btn_start = st.button('검사')

	if btn_start:
		json_data = {"images": [{img_name: img_arr.tolist()} for img_name, img_arr in cached_images.items()]}
		json_data["choice"] = choice
		st.subheader('결과')
		res = requests.post('http://localhost:5000/predict', json=json_data)
		st.text_area(res.content)
