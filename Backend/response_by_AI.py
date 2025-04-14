from zhipuai import ZhipuAI
import json
from database import save_conversation, get_latest_data
from tts import text_to_speech
from music import play_sound, AudioPlayer, get_latest_music, create_music_by_sona
from others import clean_json_string
import time

GLM_api_key = "a70ef03eb30b4924adda59520e7ace05.ZzXfzTjGlvU9zfMb"

response_player = AudioPlayer()


def get_speaker():
    last_user_pref_data = get_latest_data("user_preference.db", "user_preference")
    speaker = last_user_pref_data["voice_type"]

    # [4192, 6748, 4288, 6644, 4]
    # options={['男青年', '男中年', '女青年', '女中年', '童声']}
    if speaker == "男青年":
        speaker_id = 4192
    elif speaker == "男中年":
        speaker_id = 6748
    elif speaker == "女青年":
        speaker_id = 4288
    elif speaker == "女中年":
        speaker_id = 6644
    elif speaker == "童声":
        speaker_id = 4
    else:
        speaker_id = 4192
    speaker_id = 4
    return speaker_id


def handle_input(user_input: str, player: AudioPlayer):
    try:
        # 调用 GLM4 大模型接口，获取回答
        client = ZhipuAI(api_key=GLM_api_key)  # 替换为你ZhipuAI的  API Key
        response = client.chat.completions.create(
            model="glm-4-plus",
            messages=[
                {
                    "role": "system",
                    "content": """请分析用户的输入，并严格按照以下JSON格式返回结果。直接返回JSON，不要添加任何其他内容，不要使用markdown格式：
                            {
                                "command": 判断用户输入是否是命令，且命令是否在预设的命令列表中，并返回对应的命令编号。
                                1表示用户输入的命令是“播放音乐”，
                                2表示用户输入的命令是“暂停音乐”，
                                3表示用户输入的命令是“希望新生成一首歌或者音乐”，
                                0表示用户输入的命令不在预设的命令列表中，即不是命令
                                         
                                "feeling": 如果用户的输入不在预设的命令列表中，则返回用户的情绪，否则返回0
                                           1表示愤怒，
                                           2表示开心，
                                           3表示伤心，
                                           4表示中性，
                                           5表示抱怨，
                                "event": 根据用户的话判断用户上发生的事情，如果用户问你问题则直接把问题的内容原封不动地填到这个地方
                            }""",
                },
                {"role": "user", "content": user_input},
            ],
        )
        if response.choices and len(response.choices) > 0:
            GLManswer = response.choices[0].message.content  # 提取回答内容
        else:
            GLManswer = "未获取到有效的回答"

        cleaned_content = clean_json_string(GLManswer)

        print("ChatGLM API返回的JSON数据：")
        print(cleaned_content)

        conversation_data = json.loads(cleaned_content)

        # 解析 JSON 数据，获取命令编号和情绪
        command = conversation_data["command"]
        feeling = conversation_data["feeling"]
        event = conversation_data["event"]

        if command == 0:
            save_conversation(conversation_data)

        # 根据命令编号执行相应的操作
        response_by_AI(command, feeling, event, player)

        return {"status": "success", "message": conversation_data}
    except Exception as e:
        return {"status": "error", "message": "无法获取回答"}


def recoginze_feeling(feeling):
    if feeling == 1:
        return "愤怒"
    elif feeling == 2:
        return "开心"
    elif feeling == 3:
        return "伤心"
    elif feeling == 4:
        return "中性"
    elif feeling == 5:
        return "抱怨"
    else:
        return ""


def response_by_AI(command, feeling, event, player: AudioPlayer):
    if command == 0:
        ChatWithGLM(event)
    if command == 1:
        if not player.audio:
            last_music_path = get_latest_music()
            print(f"🎵 播放最新音频: {last_music_path}")
            play_sound(player, last_music_path)
        else:
            player.play()
    if command == 2:
        player.pause()

    if command == 3:
        SoundTips(tips = "正在为您生成音乐，请等待半分钟……")
        print("🎵 正在为您生成音乐，请等待半分钟……")
        
        prompt, is_instrumental = GenerateMusicPrompt(player, event)
        if prompt!= None and is_instrumental!= None:
            print(f"🎵 生成的prompt为: {prompt}, 是否为纯音乐：{is_instrumental}")
            music_path = create_music_by_sona(prompt, is_instrumental)
            if music_path != None:
                play_sound(player, music_path)

