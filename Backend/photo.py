import base64
import os
import json
from datetime import datetime
import requests
import platform
import pyautogui
from others import clean_json_string
from database import save_env_info, save_screenshot_info, save_user_info
from path import SCREENSHOT_IMAGES_DIR

ZHIPU_API_KEY = "a70ef03eb30b4924adda59520e7ace05.ZzXfzTjGlvU9zfMb"
ZHIPU_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


def read_env_image(image_path):
    try:
        print("\n开始处理图片...")

        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ZHIPU_API_KEY}",
        }

        prompt = """请分析这张办公场景环境图片，并严格按照以下JSON格式返回结果。直接返回JSON，不要添加任何其他内容，不要使用markdown格式：
                    {
                        "env_type": "工作环境，如：办公室/图书馆/会议室/家中/商场/室外等",
                        "is_alone": "是否独处，如：是/否",
                        "is_bright": "是否明亮，如：是/否",
                        "is_comfortable": "是否舒适，如：是/否",
                        "analysis": "你的具体分析和判断依据"
                    }"""

        data = {
            "model": "glm-4v",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            "temperature": 0.3,
            "top_p": 0.8,
            "max_tokens": 1000,
        }

        print(f"正在发送请求到ChatGLM API...，图片路径为：{image_path}")
        response = requests.post(ZHIPU_URL, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]

                try:
                    cleaned_content = clean_json_string(content)
                    print("ChatGLM API返回的JSON数据：")
                    print(cleaned_content)
                    env_data = json.loads(cleaned_content)
                    save_env_info(env_data)
                except json.JSONDecodeError:
                    print("❌ 无法解析API返回的JSON数据")
                    return {"status": "error", "message": "无法解析JSON数据"}

                return {"status": "success", "data": content}
            else:
                error_msg = f"无法解析API响应: {json.dumps(result, ensure_ascii=False, indent=2)}"
                print(f"❌ {error_msg}")
                return {"status": "error", "message": error_msg}
        else:
            error_msg = f"API请求失败: HTTP {response.status_code} - {response.text}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}

    except Exception as e:
        error_msg = f"分类过程中发生错误: {str(e)}"
        print(f"❌ {error_msg}")
        return {"status": "error", "message": error_msg}


def read_screenshot(image_path):
    try:
        print("\n开始处理图片...")

        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ZHIPU_API_KEY}",
        }

        prompt = """请分析这张屏幕截图，并严格按照以下JSON格式返回结果。直接返回JSON，不要添加任何其他内容，不要使用markdown格式：
                {
                    "activity_type": "工作或活动的类型，如：编程/文本工作/网页浏览/数据分析/图像编辑等",
                    "applications": "屏幕上看到的主要应用程序、工具或网站名称, 请以字符串列表的格式给我返回，以英文逗号分隔，如：['VS Code', 'Chrome', 'Notion']",
                    "task_description": "用户正在进行的具体任务描述",
                    "analysis": "你的具体分析和判断依据"
                }"""

        data = {
            "model": "glm-4v",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            "temperature": 0.3,
            "top_p": 0.8,
            "max_tokens": 1000,
        }

        print(f"正在发送请求到ChatGLM API...，图片路径为：{image_path}")
        response = requests.post(ZHIPU_URL, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]

                try:
                    cleaned_content = clean_json_string(content)

                    print("ChatGLM API返回的JSON数据：")
                    print(cleaned_content)

                    screen_data = json.loads(cleaned_content)
                    save_screenshot_info(screen_data)
                except json.JSONDecodeError:
                    print("❌ 无法解析API返回的JSON数据")
                    return {"status": "error", "message": "无法解析JSON数据"}

                return {"status": "success", "data": content}
            else:
                error_msg = f"无法解析API响应: {json.dumps(result, ensure_ascii=False, indent=2)}"
                print(f"❌ {error_msg}")
                return {"status": "error", "message": error_msg}
        else:
            error_msg = f"API请求失败: HTTP {response.status_code} - {response.text}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}

    except Exception as e:
        error_msg = f"分类过程中发生错误: {str(e)}"
        print(f"❌ {error_msg}")
        return {"status": "error", "message": error_msg}


def read_user_image(image_path):
    try:
        print("\n开始处理图片...")

        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ZHIPU_API_KEY}",
        }

        prompt = """请分析这张用户工作图，并严格按照以下JSON格式返回结果。直接返回JSON，不要添加任何其他内容，不要使用markdown格式：
                {
                    "is_working": "用户是否集中注意力，如：是/否"，由于我使用电脑摄像头拍摄用户，如果用户看着前方，可以判断在工作,
                    "is_talking": "用户是否在说话，如：是/否",
                    "is_listening": "用户是否在听音乐，如：是/否",
                    "feeling": "根据用户的表情来判断用户心情，如：开心/伤心/紧张/放松/急躁等",
                    "analysis": "你的具体分析和判断依据"
                }"""

        data = {
            "model": "glm-4v",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            "temperature": 0.3,
            "top_p": 0.8,
            "max_tokens": 1000,
        }

        print(f"正在发送请求到ChatGLM API...，图片路径为：{image_path}")
        response = requests.post(ZHIPU_URL, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]

                try:
                    cleaned_content = clean_json_string(content)

                    print("ChatGLM API返回的JSON数据：")
                    print(cleaned_content)

                    user_data = json.loads(cleaned_content)
                    save_user_info(user_data)
                except json.JSONDecodeError:
                    print("❌ 无法解析API返回的JSON数据")
                    return {"status": "error", "message": "无法解析JSON数据"}

                return {"status": "success", "data": content}, 200
            else:
                error_msg = f"无法解析API响应: {json.dumps(result, ensure_ascii=False, indent=2)}"
                print(f"❌ {error_msg}")
                return {"status": "error", "message": error_msg}
        else:
            error_msg = f"API请求失败: HTTP {response.status_code} - {response.text}"
            print(f"❌ {error_msg}")
            return {"status": "error", "message": error_msg}

    except Exception as e:
        error_msg = f"分类过程中发生错误: {str(e)}"
        print(f"❌ {error_msg}")
        return {"status": "error", "message": error_msg}


def capture_screenshot():
    """截取电脑屏幕并保存到 images/screenshot 目录"""

    # 确保目录存在
    save_dir = SCREENSHOT_IMAGES_DIR
    os.makedirs(save_dir, exist_ok=True)

    # 生成时间戳文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(save_dir, f"{timestamp}.png")

    try:
        if platform.system() == "Darwin":  # macOS
            # macOS上使用 pyobjc-framework-Quartz 或 pyautogui
            screenshot = pyautogui.screenshot()  # 使用 pyautogui 截屏
            screenshot.save(save_path)  # 保存截图

        elif platform.system() == "Windows":  # Windows
            from PIL import ImageGrab

            screenshot = ImageGrab.grab()  # Windows使用ImageGrab截屏
            screenshot.save(save_path)  # 保存截图

        else:
            raise Exception("不支持的操作系统")

        return save_path

    except Exception as e:
        return "Error"
