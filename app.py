import streamlit as st
st.set_page_config()

from toolkit import load_model, generate_values, generate_wav_file
import os.path
from pydub import AudioSegment

def front():

    # Sidebar 
    with st.sidebar:

        st.title("Tune Typer")
        st.header("Your Music Creation Assistant")
        st.write("")
        st.write("This app use the [musicgen model](https://huggingface.co/facebook/musicgen-small) from Meta AI to generate music.")
        st.write("Audiocraft: [Meta AI](https://ai.meta.com/blog/audiocraft-musicgen-audiogen-encodec-generative-ai-audio/)")

        # Define audio duration
        st.write("**Audio duration:**")
        duration = st.selectbox(
            'Duration',
            ('5 seconds', "10 seconds", "20 seconds", "30 seconds"))

    # Front 
    st.header("Generate Music")
    
    # Column 1 
    cols = st.columns(2)
    with cols[0]:
        music_type = st.selectbox(
            'Music Type',
            ('Electro', 'Disco', 'Pop', 'Rap', 'Rock', 'Jazz', 'Blues'))
        
    # Column 2
    with cols[1]:
        rythm = st.selectbox(
            'Rythm',
            ('Chill', 'Dancing', 'Enigmatic', 'Invigorating', 'Rhythmic', 'Enthusiastic', 'Exciting', 'Joyful', 'Soulful', 'Romantic'))
                
    # Load model
    processor, model = load_model()

    # Button generate from existing prompt
    if st.button("Generate Music", 
                 type='primary'):
        with st.spinner("Generating sound... This can take 2 minutes..."):
            audio_values = generate_values(model, processor, music_type, rythm, duration)
            generate_wav_file(model, audio_values)
    
    # Button generate from custom prompt
    st.header("Custom Prompt")
    custom_prompt = st.text_input("Your custom prompt:")
    if st.button("Generate from custom prompt",
                 type='primary'):
        with st.spinner("Generating sound... This can take 2 minutes..."):
            audio_values = generate_values(model, processor, music_type, rythm, duration, prompt=custom_prompt)
            generate_wav_file(model, audio_values)

    # Music player and downloader
    if os.path.exists('musicgen_out.wav'):
        st.audio('musicgen_out.wav', format='audio/wav')

        audio_bytes = open('musicgen_out.wav', 'rb').read()
        st.download_button(data=audio_bytes, 
                           label="Download Music",
                           mime='audio/wav')

# Main
if __name__ == "__main__":
    front()