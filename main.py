import streamlit as st
from read_doc import read_doc
from open_ai import prompt_open_ai

st.set_page_config(layout="wide")
col1, col2 = st.columns([2,1])

   
response_short = ""
response_long = ""

with col1:
  
    uploaded_file  = st.file_uploader("Upload a file")

    if uploaded_file is not None:
        section_paragraph = read_doc(uploaded_file)
        titles = [i for i in section_paragraph.keys()]

        option = st.selectbox(
            'Paragraphs identified',
            (titles))

        st.write(section_paragraph[option])

        text_input_long = st.text_area('OpenAI Long Shot')

        if st.button('Long Shot') and option is not None and text_input_long is not None:
            response_long = prompt_open_ai(text_input_long, section_paragraph[option])
        
        if response_long is not None:
            st.markdown(response_long)

    else:
        st.write('Please upload a documet')

with col2:

    if uploaded_file is not None:
        text_input_short = st.text_input('OpenAI Short Shot')       

        if st.button('Short Shot') and option is not None and text_input_short is not None:
            response_short = prompt_open_ai(text_input_short, section_paragraph[option])

        if response_short is not None:
            st.markdown(response_short)