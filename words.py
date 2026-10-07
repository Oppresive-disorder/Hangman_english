import random
import requests
from functools import lru_cache


@lru_cache(maxsize=1)
def _get_word_lists():
    import nltk
    from nltk.corpus import wordnet, words

    nltk.download("wordnet", quiet=True)
    nltk.download("words", quiet=True)

    wordnet_lemmas = {lemma.lower() for lemma in wordnet.all_lemma_names()}
    english_words = {
        word.lower()
        for word in words.words("en")
        if word.isalpha() and word.lower() in wordnet_lemmas
    }
    return (
        [word for word in english_words if 2 <= len(word) <= 5],
        [word for word in english_words if 6 <= len(word) <= 7],
        [word for word in english_words if 8 <= len(word) <= 12],
        [word for word in english_words if len(word) >= 13],
    )

def get_random_word(difficulty_level):
    easy_words, medium_words, hard_words, expert_words = _get_word_lists()
    if difficulty_level == 1:
        return random.choice(easy_words)
    elif difficulty_level == 2:
        return random.choice(medium_words)
    elif difficulty_level == 3:
        return random.choice(hard_words)
    else:
        return random.choice(expert_words)


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
    from nltk.corpus import wordnet

    synsets = wordnet.synsets(word)
    if synsets:
        return synsets[0].definition()
    return ("definition not found")


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