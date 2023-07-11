from googleapiclient.discovery import build
from .save import save_to_csv


class CollectComments:
    def __init__(self, api_key: str, video_id: str, comments_list: list = None):
        if comments_list is None:
            self.comments_list = []
        else:
            self.comments_list = comments_list
        self.api_key = api_key
        self.video_id = video_id
        self.connection = build('youtube', 'v3', developerKey=self.api_key)

    def collect_comments(self, resp):
        for item in resp['items']:
            comment = item["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            if comment not in self.comments_list:
                self.comments_list.append(comment)

            reply_count = item["snippet"]['totalReplyCount']
            if reply_count > 0:
                parent = item["snippet"]['topLevelComment']["id"]
                reply_comments = self.connection.comments().list(part='snippet', maxResults='10', parentId=parent,
                                                                 textFormat="plainText").execute()
                for i in reply_comments["items"]:
                    comment = i["snippet"]["textDisplay"]
                    if comment not in self.comments_list:
                        self.comments_list.append(comment)

    def get_comments(self, path_to_save_file):
        response = self.connection.commentThreads().list(part='snippet, replies', videoId=self.video_id).execute()
        self.collect_comments(response)
        while 'nextPageToken' in response:
            response = self.connection.commentThreads().list(part='snippet, replies', videoId=self.video_id,
                                                             pageToken=response["nextPageToken"]).execute()
            self.collect_comments(response)
        return save_to_csv(path_to_save_file, self.comments_list)
