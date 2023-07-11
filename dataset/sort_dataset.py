import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def do_analysis(comments):
    all_com = pd.read_csv('ml\\train\\labeled_tweets_clean.csv', sep=',', header=None).dropna()
    all_com.columns = ['n', 'text', 'label']
    all_com['label'] = pd.to_numeric(all_com['label'])
    count_idf = TfidfVectorizer(ngram_range=(1, 1))
    count_idf.fit_transform(all_com['text'])
    count_idf.transform(comments["Comments"])

    return count_idf

