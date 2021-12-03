import streamlit as st

from PIL import Image, ImageOps
import requests
import io
import json
import numpy as np
import pandas as pd

# port_num = 5100 # mobile
port_num = 5200 # demo
# server = f'http://localhost:{port_num}'
server = f'http://15.165.102.170:{port_num}'

st.header('불법복제품 판독 시스템 Demo')
st.sidebar.title("불법복제품 판독 시스템")
st.sidebar.info("Mobile-Demo")
select_menu = st.sidebar.selectbox("", ["검사", "물품 추가/삭제"])
items = json.loads(requests.get(server + '/list').content)["items"]

def check_name(item_name):
	if item_name.lstrip().lower() not in items:
		return True
	return False

def remove_item(item_names):
	res = requests.post(server + '/delete',
	                   json={'itemNames': [i.lstrip().lower() for i in item_names]})

	return res.content

def add_item(itemName, image_files):
	file_data = []
	for img in image_files:
		file_data.append(('images', (img.name, img.getbuffer(), img.type)))
	res = requests.post(server + '/add', files=file_data, data={"itemName": itemName})
	return res.content

if select_menu == "물품 추가/삭제":
	st.subheader('물품 추가')
	add_item_name = st.text_input('물품명')
	if add_item_name.lstrip() != "":
		if check_name(add_item_name):
			st.success(f'{add_item_name} 사용 가능')
			add_item_images = st.file_uploader('추가', type=['jpg', 'png', 'bmp', 'jpeg'], accept_multiple_files=True)
			if len(add_item_images) != 0:
				cols = st.columns(len(add_item_images))
				for i, img in enumerate(add_item_images):
					pil_img = Image.open(img).convert('RGB')
					pil_img = ImageOps.exif_transpose(pil_img)
					cols[i].image(pil_img, caption=img.name, width=150)
				is_add = st.button('추가')
				if is_add:
					res = add_item(add_item_name, add_item_images)
					st.success("추가되었습니다.")
		else:
			st.warning(f'{add_item_name} 이미 존재합니다')

	st.subheader('물품 삭제')
	choices = st.multiselect('삭제', items)
	if len(choices) != 0:
		is_delete = st.button('삭제')
		if is_delete:
			res = remove_item(choices)
			st.success(res)
			items = json.loads(requests.get(server + '/list').content)["items"]

if select_menu == "검사":
	st.subheader('보유 품목')
	df = st.table(items)

	st.subheader('검사')
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

		# choice = st.selectbox('모델 선택', models)
		choice = models[1]
		btn_start = st.button('검사')

		if btn_start:
			file_data = []
			for img in image_files:
				file_data.append(('images', (img.name, img.getbuffer(), img.type)))

			st.subheader('결과')
			res = requests.post(server + '/predict', files=file_data, data={"choice": choice})
			result = json.loads(res.content)
			pred_items = result["itemNames"]
			for i, n in enumerate(pred_items):
				st.text(f'{i+1}th 품목명: {n}')
				
