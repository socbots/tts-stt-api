#%%
import requests
import os
from flask import Flask, send_from_directory, request, make_response
from flask_cors import CORS
from flask_caching import Cache
import flask

from google.cloud import texttospeech


# Instantiates a client
client = texttospeech.TextToSpeechClient()


def CreateTTS(x):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=x)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="sv-SE", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response
    # The response's audio_content is binary.

#CreateTTS("test string")

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 86400
}
# Create server
app = Flask(__name__, static_folder='static')  
# NO CORS, BAD CORS!!!
CORS(app)
# Add conf file to app
app.config.from_mapping(config)
# Create cache
cache = Cache(app)
@app.route("/tts")

def tts():

    filename = "output.mp3"
    ReqString = request.args.get('ReqString')
    
    if(ReqString):
        response = CreateTTS(ReqString)
        with open(filename, "wb") as out:
        # Write the response to the output file.
            out.write(response.audio_content)
        return send_from_directory("static",filename, as_attachment=True)

        #return response.audio_content

def send_file(filename):  
    return send_from_directory(app.static_folder, filename)
    
if __name__ == "__main__":
    # Waitress host for production
   # from waitress import serve
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)