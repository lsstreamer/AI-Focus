import sqlite3
import json
import requests
import time
import os
from pydub import AudioSegment
from flask import jsonify  # 添加这一行导入jsonify

import threading
import time
from pyaudio import PyAudio, paInt16
from datetime import datetime
from database import save_music_info

# 配置音频生成 API 参数
music_gen_url = "https://api.openxs.top"  # 音频生成 API 地址
sona_api_key = (
    "sk-SL22yWBntU30UOpsynU9hezJ1v2K7pn8lfn3dkjCV6RkaDRE"  # 替换为你的音频生成 API Key
)

# API_KEY = "sk-0WvJEHRL7prCLh3cMDC5abDoM9xF3Bt0WxnTiIZ3tH3a4eIG"


class AudioPlayer:
    """线程安全的音频播放器，支持MP3/WAV格式，实现完整播放控制"""

    def __init__(self):
        self.lock = threading.RLock()  # 可重入锁
        self.play_event = threading.Event()  # 播放控制事件
        self.stop_event = threading.Event()  # 终止信号
        self.pause_event = threading.Event()  # 暂停信号
        self.audio = None
        self.play_obj = None
        self.play_thread = None
        self.pause_position = 0  # 毫秒
        self.sample_rate = 44100
        self.channels = 2
        self.volume = 1.0  # 0.0-1.0

    def load(self, file_path):
        """加载音频文件，自动识别格式"""
        with self.lock:
            self._release_resources()
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"音频文件不存在: {file_path}")

            if file_path.lower().endswith(".mp3"):
                self.audio = AudioSegment.from_mp3(file_path)
            elif file_path.lower().endswith(".wav"):
                self.audio = AudioSegment.from_wav(file_path)
            else:
                raise ValueError("不支持的音频格式")

            self._convert_parameters()
            self.pause_position = 0

    def _convert_parameters(self):
        """统一音频参数"""
        self.audio = self.audio.set_frame_rate(self.sample_rate)
        self.audio = self.audio.set_channels(self.channels)
        self.audio = self.audio.set_sample_width(2)  # 16-bit

    def play(self):
        """开始/恢复播放"""
        with self.lock:
            if self.play_thread and self.play_thread.is_alive():
                if self.pause_event.is_set():
                    self.resume()
                return

            if not self.audio:
                raise ValueError("未加载音频文件")

            self.stop_event.clear()
            self.play_event.set()
            self.pause_event.clear()

            self.play_thread = threading.Thread(target=self._play_loop, daemon=True)
            self.play_thread.start()

    def _play_loop(self):
        """播放主循环，实现进度控制"""
        try:
            p = PyAudio()
            stream = p.open(
                format=paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
            )

            start_pos = self.pause_position
            total_frames = len(self.audio)

            # 转换为原始音频数据
            raw_data = self.audio[start_pos:].raw_data
            frame_size = self.channels * 2  # 16-bit = 2字节
            frames = memoryview(raw_data).cast("B")

            idx = 0
            while not self.stop_event.is_set() and idx < len(frames):
                if self.pause_event.is_set():
                    time.sleep(0.1)
                    continue

                chunk = frames[idx : idx + 4096 * frame_size]
                stream.write(chunk.tobytes())
                idx += len(chunk)
                self.pause_position = start_pos + int(
                    idx / (frame_size * self.sample_rate) * 1000
                )

            stream.stop_stream()
            stream.close()
            p.terminate()

        except Exception as e:
            print(f"播放错误: {e}")
        finally:
            self._release_resources()

    def pause(self):
        """暂停播放"""
        with self.lock:
            if self.play_thread and self.play_thread.is_alive():
                self.pause_event.set()
                return True
            return False

    def resume(self):
        """恢复播放"""
        with self.lock:
            if self.pause_event.is_set():
                self.pause_event.clear()
                return True
            return False

    def stop(self):
        """完全停止并重置"""
        with self.lock:
            self.stop_event.set()
            self.play_event.clear()
            self.pause_position = 0

            # 等待线程结束
            if self.play_thread and self.play_thread.is_alive():
                self.play_thread.join(timeout=1)  # 最多等待1秒

            self._release_resources()  # 确保资源释放

    def seek(self, position_ms):
        """跳转到指定位置"""
        with self.lock:
            if 0 <= position_ms <= len(self.audio):
                self.pause_position = position_ms
                if self.is_playing():
                    self.stop()
                    self.play()

    def set_volume(self, volume):
        """设置音量(0.0-1.0)"""
        with self.lock:
            self.volume = max(0.0, min(1.0, volume))
            if self.audio:
                self.audio = self.audio.apply_gain(20 * (self.volume - 1.0))

    def is_playing(self):
        """播放状态检查"""
        return self.play_thread and self.play_thread.is_alive()

    def _release_resources(self):
        """安全释放音频资源"""
        if self.play_obj:
            try:
                self.play_obj.stop()
                if hasattr(self.play_obj, "close"):
                    self.play_obj.close()
            except:
                pass
            self.play_obj = None

    def __del__(self):
        self.stop()


