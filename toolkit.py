from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy
import streamlit as st
from typing import Optional
from random import randint

@st.cache_resource
def load_model():

    processor = AutoProcessor.from_pretrained("model")
    model = MusicgenForConditionalGeneration.from_pretrained("model")

    return processor, model

def generate_values(model, 
                    processor, 
                    music_type, 
                    rythm,
                    duration,
                    prompt: Optional[str] = None,
                    ):
    
    if duration == '5 seconds':
        max_new_tokens=256
        
    if duration == '10 seconds':
        max_new_tokens=512
    
    if duration == '20 seconds':
        max_new_tokens=1024
    
    if duration == '30 seconds':
        max_new_tokens=1536
        
    if prompt is not None:
        inputs = processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        )
        audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens)
        return audio_values

    else:
        prompt = f"A {rythm} {music_type} sound."

        inputs = processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        )
        audio_values = model.generate(**inputs, max_new_tokens=max_new_tokens)
        return audio_values

def generate_wav_file(model, audio_values):

    sampling_rate = model.config.audio_encoder.sampling_rate
    scipy.io.wavfile.write(f"musicgen_out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())
