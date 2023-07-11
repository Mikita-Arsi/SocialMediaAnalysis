from .collect_comments import CollectComments
from .sort_dataset import do_analysis


def processing(video_id, path_to_save_file, api_key, model_base):

    comments = CollectComments(api_key, video_id).get_comments(path_to_save_file)
    count_idf = do_analysis(comments)
    comments_tf_idf = count_idf.transform(comments['Comments'])

    negative_proba = model_base.predict_proba(comments_tf_idf)
    comments['negative_proba'] = negative_proba[:, 0]
    share_neg = (comments['negative_proba'] > 0.44).sum() / comments['Comments'].shape[0]
    print(f'https://youtu.be/{video_id}', share_neg)

