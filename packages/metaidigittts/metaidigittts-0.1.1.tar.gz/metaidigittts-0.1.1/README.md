# metaidigitstt

## Overview
**metaidigitstt** is a simple and lightweight speech-to-text and text-to-speech recognition module. It leverages **Google Text-to-Speech (gTTS)** for text-to-speech conversion and **pydub** for audio format conversion.

## Features
- Convert text to speech using gTTS
- Save speech as an MP3 file
- Convert MP3 to WAV format
- Play the generated audio file
- Cross-platform support (Windows, macOS, Linux)

## Installation

### Prerequisites
Ensure you have Python **3.10+** ; **google-cloud-texttospeech** & **pydub** libraries installed on your system.

### Install Dependencies
Run the following command to install required dependencies:
```sh
pip install metaidigittts
pip install google-cloud-texttospeech
pip install pydub
```

## Usage

### Import and Use in Your Python Code
```python
from metaidigitstt import text_to_speech_with_gtts

input_text = "Hello, this is a speech-to-text test!"
text_to_speech_with_gtts(input_text, "output.mp3")
```

### Convert MP3 to WAV
```python
from metaidigitstt import convert_mp3_to_wav

convert_mp3_to_wav("output.mp3", "output.wav")
```

### Play an Audio File
```python
from metaidigitstt import play_audio

play_audio("output.wav")
```

## Project Structure
```
metaidigitstt/
│── metaidigitstt/      # Module package
│   │── __init__.py     # Package initialization
│   │── main.py         # Main functions for TTS and audio conversion
│── setup.py            # Setup file for packaging
│── requirements.txt    # Required dependencies
│── README.md           # Documentation
```

## License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for more details.

## Author
Developed by **Suhal Samad**  
📧 Email: samadsuhal@gmail.com

