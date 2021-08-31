import streamlit as st
from PIL import Image
import io


st.sidebar.title("불법복제품 판독 시스템")
st.sidebar.info("Mobile-Demo")

image_files = st.file_uploader('물품 이미지 선택', type=['jpg', 'png', 'bmp'], accept_multiple_files=True)
cached_images = {}
models = ["supervised", "unsupervised"]

if len(image_files) != 0:
	cols = st.columns(len(image_files))
	for i, img in enumerate(image_files):
		cached_images[img.name] = Image.open(img)
		cols[i].image(cached_images[img.name], caption=img.name, width=100)

	choice = st.selectbox('모델 선택', models)
	btn_start = st.button('검사')

	if btn_start:
		st.subheader('결과')

		## get a result on AI-server restful api with a model choice and display it