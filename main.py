import streamlit as st
from pdf2image import convert_from_bytes
from PyPDF2 import PdfFileReader
import base64
import io
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


# Function to split PDF into pages and convert to base64 images
def split_pdf_to_base64(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    base64_images = []
    for image in images:
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        base64_images.append(img_str)
    return base64_images

# Function to convert PDF pages to markdown
def analyze_pdf_pages(base64_images, system_prompt, analysis_goals):
    combined_text = "# Output\n\n"
    for index, image in enumerate(base64_images):
        prompt = f"""{system_prompt}
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [{"type": "text", "text": "Please convert this image to markdown text. Do not include a code block around the markdown, only include markdown. If there are tables please make sure to convert them to markdown tables. If there are pictures summarize them as you would for an aria label. Please begin now with this image:"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}]}
            ]
        )
        combined_text += f"\n\n{response.choices[0].message.content}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [{"type": "text", "text": "Please analyze the following markdown text to provide insights based on the following analysis goals:"}, {"type": "text", "text": analysis_goals}, {"type": "text", "text": "Please return the analysis as a brief essay of at most 3 paragraphs in markdown format. Do not include a code block around the markdown, only include markdown."}, {"type": "text", "text": combined_text}]}
        ]
    )
    analysis = response.choices[0].message.content
    return combined_text, analysis

# Streamlit app
st.title("Application Reader")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
analysis_goals = st.text_input("Analysis Goals")

if uploaded_file is not None and analysis_goals:
    pdf_bytes = uploaded_file.read()
    
    st.write("Splitting PDF into pages and converting to base64 images...")
    base64_images = split_pdf_to_base64(pdf_bytes)
    
    st.write(f"Total pages converted: {len(base64_images)}")
    
    system_prompt = "You are an expert Legal analyst assisting with analyzing application documents."

    st.write("Analyzing PDF pages...")
    text, analysis = analyze_pdf_pages(base64_images, system_prompt, analysis_goals)
    
    st.write("Text Collection and Analysis Complete!")
    st.markdown(text)

    # Option to download the text
    st.download_button("Download Text", text, file_name="text.md")

    st.header("Notes")
    st.markdown(analysis)

    # Option to download the analysis
    st.download_button("Download Analysis", analysis, file_name="analysis.md")



