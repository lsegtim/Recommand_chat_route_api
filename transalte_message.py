from googletrans import Translator
translator = Translator()

def translate_message(message):
    return translator.translate(message, dest='en').text

def translate_message_back(message, dest='en'):
    return translator.translate(message, dest=dest).text

# german_message = "Hallo, wie geht es dir?"
# english_message = "Hello, how are you?"
# tamil_message = "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?"
