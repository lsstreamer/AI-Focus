import pyaudio
import wave
import numpy as np
import threading
import requests
import os
from datetime import datetime
from flask import Flask, jsonify, request

import base64
import hashlib
import json
from urllib.parse import urlencode
import time

# 添加音频录制相关的常量
CHUNK = 1024  # 每次读取的音频块大小
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 1  # 单声道
RATE = 16000  # 采样率
SILENCE_THRESHOLD = 1000  # 静音阈值
SILENCE_DURATION = 2.0  # 静音持续时间(秒)，用于判断录音结束
MIN_RECORD_TIME = 1.0  # 最短录音时间(秒)
MAX_RECORD_TIME = 10.0  # 最长录音时间(秒)

api_key = "Xg0sa3YWPwLNaNDDE1Oez38W"
secret_key = "9OlM9WnEXVhdm4d6U8LmUiUfXnGb2v9b"

# 添加音频录制函数
from path import AUDIO_RECORDS_DIR

def record_audio_from_headset():
    """
    自动录制耳机麦克风的音频，检测声音的开始和结束
    
    返回:
        保存的音频文件路径
    """
    # 确保保存目录存在
    os.makedirs(AUDIO_RECORDS_DIR, exist_ok=True)
    
    # 生成时间戳文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(AUDIO_RECORDS_DIR, f"audio_{timestamp}.wav")
    
    print(f"准备录制音频，将保存到: {save_path}")
    
    p = pyaudio.PyAudio()
    
    # 获取可用的音频输入设备
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    
    # 查找耳机麦克风设备
    device_index = p.get_default_input_device_info()['index']
    device_info = p.get_device_info_by_index(device_index)
    if device_info.get('maxInputChannels') > 0:
        name = device_info.get('name')
        print(f"找到输入设备: {name}")
    
    # 打开音频流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)
    
    print("开始监听音频输入...")
    
    frames = []  # 存储音频帧
    recording = False  # 是否正在录制
    silent_chunks = 0  # 连续静音块计数
    chunks_per_second = RATE / CHUNK  # 每秒的块数
    silent_chunks_threshold = int(SILENCE_DURATION * chunks_per_second)  # 判断结束的静音块阈值
    min_chunks = int(MIN_RECORD_TIME * chunks_per_second)  # 最短录音块数
    max_chunks = int(MAX_RECORD_TIME * chunks_per_second)  # 最长录音块数
    total_chunks = 0  # 总录制块数
    
    try:
        # 主录音循环
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume_norm = np.abs(audio_data).mean()
            
            # 检测声音开始
            if not recording and volume_norm > SILENCE_THRESHOLD:
                print(f"检测到声音开始，音量: {volume_norm}")
                recording = True
            
            # 如果正在录制，添加音频帧
            if recording:
                frames.append(data)
                total_chunks += 1
                
                # 检测静音
                if volume_norm < SILENCE_THRESHOLD:
                    silent_chunks += 1
                else:
                    silent_chunks = 0  # 重置静音计数
                
                # 检查是否达到最长录音时间
                if total_chunks >= max_chunks:
                    print(f"达到最长录音时间 {MAX_RECORD_TIME} 秒，停止录制")
                    break
                
                # 检查是否达到静音结束条件（且已录制足够长度）
                if silent_chunks >= silent_chunks_threshold and total_chunks > min_chunks:
                    print(f"检测到 {SILENCE_DURATION} 秒静音，停止录制")
                    break
    
    except KeyboardInterrupt:
        print("录音被用户中断")
    except Exception as e:
        print(f"录音过程中出错: {e}")
    finally:
        # 关闭流和PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    # 如果没有录到足够的音频，返回错误
    if not recording or total_chunks < min_chunks:
        print("没有检测到足够的音频输入")
        return None
    
    # 保存录音
    try:
        wf = wave.open(save_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(f"音频已保存到: {save_path}")
        return save_path
    except Exception as e:
        print(f"保存音频文件时出错: {e}")
        return None   
# 添加测试函数
def test_audio_recording():
    """测试音频录制功能"""
    print("开始测试音频录制功能...")
    print("请对着麦克风说话，系统将自动检测声音的开始和结束")
    
    try:
        audio_path = record_audio_from_headset()
        if audio_path:
            print(f"测试成功! 录音已保存到: {audio_path}")
            return audio_path
        else:
            print("录音失败")
            return None
    except Exception as e:
        print(f"测试过程中出错: {e}")
        return None

def baidu_speech_recognition(file_path, dev_pid=1537):
    """
    百度云语音识别函数（短语音识别标准版）
    
    参数:
        file_path: 音频文件路径 (支持pcm/wav/amr格式，16k采样率)
        dev_pid: 语言模型ID（默认1537-普通话输入法模型）
        
    返回:
        {'status': 'success', 'text': 识别文本} 或 {'status': 'error', 'message': 错误信息}
    """
    try:
        # 1. 获取access_token
        auth_url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            'grant_type': 'client_credentials',
            'client_id': api_key,
            'client_secret': secret_key
        }
        response = requests.post(auth_url, params=params)
        access_token = response.json().get('access_token')
        
        if not access_token:
            print("获取access_token失败")  # 打印错误信息，方便调试和定位问题
            return {'status': 'error', 'message': '获取access_token失败'}

        # 2. 读取音频文件
        with open(file_path, 'rb') as f:
            speech_data = base64.b64encode(f.read()).decode('utf-8')
        print("音频文件已读取, 文件路径为：" + file_path)
        
        # 3. 构建请求参数
        post_data = {
            'format': 'wav',  # 根据实际文件类型修改
            'rate': 16000,    # 采样率16k
            'channel': 1,     # 单声道
            'cuid': hashlib.md5(api_key.encode()).hexdigest(), # 唯一标识
            'token': access_token,
            'dev_pid': dev_pid,
            'speech': speech_data,
            'len': os.path.getsize(file_path)
        }
        
        # 4. 发送识别请求
        asr_url = "https://vop.baidu.com/server_api"
        headers = {'Content-Type': "audio/pcm;rate=16000"}
        response = requests.post(asr_url, data=json.dumps(post_data), headers=headers)
        result = response.json()

        # 5. 处理响应
        if result.get('err_no') == 0:
            return {'status': 'success', 'result': result['result'][0]}
        else:
            return {'status': 'error', 'message': f"识别错误[{result['err_no']}]: {result['err_msg']}"}
            
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == "__main__":
    path = '/Users/lss/Desktop/Python/DIP/Backend/audio_records/audio_20250331_204954.wav'
    result = baidu_speech_recognition(path)
    print(result)

    

