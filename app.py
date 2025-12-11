import os
import streamlit as st
from apikey import google_gemini_api_key
import base64
from google import genai
from google.genai import types

def generate(blog_title,keywords,num_words,num_images):
    blog_title=blog_title
    keywords=keywords
    num_words=num_words
    client = genai.Client( api_key=google_gemini_api_key)
    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"Generate a comprehensive, engaging blog post relevant to the given title {blog_title} and keywords {keywords}. Make sure to incorporate these keywords in blog post The blog should be approximately {num_words} words in length, suitable for an online audience. Ensure the content is original, informative and maintains a consistent tone throughout."),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.9,
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        tools=tools,)

    stream = client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,)
    
    full_text = ""
    
    

    #for n, generated_image in enumerate(result.generated_images):
     #   generated_image.image.save(f"generated_image_{n}.jpg")


    for chunk in stream:
        if chunk.text:
            full_text+=chunk.text
    return full_text

def generate_img(blog_title,keywords):
        
        client = genai.Client( api_key=google_gemini_api_key)

        result = client.models.generate_content(
        model="gemini-2.5-flash-image",
    
        contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"Generate Image on the theme of {blog_title} and must has relevance with {keywords}"),
            ],
        ),
    ],
    #generate_content_config = types.GenerateContentConfig(
     #   response_modalities=[
      #      "IMAGE",
       #     "TEXT",
        #],
    )

        
        for part in result.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                return part.inline_data.data  # <-- ✔ raw bytes for st.image()

        return None




st.set_page_config(layout="wide")

st.title('BlogCraft',text_alignment="center")

st.subheader('Craft your blog using BlogCraft',text_alignment="center")

with st.sidebar:
    st.title("Input Your Blog Details")
    st.subheader("Enter details of Blog you want to generate")

    blog_title = st.text_input("Blog Title")

    keywords = st.text_area("Keywords (comma-separated)")

    num_words = st.slider("Number Of Words",min_value=250,max_value=1000,step=250)

    num_images = st.number_input("Number Of Images", min_value=0, max_value=5, step=1)

    submit_button = st.button("Generate Blog")


if submit_button:
    images=[]
    for i in range(num_images):
        img = generate_img(blog_title,keywords)
        images.append(img)
    for img in images:
        st.image(img)

    if not blog_title or not keywords:
        st.error("Please fill all inputs before generating.")
    else:
        with st.spinner("Crafting your blog..."):
            blog = generate(blog_title, keywords, num_words,num_images)
        st.success("Blog generated successfully!")
        st.write(blog)
        
    









    
    
    

