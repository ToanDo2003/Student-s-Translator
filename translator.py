from googletrans import Translator
from language import language

def translate_language(text,language):
    translator = Translator()
    translation = translator.translate(text=text, dest=language)
    return translation.text
