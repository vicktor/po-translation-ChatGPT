# -*- coding: utf-8 -*-

import polib		# pip install polib
import openai		# pip install openai
import typer		# pip install "typer[all]"
import re
import datetime
import os


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# Función para generar una respuesta utilizando la API de ChatGPT
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Devolver la primera respuesta generada por ChatGPT
    return response["choices"][0]["text"]

def save_entry(file, msgid, msgstr, occurrences):
    entry = polib.POEntry(
        msgid=msgid,
        msgstr=msgstr,
        occurrences=occurrences
    )
    file.append(entry)


def main():
    language = typer.prompt("\nPlease, enter the language you want to translate to (e.g., Catalan) ")

    source = typer.prompt("\nPlease, enter your source po file (must be in english, e.g., en_US.po) ")
    destination = typer.prompt("\nPlease, enter your destination file (e.g., ca_ES.po) ")

    print("\n")

    po = polib.pofile(source)
    total = len(po)

    printProgressBar(0, total, prefix = 'Progress:', suffix = 'Translating to {0}...'.format(language), length = 50)
    now = datetime.datetime.now()

    translated = polib.POFile()
    translated.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': 'you@example.com',
        'POT-Creation-Date': now,
        'PO-Revision-Date': now,
        'Last-Translator': 'ChatGPT',
        'Language-Team': 'English',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
    }

    # Inicializar la biblioteca openai utilizando tu secret key, debe ser una variable del sistema
    # export OPENAI_API_KEY = tu_clave_obtenida_en_openai.com
    openai.api_key = os.getenv("OPENAI_API_KEY")

    i = 0
    for entry in po:
        prompt = "Translate this into {0}. {1}".format(language, entry.msgid)
        i += 1
        printProgressBar(i, total, prefix = 'Progress:', suffix = 'Translating to {0}'.format(language), length = 50)
        text = re.sub(r'^\n+', '',generate_response(prompt))
        save_entry(translated, entry.msgid, text, entry.occurrences)


    translated.save(destination)


if __name__ == "__main__":
    main()
