import axios from 'axios';
import { useEffect, useState } from 'react';
import style from "./Recent.module.scss";
import { useNavigate } from 'react-router-dom';
import Menu from '../../components/Menu/Menu';
import backgroundImage from '../../assets/bg.webp';
import person from '../../assets/Recent/person.webp';
import weekBg from '../../assets/Recent/weekBg.webp';
import FocusCharts from '../../components/Chart/FocusCharts';
import LikeCharts from '../../components/Chart/LikeCharts';
export default function Emotion() {
    const [cntRecentSongs, setCntRecentSongs] = useState(37);
    const [accompanyTime, setAccompanyTime] = useState<string>("10小时3分钟");
    const [recentStyles, setRecentStyles] = useState<string[]>(["治愈系", "白噪音"]);
    return <>
        <div className={style.background} style={{
            backgroundImage: `url(${backgroundImage})`
        }}>
            <Menu selected={2} />
            <div className={style.focusTime}>
                <FocusCharts />
            </div>
            <img src={person} alt="person" className={style.person} />
            <div className={style.week} style={{ backgroundImage: `url(${weekBg})` }}>
                <div className={style.text}>
                    <span style={{ textAlign: 'center', display: 'block' }}>
                        本周你一共听了<br />
                        <span style={{ color: "#A36AFF", fontSize: "30px" }}>
                            {cntRecentSongs}
                        </span>
                        首音乐<br />
                        AIFocus陪伴了你<br />
                        <span style={{ color: "#A36AFF", fontSize: "30px" }}>
                            {accompanyTime}
                        </span>
                    </span>
                </div>
                <LikeCharts />
                <div className={style.text}>
                <span style={{ textAlign: 'center', display: 'block' }}>
                        这一周，你听的音乐风格多元<br />
                        <span style={{ color: "#97FFDA", fontSize: "30px" }}>
                            {recentStyles[0]}
                        </span>
                        和
                        <span style={{ color: "#97FFDA", fontSize: "30px" }}>
                            {recentStyles[1]}
                        </span>
                        <br />
                        是你本周的最爱
                    </span>
                </div>
            </div>
        </div>
    </>

}