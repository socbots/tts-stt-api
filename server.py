#%%
import requests
import os
from flask import flash, Flask, send_from_directory, request, make_response, redirect, url_for
from flask_cors import CORS
from flask_caching import Cache
import flask
import urllib.parse
from google.cloud import speech
from google.cloud import texttospeech
from werkzeug.utils import secure_filename

import json

# Instantiates a client
client = texttospeech.TextToSpeechClient()

def CreateTTS(x, r, p, hz,lang, gender):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=x)
    gen = ""
    
    if(gender == "FEMALE"):
        gen = texttospeech.SsmlVoiceGender.FEMALE
    elif(gender == "MALE"):
        gen = texttospeech.SsmlVoiceGender.MALE
    else:
        gen = texttospeech.SsmlVoiceGender.NEUTRAL
    
    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang, ssml_gender=gen
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
    "CACHE_DEFAULT_TIMEOUT": 86400,
    "UPLOAD_FOLDER": '/'
}

# Create server
app = Flask(__name__)  
# NO CORS, BAD CORS!!!
CORS(app)
# Add conf file to app
app.config.from_mapping(config)
# Create cache
cache = Cache(app)
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/tts")

def tts():

    TDIR = os.path.dirname(__file__)
    filename = "output.mp3"
    ReqString = request.args.get('ReqString')
    rate = request.args.get('rate') or 1
    pitch = request.args.get('pitch') or -10
    hertz = request.args.get('hertz') or 16000
    lang = request.args.get('lang') or "sv-SE"
    gender = request.args.get('gender') or "FEMALE"
    ReqString = urllib.parse.unquote(str(ReqString))
    hertz = int(hertz)
    rate = float(rate)
    pitch = float(pitch)
    lang = str(lang)
    print("String: " + str(ReqString))
    print("Speechrate: " + str(rate))
    print("Hertz: " + str(hertz))
    print("Pitch: " + str(pitch))
    print("Lang: " + str(lang))
    print("Gender: " + str(gender))
    
    if(ReqString):
        response = CreateTTS(ReqString, rate, pitch, hertz, lang, gender)
        with open(filename, "wb") as out:
        # Write the response to the output file.
            out.write(response.audio_content)
        path = os.path.join(TDIR + filename) 
        return send_from_directory(TDIR, path, as_attachment=True)


@app.route("/stt", methods=['GET','POST'])


def sst():


    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            content = file.read()

    #print(request.form['foo']) # should display 'bar'
    #return 'Received !' # response to your request.
            client = speech.SpeechClient()

            audio = speech.RecognitionAudio(content=content)

            config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=16000, language_code="sv-SE")
    
            response = client.recognize(config=config, audio=audio)


            for result in response.results:
                print("Transcript: {}".format(result.alternatives[0].transcript))
                
            return(response.results)



@app.route("/listv")

def list_voices():
    """Lists the available voices."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()
    voicelist = {}
    for voice in voices.voices:

        # Display the voice's name. Example: tpc-vocoded
        print(f"Name: {voice.name}")
        d = ""
        # Display the supported language codes for this voice. Example: "en-US"
        for language_code in voice.language_codes:
            d = language_code
            print(f"Supported language: {language_code}")

        lang = {voice.name : {"langCode" : d, "gender": voice.ssml_gender, "sammple": voice.natural_sample_rate_hertz}}

        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # Display the SSML Voice Gendera
        print(f"SSML Voice Gender: {ssml_gender.name}")

        # Display the natural sample rate hertz for this voice. Example: 24000
        print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")
        voicelist.update(lang)
        print(voice)
    return json.dumps(voicelist)

if __name__ == "__main__":
    # Waitress host for production
    from waitress import serve
    pp = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=pp)
# %%
