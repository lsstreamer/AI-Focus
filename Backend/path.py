import os

# 获取项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 后端目录
BACKEND_DIR = os.path.join(ROOT_DIR, 'Backend')

# 数据库目录
DB_DIR = os.path.join(BACKEND_DIR, 'DB')

# 音频相关目录
AUDIO_OUTPUT_DIR = os.path.join(BACKEND_DIR, 'audio_output')
AUDIO_RECORDS_DIR = os.path.join(BACKEND_DIR, 'audio_records')

# 图片相关目录
IMAGES_DIR = os.path.join(BACKEND_DIR, 'images')
COMPUTER_IMAGES_DIR = os.path.join(IMAGES_DIR, 'computer')
SCREENSHOT_IMAGES_DIR = os.path.join(IMAGES_DIR, 'screenshot')
USB_IMAGES_DIR = os.path.join(IMAGES_DIR, 'usb')

# 音乐目录
MUSIC_DIR = os.path.join(BACKEND_DIR, 'music')

# 数据库文件路径
CONVERSATIONS_DB = os.path.join(DB_DIR, 'conversations.db')
ENV_INFO_DB = os.path.join(DB_DIR, 'env_info.db')
SCREENSHOT_INFO_DB = os.path.join(DB_DIR, 'screenshot_info.db')
USER_INFO_DB = os.path.join(DB_DIR, 'user_info.db')
USER_PREFERENCE_DB = os.path.join(DB_DIR, 'user_preference.db')
MUSIC_DB = os.path.join(DB_DIR, 'music.db')