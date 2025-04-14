import axios from 'axios';
import { useEffect, useState } from 'react';
import style from "./Music.module.scss";
import { Modal, TreeSelect, Button, Slider, Row, Col, InputNumber, InputNumberProps, Segmented } from 'antd';
import Menu from '../../components/Menu/Menu';
import backgroundImage from '../../assets/bg.webp';
import person from '../../assets/Music/person.webp';
import arrow from '../../assets/Music/arrow.png';

import Song from '../../components/Song/Song';

export default function Emotion() {
    type Music = {
        id: number,
        name: string,
        is_liked: boolean,
        is_instrumental: boolean,
        path: string,
    }
    const [isSettingOpen, setIsSettingOpen] = useState(false); // 添加模态框状态
    const [musicList, setMusicList] = useState<Music[]>([]); // 添加音乐列表示
    const [playingId, setPlayingId] = useState<number | null>(null); // 新增播放状态

    const GetMusicListFromDB = () => {
        axios.get('/api/get_music_list')
            .then(response => {
                console.log('音乐列表:', JSON.stringify(response.data, null, 2));
                // 新增状态更新
                setMusicList(response.data.music_list.map((item: any) => ({
                    id: item.id,
                    name: item.music_prompt,
                    is_liked: Boolean(item.is_liked),
                    is_instrumental: Boolean(item.is_instrumental),
                    path: item.path
                })));
            })
            .catch(error => {
                console.error('获取音乐列表失败:', error);
            });
    }
    useEffect(() => {
        GetMusicListFromDB();
    }, []);
    return <>
        <div className={style.background} style={{
            backgroundImage: `url(${backgroundImage})`
        }}>
            <Menu selected={1} />
            <img src={person} className={style.person} alt="person" />
            <div className={style.recent}>
                <div className={style.title}>
                    最近播放
                </div>
                <div className={style.songList}>
                    {musicList.map((music, _) => (
                        !music.is_liked &&
                        <Song
                            name={music.is_instrumental ? `[纯音乐] ${music.name}` : music.name}
                            bgColor="#D0D1ED"
                            is_liked={music.is_liked}
                            musicId={music.id}
                            is_playing={playingId === music.id}
                            setPlayingId={setPlayingId}
                        />
                    ))}
                </div>
            </div>
            <div className={style.likeList}>
                <div className={style.title}>
                    点赞列表
                </div>
                <div className={style.songList}>
                    {musicList.map((music, _) => (
                        music.is_liked &&
                        <Song
                            name={music.is_instrumental ? `[纯音乐] ${music.name}` : music.name}
                            bgColor="#DBE9F6"
                            is_liked={music.is_liked}
                            musicId={music.id}
                            is_playing={playingId === music.id}
                            setPlayingId={setPlayingId}
                        />
                    ))}
                </div>
            </div>
            <div className={style.setting} onClick={() => setIsSettingOpen(true)}>
                偏好设置
                <img src={arrow} className={style.arrow} alt="arrow" />
            </div>
            <Modal title="Basic Modal" open={isSettingOpen}
                onOk={() => setIsSettingOpen(false)}
                onCancel={() => setIsSettingOpen(false)}
                modalRender={() => <MusicSettings setModalClosed={() => setIsSettingOpen(false)} />}
                maskClosable={false}
            >
            </Modal>
        </div>
    </>
}

