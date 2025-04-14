import axios from 'axios';
import { useEffect } from 'react';
import style from "./Home.module.scss";
import backgroundImage from '../../assets/Home/background.webp';
import logo from '../../assets/Home/logo.webp';
import cd from '../../assets/Home/cd.webp';
import face from '../../assets/Home/face.webp';
import headset from '../../assets/Home/headset.webp';
import { useNavigate } from 'react-router-dom';
export default function HomePage() {
    const navigate = useNavigate();
    useEffect(() => {
        axios.get('/api/test')
            .then(response => console.log('后端连接成功:', response.data))
            .catch(error => console.error('连接后端失败:', error));
    }, []);

    return <>
        <div className={style.background} style={{
            backgroundImage: `url(${backgroundImage})`,
        }}>
            <img src={logo} alt="logo" className={style.logo} />
            <div className={style.func}>
                <div className={style.container}>
                    <img src={face} alt="logo" className={style.card} onClick={() => navigate('/emotion')}/>
                    情绪旅程
                </div>
                <div className={style.container}>
                    <img src={cd} alt="logo" className={style.card} style={{width: "77%"}} onClick={() => navigate('/music')}/>
                    音乐中心
                </div>
                <div className={style.container}>
                    <img src={headset} alt="logo" className={style.card} onClick={() => navigate('/recent')}/>
                    月度总结
                </div>
            </div>
        </div>
    </>

}