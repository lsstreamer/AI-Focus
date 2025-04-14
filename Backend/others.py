import json
def clean_json_string(content):
    """清理JSON字符串，移除markdown格式等"""
    # 移除markdown代码块标记
    content = content.replace('```json', '').replace('```', '').strip()
    return content 