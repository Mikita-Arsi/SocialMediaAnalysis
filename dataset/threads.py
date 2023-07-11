import threading
from dataset import processing
from const import API_KEY


class AnalisysThread(threading.Thread):
    def __init__(self, video_id: str, path_to_save_file: str, api_key: str, model_base):
        threading.Thread.__init__(self)
        self.video_id = video_id
        self.path_to_save_file = path_to_save_file
        self.api_key = api_key
        self.model_base = model_base

    def run(self):
        processing(self.video_id, self.path_to_save_file, self.api_key, self.model_base)


class AnalisysThreads:
    def __init__(self, api_key: str, videos_ids: list[str], model_base):
        self.api_key = api_key
        self.model_base = model_base
        self.threads = self._create_threads(videos_ids)

    def _create_threads(self, videos_ids: list[str]) -> list[AnalisysThread]:
        threads = []
        for i, video_id in enumerate(videos_ids):
            threads.append(AnalisysThread(video_id, f"{i + 1}.csv", self.api_key, self.model_base))
        return threads

    def run(self):
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()


