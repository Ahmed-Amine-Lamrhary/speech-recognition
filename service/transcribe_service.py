from service.audio_processor import get_text_from_audio
from service.command_execution import execute_command
from service.command_recognizer import recognize_command

def handle_transcribe(audio_file):
    # get text from audio file
    text = get_text_from_audio(audio_file)

    # get command from text
    command_name = recognize_command(text)

    # execute command
    if command_name:
        execute_command(command_name, text)

    return text
