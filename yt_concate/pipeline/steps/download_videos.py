import yt_dlp

from .step import Step

class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        # 設定 yt-dlp 的下載選項
        ydl_opts = {
            'format': 'bestvideo+bestaudio',  # 下載最好的可用影片質量
            #'merge_output_format': 'mp4',
            'outtmpl': '.%(ext)s',  # 自定義輸出檔案名稱，影片標題加上副檔名
            'nooverwrites': True
        }

        yt_set = set([found.yt for found in data])

        for yt in yt_set:

            ydl_opts['outtmpl'] = yt.video_filepath

            print('Downloading..', yt.url)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(yt.url)

        return data