import sqlite3
from datetime import datetime, timedelta
import os
from path import (
    DB_DIR,
    ENV_INFO_DB,
    CONVERSATIONS_DB,
    USER_PREFERENCE_DB,
    USER_INFO_DB,
    SCREENSHOT_INFO_DB,
    MUSIC_DB,
)
import json

DATABASES = [
    (
        "screenshot_info.db",
        """CREATE TABLE IF NOT EXISTS screenshots (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                activity_type TEXT NOT NULL,
                                applications TEXT NOT NULL,
                                task_description TEXT NOT NULL,
                                analysis TEXT NOT NULL)""",
    ),
    (
        "env_info.db",
        """CREATE TABLE IF NOT EXISTS env_status (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                env_type TEXT NOT NULL,
                                is_alone TEXT NOT NULL,
                                is_bright TEXT NOT NULL,
                                is_comfortable TEXT NOT NULL,
                                analysis TEXT NOT NULL)""",
    ),
    (
        "user_info.db",
        """CREATE TABLE IF NOT EXISTS user_status (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                is_working TEXT NOT NULL,
                                is_talking TEXT NOT NULL,
                                is_listening TEXT NOT NULL,
                                feeling TEXT NOT NULL,
                                analysis TEXT NOT NULL)""",
    ),
    (
        "conversations.db",
        """CREATE TABLE IF NOT EXISTS conversations(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                            command INTEGER NOT NULL,
                            feeling INTEGER NOT NULL,
                            event TEXT NOT NULL)""",
    ),
    (
        "user_preference.db",
        """CREATE TABLE IF NOT EXISTS user_preference (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                music_type TEXT,       
                                intensity INTEGER,     
                                intervel TEXT,          
                                voice_type TEXT)""",
    ),
    (
        "music.db",
        """CREATE TABLE IF NOT EXISTS music (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                path TEXT NOT NULL,      
                                music_prompt TEXT NOT NULL, 
                                is_instrumental INTEGER CHECK(is_instrumental IN (0, 1)),
                                is_liked INTEGER CHECK(is_liked IN (0, 1)) )""",
    ),
]


def init_db():
    for db_name, create_table_sql in DATABASES:
        with sqlite3.connect(os.path.join(DB_DIR, db_name)) as conn:
            cursor = conn.cursor()
            # 设置时区为北京时间（UTC+8）
            cursor.execute("PRAGMA timezone='Asia/Shanghai'")
            cursor.execute("SELECT datetime('now', 'localtime')")
            cursor.execute(create_table_sql)
            conn.commit()


def save_env_info(env_data):
    """将环境分析数据存入数据库"""
    try:
        conn = sqlite3.connect(ENV_INFO_DB)
        cursor = conn.cursor()

        # 确保表存在
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS env_status (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp DATETIME NOT NULL,
                            env_type TEXT NOT NULL,
                            is_alone TEXT CHECK(is_alone IN ('是', '否')) NOT NULL,
                            is_bright TEXT CHECK(is_bright IN ('是', '否')) NOT NULL,
                            is_comfortable TEXT CHECK(is_comfortable IN ('是', '否')) NOT NULL,
                            analysis TEXT NOT NULL)"""
        )

        # 插入数据
        cursor.execute(
            """INSERT INTO env_status (timestamp, env_type, is_alone, is_bright, is_comfortable, analysis) 
                          VALUES (?, ?, ?, ?, ?, ?)""",
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                env_data["env_type"],
                env_data["is_alone"],
                env_data["is_bright"],
                env_data["is_comfortable"],
                env_data["analysis"],
            ),
        )

        conn.commit()
        conn.close()
        print("✅ 环境信息已成功存入数据库！")

    except Exception as e:
        print(f"❌ 存储环境信息失败: {str(e)}")


def save_screenshot_info(screenshot_data):
    """将电脑屏幕截图数据存入数据库"""
    try:
        conn = sqlite3.connect(SCREENSHOT_INFO_DB)
        cursor = conn.cursor()

        applications_json = (
            json.dumps(screenshot_data["applications"])
            if screenshot_data["applications"]
            else None
        )
        # 确保表存在
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS screenshots (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp DATETIME NOT NULL,
                            activity_type TEXT NOT NULL,
                            applications TEXT NOT NULL,
                            task_description TEXT NOT NULL,
                            analysis TEXT NOT NULL)"""
        )

        # 插入数据
        cursor.execute(
            """INSERT INTO screenshots (timestamp, activity_type, applications, task_description, analysis) 
                          VALUES (?, ?, ?, ?, ?)""",
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                screenshot_data["activity_type"],
                applications_json,
                screenshot_data["task_description"],
                screenshot_data["analysis"],
            ),
        )

        conn.commit()
        conn.close()
        print("✅ 屏幕截图信息已成功存入数据库！")

    except Exception as e:
        print(f"❌ 存储屏幕截图信息失败: {str(e)}")


