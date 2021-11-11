import streamlit as st
from PIL import Image, ImageOps
import requests
import io
import json
import numpy as np

local_server = 'http://localhost:5100/predict'
remote_server = 'http://15.165.102.170:5100/predict'

st.sidebar.title("불법복제품 판독 시스템")
st.sidebar.info("Mobile-Demo")

image_files = st.file_uploader('물품 이미지 선택', type=['jpg', 'png', 'bmp', 'jpeg'], accept_multiple_files=True)
cached_images = {}
models = ["supervised", "unsupervised"]

if len(image_files) != 0:
	cols = st.columns(len(image_files))
	for i, img in enumerate(image_files):
		pil_img = Image.open(img).convert('RGB')
		pil_img = ImageOps.exif_transpose(pil_img)
		cached_images[img.name] = np.array(pil_img)
		cols[i].image(pil_img, caption=img.name, width=150)

	choice = st.selectbox('모델 선택', models)
	btn_start = st.button('검사')

	if btn_start:
		file_data = []
		# file_data = {"images": [{img_name: img_arr.tolist()} for img_name, img_arr in cached_images.items()]}
		for img in image_files:
			file_data.append(('images', (img.name, img.getbuffer(), img.type)))

		# file_data.append(("choice", choice))
		st.subheader('결과')
		res = requests.post(remote_server, files=file_data, data={"choice": choice})
		# res = requests.post(local_server, json=json_data)
		result = json.loads(res.content)
		for i, r in enumerate(result):
			st.text(f'top{i+1} 도면번호')
			st.text(r["regNum"])
			st.text(f'top{i+1} 품목명')
			st.text(r["itemName"])
			st.text(f'top{i+1} 유사도')
			st.text(r["similarity"])
