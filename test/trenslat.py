import os
from googletrans import Translator, LANGUAGES
import yaml

def translate_text(text, target_lang):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_lang)
    except Exception as e:
        print(f"Error: {e}")
        return text
    return translated.text

def translate_file(file_path, target_lang):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    translated_data = translate_structure(data, target_lang)

    new_file_path = file_path.replace('.yml', f'_{target_lang}.yml')
    with open(new_file_path, 'w', encoding='utf-8') as file:
        yaml.dump(translated_data, file, allow_unicode=True)

def translate_structure(struct, target_lang):
    if isinstance(struct, dict):
        return {key: translate_structure(value, target_lang) for key, value in struct.items()}
    elif isinstance(struct, list):
        return [translate_structure(item, target_lang) for item in struct]
    elif isinstance(struct, str):
        return translate_text(struct, target_lang)
    else:
        return struct  # if it's neither dict, list, nor str, return it as is

def main():
    directory_path = 'data'  # replace with your directory path
    target_languages = ['de', 'ta']  # German and Tamil

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            print(file)
            if file.endswith('.yml'):
                file_path = os.path.join(root, file)
                for target_lang in target_languages:
                    translate_file(file_path, target_lang)

if __name__ == "__main__":
    main()
