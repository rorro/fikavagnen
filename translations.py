from googletrans import Translator, LANGUAGES

translator = Translator()

def translate(word):
    all_translations = []
    for lang in LANGUAGES:
        translation = translator.translate(
            word,
            src="en",
            dest=lang
        )
        if translation.text not in all_translations:
            all_translations.append(translation.text)

    print(all_translations)
