import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def get_model_base():

    all_com = pd.read_csv('train\\labeled_tweets_clean.csv', sep=',', header=None).dropna()
    all_com.columns = ['n', 'text', 'label']
    all_com['label'] = pd.to_numeric(all_com['label'])
    train, test = train_test_split(all_com,
                                   test_size=0.2,
                                   random_state=12348,
                                   )

    train.columns = ['n', 'text', 'label']
    test.columns = ['n', 'text', 'label']

    count_idf_positive = TfidfVectorizer(ngram_range=(1, 1))
    count_idf_negative = TfidfVectorizer(ngram_range=(1, 1))

    count_idf_positive.fit_transform(train.query('label == 1')['text'])
    count_idf_negative.fit_transform(train.query('label == 0')['text'])
    count_idf = TfidfVectorizer(ngram_range=(1, 1))

    tf_idf_base = count_idf.fit(all_com['text'])
    tf_idf_train_base = count_idf.transform(train['text'])

    model_lr_base = LogisticRegression(solver='lbfgs', random_state=12345, max_iter=10000, n_jobs=-1)
    model_lr_base.fit(tf_idf_train_base, train['label'])

    return model_lr_base
