import os
import gradio as gr #type:ignore
from fastapi import FastAPI #type:ignore
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI  #type:ignore
from langchain_core.prompts import ChatPromptTemplate  #type:ignore
from gtts import gTTS  #type:ignore

load_dotenv()

# --- 1. Initialize FastAPI ---
app = FastAPI(title="AI Storyteller Backend", version="1.0.0")

# --- 2. Logic (Backend) ---
def generate_story_and_audio(topic, tone):
    try:
        # Use Gemini 2.5 Flash for speed and free-tier access
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        prompt = ChatPromptTemplate.from_template("Write a short {tone} story about {topic}. Max 150 words.")
        chain = prompt | llm
        
        story_text = chain.invoke({"topic": topic, "tone": tone}).content
        audio_filename = "story.mp3"
        gTTS(text=story_text, lang='en').save(audio_filename)
        
        return story_text, audio_filename
    except Exception as e:
        return f"Error: {str(e)}", None

# --- 3. Professional UI (Gradio) ---
custom_css = ".gradio-container {background: linear-gradient(135deg, #0f0c29 0%, #302b63 100%) !important;}"

with gr.Blocks() as demo: 
    gr.HTML("<h1 style='color:white; text-align:center;'>🌌 AI Persona Storyteller</h1>")
    with gr.Row():
        with gr.Column():
            topic = gr.Textbox(label="Topic", placeholder="e.g., A detective in 2077...")
            tone = gr.Radio(["Epic", "Mysterious", "Funny", "Spooky"], label="Tone", value="Epic")
            btn = gr.Button("Generate Narrative ✨", variant="primary")
        with gr.Column():
            out_text = gr.Textbox(label="The Story", lines=10)
            out_audio = gr.Audio(label="Audio Output", type="filepath")
    btn.click(generate_story_and_audio, inputs=[topic, tone], outputs=[out_text, out_audio])

# --- 4. Mount Gradio into FastAPI ---
# This is the industry-standard way to serve Gradio with a custom backend
app = gr.mount_gradio_app(
    app, 
    demo, 
    path="/",
    # Pass the theme and css here for Gradio 6 compatibility
    theme=gr.themes.Glass(primary_hue="cyan"),
    css=custom_css 
)

if __name__ == "__main__":
    import uvicorn #type:ignore
    # Port 7860 is the Gradio default, but FastAPI can use 8000
    uvicorn.run(app, host="0.0.0.0", port=7860)