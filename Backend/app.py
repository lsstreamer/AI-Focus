import base64
import os
from flask import Flask, request, jsonify
import requests
import sqlite3
import json
import serial.tools.list_ports
import time
import cv2
from datetime import datetime, timedelta
from PIL import ImageGrab
from zhipuai import ZhipuAI
import threading
import socket


from database import (
    delete_expired_data,
    init_db,
    save_conversation,
    save_user_pref,
    get_data_by_time,
    set_music_state,
    get_music_path_by_id,
    get_latest_data,
    get_music_path_by_random,
)
from music import get_latest_music, AudioPlayer, play_sound, create_music_by_sona
from record import record_audio_from_headset, baidu_speech_recognition
from photo import read_user_image, read_env_image, read_screenshot, capture_screenshot
from others import clean_json_string
from response_by_AI import handle_input, GenerateMusicPrompt, SoundTips

# 从path模块导入图片存储路径常量
from path import (
    COMPUTER_IMAGES_DIR,  # 电脑摄像头图片存储路径
    USB_IMAGES_DIR,  # USB摄像头图片存储路径
    SCREENSHOT_IMAGES_DIR,  # 屏幕截图存储路径
    AUDIO_OUTPUT_DIR,  # 音频输出目录
    AUDIO_RECORDS_DIR,  # 音频输入目录
)

app = Flask(__name__)
init_db()
player = AudioPlayer()


@app.route("/capture_photos", methods=["POST"])
def capture_photos():
    try:
        json = request.get_json()  # 获取请求中的 JSON 数据
        device = json.get("device", "both")  # 默认设备为 "both"
        screenshot = json.get("screenshot", True)  # 默认截屏

        # 使用字典来指定每个设备类型的保存路径
        camera_save_paths = {
            "computer": COMPUTER_IMAGES_DIR,
            "usb": USB_IMAGES_DIR,
        }

        # 初始化变量
        frames = []
        cameras = []
        image_type = []

        # 根据设备类型选择相应的摄像头
        if device == "computer":
            cameras.append(cv2.VideoCapture(0))  # 电脑摄像头
            image_type.append("computer")
        elif device == "usb":
            cameras.append(cv2.VideoCapture(0))  # USB 摄像头
            image_type.append("usb")
        elif device == "both":
            cameras.append(cv2.VideoCapture(0))  # 第一个摄像头
            image_type.append("usb")
            cameras.append(cv2.VideoCapture(1))  # 第二个摄像头
            image_type.append("computer")

        # 检查摄像头是否打开
        for cap in cameras:
            if not cap.isOpened():
                raise Exception("无法打开摄像头")

        time.sleep(0.5)
        # 捕获图像
        for cap in cameras:
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
            cap.release()  # 释放摄像头资源

        if not frames:
            return (
                jsonify({"status": "error", "message": "Failed to capture any photo"}),
                500,
            )

        # 保存图像并返回路径
        image_paths = []

        for i, (frame, cap, device) in enumerate(zip(frames, cameras, image_type)):
            # 为每个摄像头创建一个单独的文件夹，使用字典指定的路径
            save_path_base = camera_save_paths[device]

            # 检查文件夹是否存在，如果不存在就创建
            os.makedirs(save_path_base, exist_ok=True)

            # 为每个图像生成唯一的文件路径
            save_path = (
                f"{save_path_base}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )
            cv2.imwrite(save_path, frame)
            image_paths.append(save_path)

        if screenshot:
            save_path = capture_screenshot()
            if save_path != "Error":
                image_paths.append(save_path)
                image_type.append("screenshot")
            else:
                return (
                    jsonify(
                        {"status": "error", "message": "Failed to capture screenshot"}
                    ),
                    500,
                )

        for image_path, type in zip(image_paths, image_type):
            if type == "computer":
                read_user_image(image_path)
            elif type == "usb":
                read_env_image(image_path)
            elif type == "screenshot":
                read_screenshot(image_path)

        return jsonify({"status": "success", "image_paths": image_paths}), 200

    except Exception as e:
        print("Error capturing photo:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/clear", methods=["POST"])
def clear_data():
    # 获取 JSON 参数中的 day 和 hour
    age_json = request.get_json()  # 获取请求中的 JSON 数据
    days = age_json.get("day", 0)  # 如果没有提供day参数，默认为0天
    hours = age_json.get("hour", 0)  # 如果没有提供hour参数，默认为0小时
    minutes = age_json.get("minute", 0)  # 如果没有提供minute参数，默认为0分钟

    # 计算过期的时间
    expiration_time = datetime.now() - timedelta(
        days=days, hours=hours, minutes=minutes
    )

    # 文件夹路径
    folders_to_clear = [
        COMPUTER_IMAGES_DIR,
        USB_IMAGES_DIR,
        SCREENSHOT_IMAGES_DIR,
        AUDIO_RECORDS_DIR,
        AUDIO_OUTPUT_DIR,
    ]

    # 清除过期图像
    deleted_files = []
    for folder in folders_to_clear:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".mp3") or file.endswith(".wav"):
                    file_path = os.path.join(folder, file)
                    # 获取文件的最后修改时间
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))

                    # 如果文件的最后修改时间超过过期时间，则删除文件
                    if file_mtime < expiration_time:
                        os.remove(file_path)
                        deleted_files.append(file_path)  # 记录已删除的文件路径
                        print(f"Deleted: {file_path}")
        else:
            print(f"Folder {folder} does not exist")

    delete_expired_data(days, hours, minutes)  # 删除数据库中的过期数据
    # 返回删除的信息
    if deleted_files:
        return jsonify(
            {
                "status": "success",
                "message": f"Cleared images older than: {expiration_time}",
                "deleted_files": deleted_files,
            }
        )
    else:
        return jsonify(
            {
                "status": "success",
                "message": f"No files older than {expiration_time} found to delete.",
            }
        )


