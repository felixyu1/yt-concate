from warnings import catch_warnings

import yt_dlp

from .step import Step


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        # 設置下載參數
        ydl_opts = {
            'writesubtitles': True,  # 下載字幕
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'vtt',
            'skip_download': True,
            'outtmpl': '',
        }

        # YouTube 影片的網址
        #video_url = 'https://www.youtube.com/watch?v=4HSUztF59zo'

        for video_url in data:
            print('Downloading caption for ', video_url)
            if utils.caption_file_exists(video_url):
                print('found existing caption file')
                continue

            ydl_opts['outtmpl'] = utils.get_caption_path(video_url)

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(video_url)

                utils.convert_vtt_to_srt(video_url)
            except (KeyError, AttributeError):
                print('Error when downloading caption for ', video_url)
                continue

        return
