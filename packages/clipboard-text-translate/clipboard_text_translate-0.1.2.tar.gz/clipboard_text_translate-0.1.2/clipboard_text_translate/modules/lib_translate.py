#!/usr/bin/python3

import urllib.parse

def generate_google_translate_link(text, source_lang="auto", target_lang="en"):
    encoded_text = urllib.parse.quote(text)
    return f"https://translate.google.com/?sl={source_lang}&tl={target_lang}&text={encoded_text}&op=translate"


import asyncio
from googletrans import Translator

def translate_text_sync(text, source_lang='auto', target_lang='en'):
    '''
    No respeita \foramtação latex
    '''
    # Função assíncrona interna para obter a tradução
    async def translate():
        translator = Translator()
        translation = await translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text

    # Chama a função assíncrona e aguarda a tradução
    return asyncio.run(translate())


'''

text = "Hola, ¿cómo estás?"
translated_text = translate_text_sync(text, dest='en')

print(f"Texto original: {text}")
print(f"Tradução: {translated_text}")

'''