function MusicSettings(props: { setModalClosed: () => void }) {
    const [musicType, setValue] = useState<string>();
    const [intensity, setIntensity] = useState(5);
    const [intervel, setIntervel] = useState<string>('5min');
    const [voiceType, setVoiceType] = useState<string>('男青年');

    const onChangeIntensity: InputNumberProps['onChange'] = (newValue) => {
        setIntensity(newValue as number);
    };
    const onChangeType = (newValue: string) => {
        setValue(newValue);
    };

    const onChangeIntervel = (value: string) => {
        setIntervel(value);
    };

    const onChangeVoiceType = (value: string) => {
        setVoiceType(value);
    }
    const SaveUserPreference = () => {
        const userSettings = {
            musicType: musicType ? musicType : null, // 转换为数组格式，空值转为 null
            intensity,
            intervel,
            voiceType,
        };
        console.log('用户设置:', JSON.stringify(userSettings, null, 2));
        // 在 console.log 之后添加：
        axios.post('/api/save_user_preference', userSettings)
            .then(response => console.log('设置保存成功'))
            .catch(error => console.error('保存失败:', error));
    }

    const OnConfirm = () => {
        SaveUserPreference();
        props.setModalClosed();
    }

    useEffect(() => {
        console.log('用户设置:', JSON.stringify({
            musicType: musicType ? [musicType] : null, // 转换为数组格式，空值转为 null
            intensity,
            intervel,
            voiceType,
        }, null, 2));
    }, [musicType, intensity, intervel, voiceType]);

    const treeData = [
        {
            value: '纯音乐',
            title: '纯音乐',
            children: [
                {
                    value: '交响乐',
                    title: '交响乐',
                },
                {
                    value: '协奏曲',
                    title: '协奏曲',
                },
                {
                    value: '奏鸣曲',
                    title: '奏鸣曲',
                },
                {
                    value: '电子音乐',
                    title: '电子音乐',
                },
                {
                    value: '环境音乐',
                    title: '环境音乐',
                },
                {
                    value: '新世纪音乐',
                    title: '新世纪音乐',
                },
                {
                    value: '电影配乐',
                    title: '电影配乐',
                },
                {
                    value: '轻音乐',
                    title: '轻音乐',
                },
                {
                    value: '爵士乐(纯器乐)',
                    title: '爵士乐(纯器乐)',
                },
                {
                    value: '钢琴/小提琴独奏',
                    title: '钢琴/小提琴独奏',
                },
            ],
        },
        {
            value: '非纯音乐',
            title: '非纯音乐',
            children: [
                {
                    value: '流行音乐',
                    title: '流行音乐',
                },
                {
                    value: '摇滚乐',
                    title: '摇滚乐',
                },
                {
                    value: '说唱/嘻哈',
                    title: '说唱/嘻哈',
                },
                {
                    value: 'R&B(节奏布鲁斯)',
                    title: 'R&B(节奏布鲁斯)',
                },
                {
                    value: '乡村音乐',
                    title: '乡村音乐',
                },
                {
                    value: '爵士乐(人声)',
                    title: '爵士乐(人声)',
                },
                {
                    value: '蓝调',
                    title: '蓝调',
                },
                {
                    value: '民谣',
                    title: '民谣',
                },
                {
                    value: '电子舞曲',
                    title: '电子舞曲',
                },
                {
                    value: '合唱音乐',
                    title: '合唱音乐',
                },
                {
                    value: '歌剧',
                    title: '歌剧',
                },
                {
                    value: '音乐剧',
                    title: '音乐剧',
                },
                {
                    value: '重金属',
                    title: '重金属',
                },
                {
                    value: '民族音乐',
                    title: '民族音乐',
                },
            ],
        },
    ];


    return <div className={style.settingBg}>
        <div className={style.title}>
            偏好设置
        </div>
        <div className={style.content}>
            <div className={style.row}>
                <div style={{ width: "150px" }}>
                    音乐类型
                </div>
                <TreeSelect
                    showSearch
                    style={{ width: '100%' }}
                    value={musicType}
                    dropdownStyle={{ maxHeight: 200, overflow: 'auto' }}
                    placeholder="请选择你喜欢的音乐类型"
                    allowClear
                    multiple
                    onChange={onChangeType}
                    treeData={treeData}
                />
            </div>
            <div className={style.row}>
                <div style={{ width: "150px" }}>
                    手环震动强度
                </div>
                <Row>
                    <Col span={12}>
                        <Slider
                            min={0}
                            max={10}
                            onChange={onChangeIntensity}
                            value={typeof intensity === 'number' ? intensity : 0}
                            style={{
                                width: '330px', // 设置宽度为父容器的80%

                            }}
                            styles={
                                {
                                    track: {
                                        background: "linear-gradient(to right, rgb(197, 110, 255) 0%,  rgb(123, 92, 170) 100%)"
                                    },
                                    rail: {
                                        backgroundColor: '#E5E5E5',
                                    },
                                }
                            }
                        />
                    </Col>
                    <Col span={4}>
                        <InputNumber
                            min={0}
                            max={100}
                            style={{ position: 'relative', left: '160px' }}
                            value={intensity}
                            onChange={onChangeIntensity}
                        />
                    </Col>
                </Row>
            </div>
            <div className={style.row}>
                <div style={{ width: "150px" }}>
                    休息间隔
                </div>
                <Segmented<string>
                    options={['5min', '10min', '15min', '30min', '60min']}
                    onChange={onChangeIntervel}
                />
                <InputNumber
                    min={1}
                    max={24 * 60}
                    style={{ position: 'relative', left: '60px' }}
                    value={Number(intervel.replace(/\D/g, '') || 5)} // 字符串转数字
                    suffix="min"
                    onChange={(value) => {
                        setIntervel(`${value}min`); // 数字转字符串
                    }}
                />
            </div>
            <div className={style.row}>
                <div style={{ width: "150px" }}>
                    语音音色
                </div>
                <Segmented<string>
                    // [4192, 6748, 4288, 6644, 4]
                    options={['男青年', '男中年', '女青年', '女中年', '童声']}
                    onChange={onChangeVoiceType}
                    block
                    style={{ width: '80%' }}
                />
            </div>
            <div className={style.bottom}>
                <Button type="primary" className={style.confirm} onClick={OnConfirm}>确定</Button>
                <Button className={style.cancel} onClick={props.setModalClosed}>取消</Button>
            </div>
        </div>
    </div>
}