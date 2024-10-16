import os
import subprocess
from yt_concate.settings import CAPTIONS_DIR
from yt_concate.settings import VIDEOS_DIR
from yt_concate.settings import DOWNLOADS_DIR
from yt_concate.settings import CAPTION_FILE_EXT_EN_VTT
from yt_concate.settings import CAPTION_FILE_EXT_EN_SRT



class Utils:
    def __init__(self):
        pass

    def create_dir(self):
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        os.makedirs(VIDEOS_DIR, exist_ok=True)
        os.makedirs(CAPTIONS_DIR, exist_ok=True)

    def get_video_list_file_path(self, channel_id):
        return os.path.join(DOWNLOADS_DIR, channel_id+'.txt')

    def video_list_file_exists(self, channel_id):
        path = self.get_video_list_file_path(channel_id)
        return os.path.exists(path) and os.path.getsize(path) > 0

    @staticmethod
    def get_video_id_from_url(url):
        return url.split('watch?v=')[-1]

    def get_caption_srt_filename(self, url):
        return self.get_video_id_from_url(url) + CAPTION_FILE_EXT_EN_SRT

    def get_caption_vtt_filename(self, url):
        return self.get_video_id_from_url(url) + CAPTION_FILE_EXT_EN_VTT

    def get_caption_path(self, url):
        return os.path.join(CAPTIONS_DIR, self.get_video_id_from_url(url))

    def get_caption_vtt_path(self, url):
        return os.path.join(CAPTIONS_DIR, self.get_caption_vtt_filename(url))

    def get_caption_srt_path(self, url):
        return os.path.join(CAPTIONS_DIR, self.get_caption_srt_filename(url))

    def caption_file_exists(self, url):
        path = self.get_caption_srt_path(url)
        return os.path.exists(path) and os.path.getsize(path) > 0

    def convert_vtt_to_srt(self, url):
        vtt_file = self.get_caption_vtt_path(url)
        srt_file = self.get_caption_srt_path(url)
        # 確認 vtt 文件是否存在
        if os.path.exists(vtt_file):
            # 使用 ffmpeg 進行 vtt 到 srt 的轉換
            ffmpeg_command = ['ffmpeg', '-i', vtt_file, srt_file]
            try:
                subprocess.run(ffmpeg_command, check=True)
                print(f"字幕已下載並轉換為 SRT: {srt_file}")
                os.remove(vtt_file)
            except subprocess.CalledProcessError as e:
                print(f"字幕轉換失敗: {e}")
        else:
            print("未找到 vtt 文件，轉換失敗")
