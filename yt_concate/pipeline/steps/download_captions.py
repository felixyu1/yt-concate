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

        for yt in data:
            print('Downloading caption for ', yt.id)
            if utils.caption_file_exists(yt):
                print('found existing caption file')
                continue

            ydl_opts['outtmpl'] = yt.caption_filepath

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(yt.url)

                utils.convert_vtt_to_srt(yt)
            except (KeyError, AttributeError):
                print('Error when downloading caption for ', yt.url)
                continue

        return data