def save_user_info(user_data):
    """将用户状态信息存入数据库"""
    try:
        conn = sqlite3.connect(USER_INFO_DB)
        cursor = conn.cursor()

        # 确保表存在
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS user_status (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp DATETIME NOT NULL,
                            is_working TEXT NOT NULL,
                            is_talking TEXT NOT NULL,
                            is_listening TEXT NOT NULL,
                            feeling TEXT NOT NULL,
                            analysis TEXT NOT NULL)"""
        )

        # 插入数据
        cursor.execute(
            """INSERT INTO user_status (timestamp, is_working, is_talking, is_listening, feeling, analysis) 
                          VALUES (?, ?, ?, ?, ?, ?)""",
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_data["is_working"],
                user_data["is_talking"],
                user_data["is_listening"],
                user_data["feeling"],
                user_data["analysis"],
            ),
        )

        conn.commit()
        conn.close()
        print("✅ 用户状态信息已成功存入数据库！")

    except Exception as e:
        print(f"❌ 存储用户状态信息失败: {str(e)}")


def save_conversation(conversation_data):
    """将对话信息存入数据库"""
    try:
        # 连接到 SQLite 数据库
        conn = sqlite3.connect(CONVERSATIONS_DB)
        cursor = conn.cursor()

        # 确保表存在
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS conversations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp DATETIME NOT NULL,
                            command INTEGER NOT NULL,
                            feeling INTEGER NOT NULL,
                            event TEXT NOT NULL)"""
        )

        # 插入数据
        cursor.execute(
            """INSERT INTO conversations (timestamp, command, feeling, event) 
                          VALUES (?, ?, ?, ?)""",
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                conversation_data["command"],
                conversation_data["feeling"],
                conversation_data["event"],
            ),
        )

        # 提交事务
        conn.commit()

        # 关闭连接
        conn.close()

        print("✅ 对话信息已成功存入数据库！")

    except Exception as e:
        print(f"❌ 存储对话信息失败: {str(e)}")


def save_user_pref(pref_data):
    try:
        conn = sqlite3.connect(USER_PREFERENCE_DB)
        cursor = conn.cursor()

        # 转换数组为 JSON 字符串
        music_json = (
            json.dumps(pref_data["musicType"], ensure_ascii=False) if pref_data["musicType"] else None
        )
        cursor.execute(
            """INSERT INTO user_preference 
                            (timestamp, music_type, intensity, intervel, voice_type) 
                            VALUES (?, ?, ?, ?, ?)""",
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                music_json,
                pref_data["intensity"],
                pref_data["intervel"],
                pref_data["voiceType"],
            ),
        )
        conn.commit()
        print("✅ 用户偏好设置已存储")
    except Exception as e:
        print(f"❌ 存储失败: {str(e)}")
    finally:
        conn.close()

def save_music_info(music_data):
    """将音乐生成记录存入数据库"""
    try:
        conn = sqlite3.connect(MUSIC_DB)
        cursor = conn.cursor()

        # 插入数据（使用参数化查询防止SQL注入）
        cursor.execute(
            """INSERT INTO music 
               (timestamp, path, music_prompt, is_instrumental, is_liked) 
               VALUES (?, ?, ?, ?, ?)""",  # 新增name和is_instrumental字段
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                music_data["path"],  
                music_data["music_prompt"],
                1 if music_data["is_instrumental"] else 0,  # 转换乐器类型标识
                1 if music_data["is_liked"] else 0
            ),
        )
        
        conn.commit()
        print("✅ 音乐记录已成功存入数据库！")  # 修改提示语更准确
    except Exception as e:
        print(f"❌ 存储音乐记录失败: {str(e)}")  # 修改错误提示
    finally:
        if conn:
            conn.close()
            
