import { AiOutlineHeart, AiFillHeart } from "react-icons/ai"; // 引入爱心图标
import style from "./Song.module.scss";
import { use, useEffect, useState } from "react"; // 添加状态管理

// 在顶部新增图标引入
import { MdPlayArrow, MdPause } from "react-icons/md";
import axios from "axios";

export default function Song(props: {
    name: string;
    bgColor: string;
    is_liked: boolean;
    musicId: number;
    is_playing: boolean;
    setPlayingId: React.Dispatch<React.SetStateAction<number | null>>;
}) {
    const [isLiked, setIsLiked] = useState(false);

    // 新增播放控制函数
    const handlePlay = () => {
        const newPlayState = !props.is_playing;
        props.setPlayingId(props.musicId);
        // 发送播放控制请求
        if (newPlayState) {
            axios.post('/api/play_by_id', { id: props.musicId })
                .then(response => {
                    if (response.data.status !== 'success') {
                        // 操作失败时回滚状态
                        props.setPlayingId(null);
                        console.error('操作失败:');
                    }
                })
        }
        else {
            props.setPlayingId(null);
            axios.get('/api/pause')
                .then(response => {
                    if (response.data.status !== 'success') {  // 添加严格相等运算符
                        props.setPlayingId(props.musicId);
                        console.error('操作失败');
                    }
                })
                .catch(error => {  // 新增错误处理
                    props.setPlayingId(props.musicId);
                    console.error('请求失败:', error);
                });
        }
    };

    const handleLike = () => {
        // 先切换本地状态提供即时反馈
        const newLikeState = !isLiked;
        setIsLiked(newLikeState);

        // 调用点赞API
        axios.post('/api/set_like_music', { music_id: props.musicId, is_liked: newLikeState })
            .then(response => {
                if (response.data.status !== 'success') {
                    // 操作失败时回滚状态
                    setIsLiked(!newLikeState);
                    console.error('操作失败:', response.data.message);
                }
            })
            .catch(error => {
                // 网络错误时回滚状态
                setIsLiked(!newLikeState);
                console.error('请求失败:', error);
            });
    };

    useEffect(() => {
        setIsLiked(props.is_liked);
    }, [])

    return <>
        <div className={style.background} style={{ backgroundColor: props.bgColor }}>
            <div className={style.name}>
                {props.name}
            </div>
            {props.is_playing ? (
                <MdPause color="#937BFF" size={25} onClick={handlePlay} className={style.playIcon} />
            ) : (
                <MdPlayArrow color="#666" size={25} onClick={handlePlay} className={style.playIcon} />
            )}
            {isLiked ? (
                <AiFillHeart color="#ff4d4f" size={25} onClick={handleLike} className={style.heartIcon} />
            ) : (
                <AiOutlineHeart color="#666" size={25} onClick={handleLike} className={style.heartIcon} />
            )}
        </div>
    </>
}