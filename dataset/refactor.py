import re
import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords as nltk_stopwords
from pymystem3 import Mystem
from .utils import stopwords


def clear_text(text: str) -> str:
    clear_text = re.sub(r'[^А-яЁё]+', ' ', text).lower()
    return ' '.join(clear_text.split())


def clean_stop_words(text, stopwords):
    text = [word for word in text.split() if word not in stopwords]
    return " ".join(text)


def lemmatize(df: (pd.Series, pd.DataFrame),
              text_column: (None, str),
              n_samples: int,
              break_str='br',
              ) -> pd.Series:
    result = []

    m = Mystem()

    for i in range((df.shape[0] // n_samples) + 1):
        start = i * n_samples
        stop = start + n_samples
        sample = break_str.join(df[text_column][start: stop].values)
        lemmas = m.lemmatize(sample)
        lemm_sample = ''.join(lemmas).split(break_str)
        result += lemm_sample

    return pd.Series(result, index=df.index)


def refactoring(comments):
    np.array(stopwords)

    comments = pd.DataFrame({"Comments": [
        clean_stop_words(
            clear_text(comments["Comments"][i]),
            stopwords
        ) for i, comment in enumerate(comments["Comments"])
    ]})
    comments = lemmatize(comments, "Comments", 100)
    return comments

