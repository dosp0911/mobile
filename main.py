import streamlit as st
from PIL import Image
import requests
import io
import json
import numpy as np

local_server = 'http://localhost:5100/predict'
remote_server = 'http://125.132.250.102:5100/predict'

st.sidebar.title("불법복제품 판독 시스템")
st.sidebar.info("Mobile-Demo")

image_files = st.file_uploader('물품 이미지 선택', type=['jpg', 'png', 'bmp', 'jpeg'], accept_multiple_files=True)
cached_images = {}
models = ["supervised", "unsupervised"]

if len(image_files) != 0:
	cols = st.columns(len(image_files))
	for i, img in enumerate(image_files):
		pil_img = Image.open(img).convert('RGB')
		cached_images[img.name] = np.array(pil_img)
		cols[i].image(pil_img, caption=img.name, width=100)

	choice = st.selectbox('모델 선택', models)
	btn_start = st.button('검사')

	if btn_start:
		json_data = {"images": [{img_name: img_arr.tolist()} for img_name, img_arr in cached_images.items()]}
		json_data["choice"] = choice
		st.subheader('결과')
		res = requests.post(remote_server, json=json_data)
		# res = requests.post(local_server, json=json_data)
		result = json.loads(res.content)
		st.text('top3 Registration Number')
		st.text(result["top3-reg-nums"])
		st.text('detail info')
		st.text(result["details"])
