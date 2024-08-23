from googletrans import Translator

def translate_story(stories, language):
    translation_arr = []
    
    translator = Translator()

    translations = [translator.translate(story, dest=language) for story in stories]

    for line in translations:
        inner_arr = [
            line.origin,
            line.pronunciation
        ]
        translation_arr.append(inner_arr)

    return translation_arr