def set_music_state(music_id, is_liked):
    """设置音乐喜欢状态（True=喜欢，False=取消）"""
    try:
        print(f"尝试设置音乐ID {music_id} 的喜欢状态为 {is_liked}")
        conn = sqlite3.connect(MUSIC_DB)
        cursor = conn.cursor()
        # 将布尔值转换为整数
        cursor.execute(
            "UPDATE music SET is_liked = ? WHERE id = ?", 
            (int(is_liked), music_id)  # 添加int()转换
        )
        conn.commit()
        print(f"✅ 音乐已成功{'喜欢' if is_liked else '取消喜欢'}！")
    except Exception as e:
        print(f"❌ 设置喜欢状态失败: {str(e)}")
    finally:
        if conn:
            conn.close()

def get_music_path_by_id(music_id):
    """根据音乐ID获取音乐文件路径"""
    try:
        conn = sqlite3.connect(MUSIC_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT path FROM music WHERE id =?", (music_id,))
        result = cursor.fetchone()
        if result:
            print(f"✅ 找到音乐ID {music_id} 的路径: {result[0]}")
            return result[0]  # 返回路径
        else:
            return None  # 如果没有找到，返回None
    except Exception as e:
        print(f"❌ 获取音乐路径失败: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
            
def get_music_path_by_random():
    """随机获取一首音乐文件路径"""
    try:
        conn = sqlite3.connect(MUSIC_DB)
        cursor = conn.cursor()
        # 使用RANDOM()函数随机排序并获取第一条记录
        cursor.execute("SELECT path FROM music ORDER BY RANDOM() LIMIT 1")
        result = cursor.fetchone()
        if result:
            print(f"✅ 随机获取到音乐路径: {result[0]}")
            return result[0]  # 返回路径
        else:
            print("⚠️ 音乐库中没有音乐")
            return None
    except Exception as e:
        print(f"❌ 随机获取音乐路径失败: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
            
def delete_expired_data(day, hour, minute):
    # 计算过期时间点
    cutoff_time = datetime.now() - timedelta(days=day, hours=hour, minutes=minute)
    cutoff_time_str = cutoff_time.strftime("%Y-%m-%d %H:%M:%S")  # 转换为字符串格式

    # 需要删除数据的表
    tables = [
        ("screenshot_info.db", "screenshots"),
        ("env_info.db", "env_status"),
        ("user_info.db", "user_status"),
        ("conversations.db", "conversations"),
    ]

    # 删除过期数据
    for db_name, table_name in tables:
        try:
            with sqlite3.connect(os.path.join(DB_DIR, db_name)) as conn:
                cursor = conn.cursor()
                delete_sql = f"DELETE FROM {table_name} WHERE timestamp < ?"
                cursor.execute(delete_sql, (cutoff_time_str,))
                conn.commit()
                print(f"✅ 已从 {table_name} 表中删除过期数据")
        except Exception as e:
            print(f"❌ 删除 {table_name} 表中的过期数据失败: {str(e)}")


def get_latest_data(db_name, table_name):
    """获取指定数据库表的最新一条记录
    参数：
        db_name: 数据库文件名 (如: 'conversations.db')
        table_name: 表名 (如: 'conversations')
    返回：
        包含最新记录的字典（无数据时返回None）
    """
    try:
        conn = sqlite3.connect(os.path.join(DB_DIR, db_name))
        conn.row_factory = sqlite3.Row  # 使查询结果可通过列名访问
        cursor = conn.cursor()

        # 使用参数化查询防止SQL注入
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()

        # 将Row对象转换为字典
        return dict(row) if row else None

    except sqlite3.Error as e:
        print(f"❌ 查询 {table_name} 表失败: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()

def get_data_by_time(db_name, table_name, start_time = None, end_time = None):
    """获取指定数据库表在指定时间范围内的数据
    参数：
        db_name: 数据库文件名 (如: 'conversations.db')
        table_name: 表名 (如: 'conversations')
        start_time: 开始时间 (格式: 'YYYY-MM-DD HH:MM:SS')
        end_time: 结束时间 (格式: 'YYYY-MM-DD HH:MM:SS')
    返回：
        包含查询结果的列表（无数据时返回空列表）
    """
    try:
        conn = sqlite3.connect(os.path.join(DB_DIR, db_name))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 构建基础查询语句
        query = f"SELECT * FROM {table_name}"
        params = []

        # 添加时间条件
        if start_time or end_time:
            query += " WHERE "
            conditions = []
            if start_time:
                conditions.append("timestamp >= ?")
                params.append(start_time)
            if end_time:
                conditions.append("timestamp <= ?")
                params.append(end_time)
            query += " AND ".join(conditions)

        # 执行参数化查询
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        # 转换为字典列表
        return [dict(row) for row in rows] if rows else []

    except sqlite3.Error as e:
        print(f"❌ 查询 {table_name} 表失败: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()
            