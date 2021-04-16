# API written in python using flask and waitress for Google Text-To-Speech synthesis

### Endpoints

#### /tts

##### Arguments

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