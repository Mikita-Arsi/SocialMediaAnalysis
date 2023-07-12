import threading
from dataset import processing
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class AnalisysThread(threading.Thread):
    def __init__(self, video_id: str, path_to_save_file: str, api_key: str, model_base):
        threading.Thread.__init__(self)
        self.video_id = video_id
        self.path_to_save_file = path_to_save_file
        self.api_key = api_key
        self.model_base = model_base

    def run(self):
        thread_num = self.path_to_save_file.split('.')[0]
        res = processing(self.video_id, self.path_to_save_file, self.api_key, self.model_base)
        share_neg = (res['negative_proba'] > 0.44).sum() / res['Comments'].shape[0]

        print(f"{thread_num}: {share_neg}")

        fig = make_subplots(1, 1,
                            subplot_titles=[f'Распределение комментариев по оценке негативности (видео {thread_num})']
                            )

        fig.add_trace(go.Violin(
            x=res['negative_proba'],
            name=f'{thread_num} (N = %i)' % res.shape[0],
            side='positive',
            spanmode='hard'
        ))

        fig.add_annotation(x=0.8, y=0.5,
                           text="%0.2f — доля негативных комментариев (при p > 0.44)" % share_neg,
                           showarrow=False,
                           yshift=10)

        fig.update_traces(orientation='h',
                          width=1.5,
                          points=False
                          )

        fig.update_layout(height=500,
                          xaxis_zeroline=False,
                          template='plotly_dark',
                          font_color='rgba(212, 210, 210, 1)',
                          legend=dict(
                              y=0.9,
                              x=-0.1,
                              yanchor='top',
                          ),
                          )
        fig.update_yaxes(visible=False)

        fig.show()


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


