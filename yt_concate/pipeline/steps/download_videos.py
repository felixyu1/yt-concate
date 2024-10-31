import yt_dlp

from .step import Step


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        # 設定 yt-dlp 的下載選項
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # 下載最好的可用影片質量
            #'merge_output_format': 'mp4',
            'outtmpl': '',  # 自定義輸出檔案名稱，影片標題加上副檔名
            'nooverwrites': True,
        }

        yt_set = set([found.yt for found in data])

        for yt in yt_set:

            ydl_opts['outtmpl'] = yt.video_filepath

            print('Downloading video for ', yt.url)
            if utils.video_file_exists(yt):
                print('found existing video file')
                continue

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(yt.url)

        #Utils.convert_video_to_mp4()

        return data