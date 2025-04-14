import { useNavigate } from "react-router-dom";
import style from "./Menu.module.scss";
import logo from "../../assets/Menu/small_logo.webp";


export default function Menu(props: { selected: number }) {
    const navigate = useNavigate();

    return <>
        <div className={style.topBar}>
            <div className={style.logoContainer} onClick={() => navigate('/')}>
                <img className={style.logo} src={logo} alt="logo" />
            </div>
            <div className={style.menu}>
                <div className={style.container}
                    onClick={() => { if (props.selected !== 0) navigate('/emotion') }}
                    style={{
                        background: props.selected === 0 ?
                            'linear-gradient(180deg, #E2FFD1 0%, #E6FF93 100%)' :
                            'transparent'
                    }}
                >
                    情绪旅程
                </div>
                <div className={style.container}
                    onClick={() => { if (props.selected !== 1) navigate('/music') }}
                    style={{
                        background: props.selected === 1 ?
                            'linear-gradient(180deg, #DAF1FF 0%, #A1DDFF 100%)' :
                            'transparent'
                    }}
                >
                    音乐中心
                </div>
                <div className={style.container}
                    onClick={() => { if (props.selected !== 2) navigate('/recent') }}
                    style={{
                        background: props.selected === 2 ?
                            'linear-gradient(180deg, #DADDFF 0%, #D8C4FF 100%)' :
                            'transparent'
                    }}
                >
                    每周总结
                </div>
            </div>
        </div>
    </>
}

