from dotenv import load_dotenv
import os
import io
import base64
load_dotenv()
import streamlit as st
from PIL import Image
import pdf2image

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.txt

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:

        ## converting pdf 2 image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mine_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode

            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
# stramlit app

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_txt=st.text_area("Job Desciption: ",key="input")
uploaded_file=st.file_uploader("Upload your Resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1=st.button("Tell Me About the Resume")

# submit2=st.button("Hpw Can I Improvied My Skills")

submit3=st.button("Percentage match")

input_prompt1="""
you are an expirenced technical human resource Manager your task 
is to review the provide.You are an experienced HR With Tech Experience in the filed of Data Science, Full stack Web development, Big Data Engineering, DEVOPS, Data Analyst, your task is to review the provided resume against the job description for these profiles. Please share your professional evaluation on whether the candidate's profile aligns with
Highlight the strengths and weaknesses of the applicant in relation to the specified job
"""

input_prompt3="""You are an skilled ATS (Applicant Tracking System) scanner with a deep unders your task is to evaluate the resume against the provided job description. giv the job description. 
First the output should come as percentage and then key
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_txt)
        st.subheader("The Response is")
        st.write(response)

    else:
        st.write("please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_txt)
        st.subheader("The Response is")
        st.write(response)

    else:
        st.write("please upload the resume")    
        
            

