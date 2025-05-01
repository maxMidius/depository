import panel as pn

# Initialize Panel extension
pn.extension()

# Create the TextToSpeech widget with a hardcoded message
tts = pn.widgets.TextToSpeech(
    name="Text-to-Speech",
    value="Hello TTS world",
)
tts.auto_speak = False  # Disable auto-speak to avoid immediate playback
tts.speak_button = pn.widgets.Button(name="Speak", button_type="primary")
tts.speak_button.on_click(lambda event: tts.speak())  # Bind the button to the speak method 

# Create a cancel button
cancel_button = pn.widgets.Button(name="Cancel", button_type="danger")
cancel_button.on_click(lambda event: tts.cancel())  # Bind the button to the cancel method

# Create the app layout including the TTS widget and buttons
app = pn.Column(
    pn.pane.Markdown("# Simple TTS Demo"),
    tts,  # Add the TTS widget to the layout
    pn.Row(tts.speak_button, cancel_button)  # Add both buttons in a row
)

# Make the app servable
app.servable()
