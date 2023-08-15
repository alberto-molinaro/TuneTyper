import streamlit as st
from toolkit import load_model, generate_values, generate_wav_file
import os.path

def front():

    st.header("Tune Typer")
    st.subheader("Your Music Creation Assistant")

    st.write("")

    st.write("This app use the [musicgen model](https://huggingface.co/facebook/musicgen-small) from Meta AI to generate music.")
    st.write("A special thank to [Meta AI](https://ai.meta.com/blog/audiocraft-musicgen-audiogen-encodec-generative-ai-audio/) for open-sourcing it!")

    st.subheader("Generate Music")
    cols = st.columns(3)
    with cols[0]:
        music_type = st.selectbox(
            'Music Type',
            ('Electro', 'Disco', 'Pop', 'Rap', 'Rock', 'Jazz', 'Blues'))
        
    with cols[1]:
        rythm = st.selectbox(
            'Rythm',
            ('Chill', 'Dancing', 'Enigmatic', 'Invigorating', 'Rhythmic', 'Enthusiastic', 'Exciting', 'Joyful', 'Soulful', 'Romantic'))

    with cols[2]:
        duration = st.selectbox(
            'Duration',
            ('5 seconds', "10 seconds", "20 seconds", "30 seconds"))
                
    processor, model = load_model()

    if st.button("Generate Music"):
        with st.spinner("Generating sound... This can take 2 minutes..."):
            audio_values = generate_values(model, processor, music_type, rythm, duration)
            generate_wav_file(model, audio_values)
    
    st.subheader("Custom Prompt")

    custom_prompt = st.text_input("Your custom prompt:")
    if st.button("Generate from custom prompt"):
        with st.spinner("Generating sound... This can take 2 minutes..."):
            audio_values = generate_values(model, processor, music_type, rythm, duration, prompt=custom_prompt)
            generate_wav_file(model, audio_values)

    if os.path.exists('musicgen_out.wav'):
        st.audio('musicgen_out.wav', format='audio/wav')

if __name__ == "__main__":
    front()