def create_music_by_sona(prompt, is_instrumental):
    print(f"🎵 开始生成音乐: {prompt}， is_instrumental：{is_instrumental}")
    task_id = submit_music_task(prompt, is_instrumental=is_instrumental)
    if task_id:
        audio_url = fetch_music_task_status(task_id)
        if audio_url:

            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(MUSIC_DIR, f"{current_time}.mp3")

            # 下载音频到本地，并保存为当前时间命名的文件
            success = download_audio(audio_url, filename)

            # 将音乐信息保存到数据库
            if success:
                music_info = {
                    "path": filename,
                    "music_prompt": prompt,
                    "is_instrumental": is_instrumental,
                    "is_liked": False,  # 默认未标记喜欢
                }

                save_music_info(music_info)
                return filename
            else:
                return None
        else:
            print("音频生成任务未能成功完成！")
            return None
    else:
        print("音频生成任务提交失败！")
        return None


# 提交音乐生成任务
def submit_music_task(prompt, is_instrumental=False):
    """提交音乐生成任务"""
    url = f"{music_gen_url}/suno/submit/music"
    headers = {
        "Authorization": f"Bearer {sona_api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    music_request = {
        "gpt_description_prompt": prompt,
        "make_instrumental": is_instrumental,
        "mv": "chirp-v3-0",
    }
    response = requests.post(url, json=music_request, headers=headers)
    data = response.json()
    if data.get("code") == "success":
        task_id = data["data"]
        print(f"音乐生成任务提交成功！任务 ID: {task_id}")
        return task_id
    else:
        print(f"音乐生成任务提交失败: {data.get('message', '未知错误')}")
        return None


# 轮询查询任务状态并获取音频
def fetch_music_task_status(task_id):
    """轮询查询音乐生成任务状态"""
    url = f"{music_gen_url}/suno/fetch/{task_id}"
    headers = {
        "Authorization": f"Bearer {sona_api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    while True:
        response = requests.get(url, headers=headers)
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("API 返回的不是 JSON 格式！")
            return None
        if data.get("code") == "success":
            task_data = data.get("data", {})
            status = task_data.get("status", "pending")
            print(f"任务状态: {status}")
            if status == "SUCCESS":
                song_data = task_data.get("data", [])
                if song_data:
                    audio_url = song_data[0].get("audio_url")
                    if audio_url:
                        print(f"任务完成，音频 URL: {audio_url}")
                        return audio_url
                print("音频数据为空！")
                return None
        else:
            print(f"查询失败: {data.get('message', '未知错误')}")
            return None
        time.sleep(5)


def download_audio(audio_url, filename):
    """下载音频文件并保存到本地"""
    try:
        response = requests.get(audio_url)
        response.raise_for_status()  # 如果响应码不是 200，会抛出异常
        # 保存音频文件到本地
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"🎶 音乐已下载: {filename}")

        from response_by_AI import SoundTips

        SoundTips("音乐已经为您生成完毕，请欣赏吧！")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ 下载失败: {e}")
        return False


from path import MUSIC_DIR


def get_latest_music():
    """获取音乐文件夹下最新的音乐文件"""
    # 获取文件夹中所有的文件
    files = [
        f for f in os.listdir(MUSIC_DIR) if os.path.isfile(os.path.join(MUSIC_DIR, f))
    ]

    # 获取最新文件（按修改时间排序）
    if files:
        latest_file = max(
            files, key=lambda f: os.path.getmtime(os.path.join(MUSIC_DIR, f))
        )
        return os.path.join(MUSIC_DIR, latest_file)
    else:
        return "Error: 没有找到音乐文件！"


def play_sound(player: AudioPlayer, filename):
    """播放音频接口"""
    if not os.path.exists(filename):
        print(f"音频文件不存在: {filename}")
        return

    player.stop()  # 停止当前播放的音频
    player.load(filename)
    player.play()
