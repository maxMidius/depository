import os
from flask import Flask, send_from_directory
from dash import Dash, html, dcc, Input, Output, State
from gtts import gTTS

# Create a Flask server
server = Flask(__name__)

# Create a Dash app
app = Dash(__name__, server=server)

# Directory to save audio files
AUDIO_DIR = "audio"
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

# Serve audio files
@server.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

# Dash layout
app.layout = html.Div([
    html.H1("Text to Speech Converter"),
    dcc.Input(id="text-input", type="text", placeholder="Enter text here", style={"width": "300px"}),
    html.Button("Convert to Speech", id="convert-button"),
    html.Audio(id="audio-player", controls=True, style={"marginTop": "20px"}),
    html.Div(id="output")
])

# Callback to convert text to speech and update audio player
@app.callback(
    Output("audio-player", "src"),
    Output("output", "children"),
    Input("convert-button", "n_clicks"),
    State("text-input", "value")
)
def convert_text_to_speech(n_clicks, text):
    if n_clicks is None or not text:
        return "", "Enter text and click the button to convert to speech."

    # Convert text to speech
    try:
        tts = gTTS(text)
        audio_file = os.path.join(AUDIO_DIR, "speech.mp3")
        tts.save(audio_file)
        print(f"Audio file saved at: {audio_file}")

        # Verify the file exists and is not empty
        if os.path.exists(audio_file) and os.path.getsize(audio_file) > 0:
            audio_url = f"/audio/speech.mp3"
            return audio_url, "Conversion successful. Click play to listen."
        else:
            return "", "Error: Audio file was not created successfully."
    except Exception as e:
        print(f"Error during TTS conversion: {e}")
        return "", f"Error: {e}"

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)