def SoundTips(tips: str):
    save_path = text_to_speech(tips, get_speaker())
    if save_path!= None:
        play_sound(response_player, save_path)

def ChatWithGLM(event):
    try:
        # 调用 GLM4 大模型接口，获取回答
        client = ZhipuAI(api_key=GLM_api_key)  # 替换为你ZhipuAI的  API Key
        response = client.chat.completions.create(
            model="glm-4-plus",
            messages=[
                {
                    "role": "system",
                    "content": """如果用户向你抱怨，请你根据用户最近发生的事和用户的情绪，生成一段对话，与他聊天。
                    如果用户向你询问问题，则解答他的疑惑，使用简短精炼的文字进行回答，不要给出代码块，不需要举例说明。
                    请你直接给出精简的回答（不超过200字，不需要举例说明），其他的文字不需要输出，不要输出任何代码。""",
                },
                {"role": "user", "content": event},
            ],
        )
        if response.choices and len(response.choices) > 0:
            GLManswer = response.choices[0].message.content  # 提取回答内容
        else:
            GLManswer = "未获取到有效的回答"

        print(GLManswer)
        save_path = text_to_speech(GLManswer, get_speaker())
        if save_path != None:
            play_sound(response_player, save_path)

        return {"status": "success", "message": GLManswer}
    except Exception as e:
        return {"status": "error", "message": "无法获取回答"}


def Collect_DB_Data():
    latest_conversation_data = get_latest_data("conversations.db", "conversations")
    lastest_user_pref_data = get_latest_data("user_preference.db", "user_preference")
    lastest_screenshot_data = get_latest_data("screenshot_info.db", "screenshots")
    lastest_user_data = get_latest_data("user_info.db", "user_status")
    return (
        latest_conversation_data["feeling"],
        lastest_user_pref_data["music_type"],
        lastest_screenshot_data["analysis"],
        lastest_user_data["feeling"],
        lastest_user_data["analysis"],
    )


def GenerateMusicPrompt(player: AudioPlayer, tips=""):
    speak_feeling, music_type, work_descriptions, work_feeling, work_feeling_analysis = Collect_DB_Data()
    content = f"""
    我最近的谈话的情绪是:{recoginze_feeling(speak_feeling)}，
    我最近的工作是:{work_descriptions}，
    我最近的工作的情绪是:{work_feeling}，
    我最近的情绪分析是:{work_feeling_analysis}，
    我最喜欢的音乐类型有{music_type}，你从中选一个来生成曲子。
    我期待是音乐是：{tips}
    请你根据我的信息生成一首歌曲的中文的prompt。
    """

    print(content)
    try:
        # 调用 GLM4 大模型接口，获取回答
        client = ZhipuAI(api_key=GLM_api_key)  # 替换为你ZhipuAI的  API Key
        response = client.chat.completions.create(
            model="glm-4-plus",
            messages=[
                {
                    "role": "system",
                    "content": """请根据用户的信息生成一首歌曲的中文的prompt，请你查阅相关资料，尽量让歌曲的风格节奏能够使用户专心工作。
                    prompt的要求：
                    1. prompt的长度不超过30字，且必须为中文
                    2. prompt应该由形容词或者短语通过逗号连接
                    3. prompt的歌曲风格优先考虑“我期待是音乐是”中的内容，如果内容不存在则考虑“我最喜欢的音乐类型有”中的内容
                    请你严格按照以下JSON格式返回结果。直接返回JSON，不要添加任何其他内容，不要使用markdown格式：
                    {
                        is_instrumental: 是否为纯音乐，如果是则为true，否则为false，
                        "prompt": 歌曲的中文的prompt
                    }
                    """,
                },
                {"role": "user", "content": content},
            ],
        )
        if response.choices and len(response.choices) > 0:
            GLManswer = response.choices[0].message.content  # 提取回答内容
        else:
            GLManswer = "未获取到有效的回答"

        cleaned_content = clean_json_string(GLManswer)

        print("ChatGLM API返回的JSON数据：")
        print(cleaned_content)

        prompt_data = json.loads(cleaned_content)
        # 解析 JSON 数据，获取命令编号和情绪
        is_instrumental = prompt_data["is_instrumental"]
        prompt = prompt_data["prompt"]

        return prompt, is_instrumental
    except Exception as e:
        return None
