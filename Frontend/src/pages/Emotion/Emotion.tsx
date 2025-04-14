import axios from 'axios';
import { useEffect, useState } from 'react';
import style from "./Emotion.module.scss";
import Menu from '../../components/Menu/Menu';
import Evaluation from '../../components/Evaluation/Evaluation';
import { EmoComposition, EmoFrequency } from '../../components/Chart/EmoCharts';

import backgroundImage from '../../assets/bg.webp';
import data from '../../assets/Emotion/data.webp';
import person from '../../assets/Emotion/person.webp';
import aifocus from '../../assets/Emotion/aifocus.webp';
import textBG from '../../assets/Emotion/textBG.webp';
import happy from '../../assets/Emotion/feeling/happy.webp';
import bored from '../../assets/Emotion/feeling/bored.webp';
import sad from '../../assets/Emotion/feeling/sad.webp';
import angry from '../../assets/Emotion/feeling/angry.webp';
import worried from '../../assets/Emotion/feeling/worried.webp';
export default function Emotion() {
    // 添加类型定义
    type EmotionKey = 'happy' | 'bored' | 'sad' | 'angry' | 'worried';

    const emotionMap = {
        happy: {
            image: happy,
            text: "愉悦"
        },
        bored: {
            image: bored,
            text: "无聊"
        },
        sad: {
            image: sad,
            text: "难过"
        },
        angry: {
            image: angry,
            text: "生气"
        },
        worried: {
            image: worried,
            text: "担忧"
        }
    } as const;

    // 修改 useState 类型
    const [emotion, setEmotion] = useState<EmotionKey>('bored');

    return <>
        <div className={style.background} style={{
            backgroundImage: `url(${backgroundImage})`
        }}>
            <Menu selected={0} />
            <img src={person} className={style.person} alt="person" />
            <div className={style.data}>
                <div className={style.top}>
                    <div className={style.evaluation}>
                        <div className={style.title}>
                            评估结果
                        </div>
                        <div className={style.content}>
                            <Evaluation bgColor="#BDEAC3" dotColor="#5AE46C" cntDot={5} text="专注程度" />
                            <Evaluation bgColor="#BAF2D0" dotColor="#5AE4B4" cntDot={2} text="情绪评分" />
                            <Evaluation bgColor="#BAF2E7" dotColor="#31DECA" cntDot={7} text="工作压力" />
                            <Evaluation bgColor="#BAEBF2" dotColor="#31C4DE" cntDot={4} text="工作环境" />
                        </div>
                    </div>
                    <div className={style.state}>
                        <div className={style.title}>
                            您的状态
                        </div>
                        <div className={style.content}>
                            <div className={style.image}>
                                <img src={emotionMap[emotion].image} alt='emotion' className={style.emotion} />
                                <img src={aifocus} alt='aifocus' className={style.ai} />
                            </div>
                            <div className={style.text} style={{
                                backgroundImage: `url(${textBG})`
                            }}>
                                {emotionMap[emotion].text} · 听音乐中
                            </div>
                        </div>
                    </div>

                </div>
                <div className={style.bottom} style={{ backgroundImage: `url(${data})` }}>
                    <div className={style.charContainer}>
                        <EmoComposition />
                    </div>
                    <div className={style.charContainer}>
                        <EmoFrequency />
                    </div>
                </div>
            </div>
        </div>
    </>

}