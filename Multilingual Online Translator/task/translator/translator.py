import sys

import requests
from bs4 import BeautifulSoup

langs = [
    "Arabic",
    "German",
    "English",
    "Spanish",
    "French",
    "Hebrew",
    "Japanese",
    "Dutch",
    "Polish",
    "Portuguese",
    "Romanian",
    "Russian",
    "Turkish",
]


def print_and_write(text: str):
    print(text)
    f.write(text + "\n")


def get_translation(from_lang: str, to_lang: str, word: str) -> None:
    url = f"https://context.reverso.net/translation/{from_lang.lower()}-{to_lang.lower()}/{word}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    if not r:
        print(f"Sorry, unable to find {word}")
        sys.exit(-1)
    print_and_write("Translations")
    soup = BeautifulSoup(r.content, "html.parser")

    print_and_write(f"{to_lang} Translations:")
    terms = [t.text for t in soup.select(".display-term")]
    for term in terms:
        print_and_write(term)

    print_and_write(f"{to_lang} Examples:")
    terms = [t.text.strip() for t in soup.select("#examples-content .ltr span") if t.text != ""]
    for term in terms:
        print_and_write(term)


from_lang, to_lang, word = sys.argv[1:]
for lang in (from_lang, to_lang):
    if lang.lower() not in [l.lower() for l in langs] and lang != "all":
        print(f"Sorry, the program doesn't support {lang}")
        sys.exit(-1)

with open(f"{word}.txt", "w") as f:
    if to_lang == "all":
        for lang in langs:
            get_translation(from_lang, lang, word)
    else:
        get_translation(from_lang, to_lang, word)
