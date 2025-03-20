import os.path
import pickle

import nltk


class BrillPostagger:
    MODELS = {
        "ca": "ca_ancora-ud-brill",
        "da": "da_ddt-ud-brill",
        "de": "de_gsd-ud-brill",
        "en": "en_ewt-ud-brill",
        "es": "es_ancora-ud-brill",
        "eu": "eu_bdt-ud-brill",
        "fr": "fr_gsd-ud-brill",
        "gl": "gl_ctg-ud-brill",
        "it": "it_vit-ud-brill",
        "nl": "nl_alpino-ud-brill",
        "pt": "pt_bosque-ud-brill"
    }
    def __init__(self, model: str):
        with open(model, "rb") as f:
            self.tagger = pickle.load(f)

    @staticmethod
    def from_pretrained(lang: str):
        lang = lang.split("-")[0].lower()
        model = BrillPostagger.MODELS[lang]
        return BrillPostagger(f"{os.path.dirname(__file__)}/{model}.pkl")

    def tag(self, sentence: str):
        tokens = nltk.word_tokenize(sentence)
        return self.tagger.tag(tokens)

if __name__ == "__main__":
    tagger = BrillPostagger.from_pretrained("pt")
    print(tagger.tag("como está o tempo lá fora?"))