@app.route("/input", methods=["POST"])
def command_input():
    data = request.json  # 获取用户发送的 JSON 数据
    if not data or "command" not in data:
        return jsonify({"error": "Command is required"}), 400

    command = data["command"]  # 提取用户输入的命令
    print(f"Received command: {command}")
    result = handle_input(command, player)
    if result["status"] == "success":
        return jsonify({"status": "success", "message": result["message"]}), 200
    else:
        return jsonify({"status": "error", "message": "无法识别"}), 400


@app.route("/generate_music_by_prompt", methods=["POST"])
def generate_music():
    data = request.json  # 获取用户发送的 JSON 数据
    if not data or "prompt" not in data:
        return jsonify({"error": "Prompt is required"}), 400

    prompt = data["prompt"]  # 提取用户输入的提示词
    is_instrumental = data.get("is_instrumental", True)  # 是否为纯音乐，默认为 True

    try:
        # 调用 Sona 大模型接口，生成音频
        create_music_by_sona(prompt, is_instrumental)
        return (
            jsonify(
                {
                    "status": "success",
                    "prompt": prompt,
                    "is_instrumental": is_instrumental,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_music_by_DB", methods=["GET"])
def generate_music_by_DB():
    SoundTips("正在为您生成音乐，请等待半分钟……")
    print("🎵 正在为您生成音乐，请等待半分钟……")
    
    prompt, is_instrumental = GenerateMusicPrompt(player)
    if prompt!= None and is_instrumental!= None:
        print(f"🎵 生成的prompt为: {prompt}, 是否为纯音乐：{is_instrumental}")
        music_path = create_music_by_sona(prompt, is_instrumental)
        if music_path != None:
            play_sound(player, music_path)
    
    return jsonify({"status": "success"}), 200


@app.route("/stop", methods=["GET"])
def stop_music():
    """停止播放"""
    try:
        player.stop()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/pause", methods=["GET"])
def pause_music():
    """暂停播放"""
    try:
        player.pause()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/play_lastest", methods=["GET"])
def play_lastest_music():
    """播放最新音频"""
    try:
        last_music_path = get_latest_music()
        print(f"🎵 播放最新音频: {last_music_path}")
        play_sound(player, last_music_path)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/play", methods=["GET"])
def play_music():
    """播放音频"""
    try:
        if not player.audio:
            play_lastest_music()
        else:
            player.resume()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/play_by_id", methods=["POST"])
def play_music_by_id():
    """播放音频"""
    try:
        data = request.json
        if not data or "id" not in data:
            return jsonify({"error": "Path is required"}), 400
        music_id = data["id"]
        path = get_music_path_by_id(music_id)
        play_sound(player, path)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/play_by_random", methods=["GET"])
def play_music_by_random():
    """随机播放音频"""
    try:
        path = get_music_path_by_random()
        play_sound(player, path)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/record", methods=["GET"])
def start_audio_recording():
    """API端点：开始录制音频"""
    try:
        # 在新线程中启动录音，避免阻塞API响应
        def record_thread():
            audio_path = record_audio_from_headset()
            if audio_path:
                print(f"录音完成: {audio_path}")
                print("开始语音识别...")
                result = baidu_speech_recognition(audio_path)
                if result["status"] == "success":
                    print(f"语音识别结果: {result['result']}")
                    handle_input(result["result"], player)
                else:
                    print(f"语音识别失败: {result['message']}")
            else:
                print("录音失败")

        thread = threading.Thread(target=record_thread)
        thread.daemon = True
        thread.start()

        return jsonify({"status": "success", "message": "开始录制音频"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/save_user_preference", methods=["POST"])
def save_user_preference():
    """API端点：保存用户偏好"""
    try:
        # 获取用户偏好数据
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        # 保存用户偏好到数据库
        save_user_pref(data)
        return (
            jsonify(
                {"status": "success", "message": "User preference saved successfully"}
            ),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/get_music_list", methods=["GET"])
def get_music_list():
    """API端点：获取音乐列表"""
    try:
        # 获取音乐列表
        music_list = get_data_by_time("music.db", "music")
        return jsonify({"status": "success", "music_list": music_list}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/set_like_music", methods=["POST"])
def set_like_music():
    """API端点：设置喜欢的音乐"""
    try:
        data = request.json
        if not data or "music_id" not in data:
            return jsonify({"status": "error", "message": "Missing music_id"}), 400
            
        # 调用数据库操作函数
        set_music_state(data["music_id"], data["is_liked"])
        return jsonify({
            "status": "success",
            "message": f"Set music {data['music_id']} liked successfully"
        }), 200
        
    except Exception as e:
        print(f"❌ 设置喜欢状态失败: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"操作失败: {str(e)}"
        }), 500

@app.route("/get_work_time", methods=["GET"])
def get_work_time():
    """API端点：获取学习时间"""
    try:
        work_time_str = get_latest_data("user_preference.db", "user_preference")["intervel"]
        work_time = int(work_time_str.replace('min', ''))  
        
        return jsonify({"status": "success", "work_time": work_time}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route("/get_intensity", methods=["GET"])
def get_intensity():
    """API端点：获取震动强度"""
    try:
        intensity = get_latest_data("user_preference.db", "user_preference")["intensity"]
        return jsonify({"status": "success", "intensity": intensity}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/welcome", methods=["GET"])
def welcome():
    """API端点：欢迎词"""
    try:
        SoundTips("欢迎使用AI Focus，我是您的私人助理，希望你能在工作和学习中收获好心情！")
        return jsonify({"status": "success"}), 200
    except Exception as e:
            return jsonify({"status": "error",}), 500
      
@app.route("/good_bye", methods=["GET"])        
def good_bye():
    """API端点：结束语"""
    try:
        SoundTips("感谢您使用AI focus，期待给您的下次陪伴！")
        return jsonify({"status": "success"}), 200
    except Exception as e:
            return jsonify({"status": "error",}), 500

if __name__ == "__main__":
    init_db()
    # 获取本机局域网 IP
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print(f"Flask 服务器的局域网 IP: http://{local_ip}:8000")
    app.run(debug=True, host="0.0.0.0", port=8000)
