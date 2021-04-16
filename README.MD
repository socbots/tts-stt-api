## API written in python using flask and waitress for Google Text-To-Speech synthesis

A testing site for this API has been setup on https://www.dinmamma.fi/alftts/

## Requirements
Install requirements using 

`pip install -r requirements.txt`

Set google auth key environment variable using this guide

https://cloud.google.com/docs/authentication/getting-started

Run the server

`python server.py`



## Endpoints

> for testing on localhost

`localhost:5000/tts?ReqString="This is a test"&rate=1&pitch=0&hertz=16000&lang=sv-SE`

> Current Production env 

`http://alf-tts-api.herokuapp.com/tts?ReqString="This is a test"&rate=1&pitch=0&hertz=16000&lang=sv-SE`

## Arguments /tts 

> ReqString (Required, type = String)

This is the input string you want synthesized. Formatting can be either cleartext or using SSML. ReqString is parsed on request to match formatting and remove URLEncoded chars.
https://cloud.google.com/text-to-speech/docs/ssml

> rate (Optional, default = 1, Min = 0.25, Max = 4, type = float)

This is the speech rate. Lower is slower, higher is faster. 

> pitch (Optional, default =  -10, Min = -20, Max = 20, type = float)

This is the pitch, higher makes a more Lilla My sounding noise.

> hertz (Optional, default = 16000, Min = 8000, Max = 48000, type = int)

Sample rate. Reduce or increase quality of the synthesis.

Accepted values
- 8000
- 11025
- 12000
- 16000
- 22050
- 24000
- 32000
- 44100
- 48000

> lang (Optional, default = sv-SE, type = String)

Language of the input text. Check link below for a complete list of supported languages.
https://cloud.google.com/text-to-speech/docs/voices

> gender (Optional, default = FEMALE, type = String input converts to ENUM)

Gender to be synthesised. Not all languages support all genders. 
Accepted values
- FEMALE
- MALE
- NEUTRAL

#### Response

API Responds with a mp3 using flask send_from_directory. 

#### /listv

listv is used to List currently supported voices by the Google TTS API.