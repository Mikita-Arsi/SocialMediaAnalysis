from sklearn.feature_extraction.text import TfidfVectorizer

from .collect_comments import CollectComments
from .refactor import refactoring
from .sort_dataset import sort_comments


def processing(video_id, path_to_save_file, api_key, model_base):
    count_idf_positive = TfidfVectorizer(ngram_range=(1, 1))
    count_idf_negative = TfidfVectorizer(ngram_range=(1, 1))

    comments = CollectComments(api_key, video_id).get_comments(path_to_save_file)
    comments_tf_idf = sort_comments(comments)
    comments_tf_idf_base =


    negative_proba = model_base.predict_proba(comments_tf_idf)
    print(negative_proba)






