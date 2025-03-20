from gtts import gTTS
import subprocess
import platform
from pydub import AudioSegment


# Main function to convert text to speech and play the audio
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    
    # Create the MP3 file
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)
    
    # Convert MP3 to WAV
    wav_filepath = output_filepath.replace(".mp3", ".wav")
    convert_mp3_to_wav(output_filepath, wav_filepath)
    
    # Play the WAV file
    play_audio(wav_filepath)

def convert_mp3_to_wav(mp3_filepath, wav_filepath):
    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(mp3_filepath)
    audio.export(wav_filepath, format="wav")

# Function to play the audio based on the operating system
def play_audio(filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

#input_text = "Hi this is Pharmacist Samad, autoplay testing!" 
#text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")