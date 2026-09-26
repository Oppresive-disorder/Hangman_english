import nltk
import requests
from nltk.corpus import wordnet, words

nltk.download("wordnet", quiet=True)
nltk.download("words", quiet=True)


english_hord = [w.lower() for w in set(words.words("en")) if w.isalpha()]
easy_words = [w for w in english_hord if 2 <= len(w) <= 5]
medium_words = [w for w in english_hord if 6 <= len(w) <= 7]
hard_words = [w for w in english_hord if 8 <=len(w) <= 12]
expert_words = [w for w in english_hord if len(w) >= 13]

def fetch_from_free_dictionary(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url, timeout=2)
    if response.status_code == 200:
        return response.json()[0]["meanings"][0]["definitions"][0]["definition"]
    return None

def fetch_from_datamuse(word):
    url = f"https://api.datamuse.com/words?sp={word}&md=d"
    response = requests.get(url, timeout=2)
    if response.status_code == 200:
        data = response.json()
        if data and "defs" in data[0]:
            raw_def = data[0]["defs"][0]
            return raw_def.split("\t")[-1]
    return None

def fetch_from_wordnet_local(word):
    synsets = wordnet.synsets(word)
    if synsets:
        return synsets[0].definition()
    return "A worddddd!"


def get_definition(word):
    try:
      definition = fetch_from_free_dictionary(word)
      if definition:
         return definition
    except Exception:
        pass
    try:
        definition = fetch_from_datamuse(word)
        if definition:
            return definition
    except Exception: 
        pass
    return fetch_from_wordnet_local(word)