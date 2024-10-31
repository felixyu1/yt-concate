import os
import fnmatch
import subprocess

from yt_concate.settings import CAPTIONS_DIR, VIDEO_FILE_EXT
from yt_concate.settings import CAPTION_FILE_EXT_EN_SRT
from yt_concate.settings import CAPTION_FILE_EXT_EN_VTT
from yt_concate.settings import DOWNLOADS_DIR
from yt_concate.settings import VIDEOS_DIR
from yt_concate.settings import OUTPUTS_DIR


class Utils:
    def __init__(self):
        pass

    def create_dir(self):
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        os.makedirs(VIDEOS_DIR, exist_ok=True)
        os.makedirs(CAPTIONS_DIR, exist_ok=True)
        os.makedirs(OUTPUTS_DIR, exist_ok=True)

    def get_video_list_file_path(self, channel_id):
        return os.path.join(DOWNLOADS_DIR, channel_id + '.txt')

    def video_list_file_exists(self, channel_id):
        path = self.get_video_list_file_path(channel_id)
        return os.path.exists(path) and os.path.getsize(path) > 0

    def get_caption_srt_filename(self, yt):
        return yt.id + CAPTION_FILE_EXT_EN_SRT

    def get_caption_vtt_filename(self, yt):
        return yt.id + CAPTION_FILE_EXT_EN_VTT

    def get_caption_vtt_path(self, yt):
        return os.path.join(CAPTIONS_DIR, self.get_caption_vtt_filename(yt))

    def get_caption_srt_path(self, yt):
        return os.path.join(CAPTIONS_DIR, self.get_caption_srt_filename(yt))

    def caption_file_exists(self, yt):
        path = self.get_caption_srt_path(yt)
        return os.path.exists(path) and os.path.getsize(path) > 0

    def get_video_filename(self, yt):
        return yt.id + VIDEO_FILE_EXT

    def get_video_real_filename(self, yt):
        path = VIDEOS_DIR
        pattern = yt.id + '.*'
        result = self.find(pattern, path)

        return result[0]

    def get_video_path(self, yt):
        return os.path.join(VIDEOS_DIR, self.get_video_filename(yt))

    def video_file_exists(self, yt):
        path = VIDEOS_DIR
        pattern = yt.id + '.*'
        result = self.find(pattern, path)
        #return os.path.exists(path) and os.path.getsize(path) > 0
        return len(result) > 0

    def convert_vtt_to_srt(self, yt):
        vtt_file = self.get_caption_vtt_path(yt)
        srt_file = self.get_caption_srt_path(yt)
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

    @staticmethod
    def convert_video_to_mp4():
        for filename in os.listdir(VIDEOS_DIR):
            if not filename.endswith(".mp4"):
                main_filename = filename.split('.')
                input_path = VIDEOS_DIR + '/' + filename
                output_path = VIDEOS_DIR + '/' + main_filename[0] +'.mp4'
                # ffmpeg 指令
                ffmpeg_command = ['ffmpeg', '-i', input_path, '-c:v', 'libx264', '-c:a', 'aac', '-strict',
                                  'experimental',
                                  output_path]
                # 執行轉換
                subprocess.run(ffmpeg_command, check=True)
            else:
                continue

    @staticmethod
    def find(pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
                    break
                else:
                    continue
            break
        return result

    def get_output_filepath(self, channel_id, search_word):
        filename = channel_id + '_' + search_word + '.mp4'
        return os.path.join(OUTPUTS_DIR, filename)