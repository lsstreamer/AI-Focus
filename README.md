
# AI-Focus · 智能专注耳机

AI-Focus 是一款智能专注助手应用，旨在帮助用户在工作和学习过程中保持专注、提升效率，并打造沉浸式的专注体验。

## 项目亮点

- 用户状态监测：通过摄像头实时分析专注度与情绪状态  
- 环境分析：评估工作环境的舒适度、亮度与私密性  
- 屏幕活动分析：识别当前屏幕行为类型与使用应用  
- AI音乐生成：根据情绪和偏好动态生成个性化音乐  
- 语音交互：支持语音指令与反馈（语音识别 & 合成）  
- 数据统计与可视化：展示用户专注时间、音乐偏好、使用模式等

## 技术架构

### 前端（Frontend）
- 框架：React + TypeScript
- 样式管理：SCSS
- 可视化：图表组件展示专注数据与用户行为

### 后端（Backend）
- 框架：Python Flask
- 数据库：SQLite
- AI集成：
  - 图像分析：智谱 GLM-4V
  - 语音处理：百度语音识别 & 合成
  - 音乐生成：Sona AI

## 项目结构

```
AI-Focus/
├── Backend/                # 后端服务
│   ├── app.py              # Flask 主程序
│   ├── database.py         # SQLite 操作
│   ├── music.py            # 音乐生成与播放
│   ├── photo.py            # 用户状态分析
│   ├── record.py           # 音频录制与识别
│   ├── response_by_AI.py   # AI 对话逻辑
│   └── tts.py              # 文字转语音（TTS）
├── Frontend/               # 前端项目
│   ├── src/                # 源代码
│   │   ├── components/     # 公共组件
│   │   ├── pages/          # 页面结构
│   │   └── assets/         # 图片、样式等静态资源
│   └── public/             # 公共资源
└── README.md               # 项目说明文档
```

## 依赖说明（部分）

- React / TypeScript / SCSS
- Flask / Flask-CORS
- Baidu Speech API
- 智谱AI API
- Sona 音乐生成 API
