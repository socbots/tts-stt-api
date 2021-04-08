#%%
import requests
import os
from flask import Flask, send_from_directory, request, make_response
from flask_cors import CORS
from flask_caching import Cache
import flask
import urllib.parse
from google.cloud import texttospeech


# Instantiates a client
client = texttospeech.TextToSpeechClient()


def CreateTTS(x, r, p, hz):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=x)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="sv-SE", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        pitch=p,
        speaking_rate=r,
        sample_rate_hertz=hz,
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 86400
}


# Create server
app = Flask(__name__)  
# NO CORS, BAD CORS!!!
CORS(app)
# Add conf file to app
app.config.from_mapping(config)
# Create cache
cache = Cache(app)
@app.route("/tts")

def tts():

    TDIR = os.path.dirname(__file__)
    filename = "output.mp3"
    ReqString = request.args.get('ReqString')
    rate = request.args.get('rate') or 1
    pitch = request.args.get('pitch') or -10
    hertz = request.args.get('hertz') or 16000
    ReqString = urllib.parse.unquote(ReqString)
    hertz = int(hertz)
    rate = float(rate)
    pitch = float(pitch)

    print(ReqString)
    if(ReqString):
        response = CreateTTS(ReqString, rate, pitch, hertz)
        with open(filename, "wb") as out:
        # Write the response to the output file.
            out.write(response.audio_content)
        path = os.path.join(TDIR + filename) 
        return send_from_directory(TDIR, path, as_attachment=True)
    
if __name__ == "__main__":
    # Waitress host for production
    from waitress import serve
    pp = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=pp)