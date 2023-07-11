from sklearn.feature_extraction.text import TfidfVectorizer


def sort_comments(comments):
    count_idf = TfidfVectorizer(ngram_range=(1, 1))
    comments_td_idf = count_idf.fit(comments["Comments"])
    base = count_idf.transform()
    return comments_td_idf

