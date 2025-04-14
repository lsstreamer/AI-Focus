import React from 'react';
import ReactECharts from 'echarts-for-react';
import * as echarts from 'echarts';
// 在顶部类型引入部分添加 RadarSeriesOption
import type {
    PieSeriesOption,
    RadarSeriesOption, // 新增雷达图类型
    TitleComponentOption,
    LegendComponentOption,
    TooltipComponentOption,
    GridComponentOption
} from 'echarts';

// 更新类型组合
type ECOption = echarts.ComposeOption<
    | PieSeriesOption
    | RadarSeriesOption // 添加雷达图类型
    | TitleComponentOption
    | LegendComponentOption
    | TooltipComponentOption
    | GridComponentOption
>;


export function EmoComposition() {
    const option: ECOption = {
        title: {
            text: '情绪组成',
            left: 'center',
            textStyle: {
                color: 'rgba(238, 249, 255, 0.9)',
                fontSize: 24,
                fontWeight: 'bold',
                textShadowColor: 'rgba(0, 0, 0, 0.5)',  // 阴影颜色
                textShadowBlur: 2,                       // 模糊半径
                textShadowOffsetY: 2                     // 垂直偏移
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },

        toolbox: {
            show: true,
            feature: {
                mark: { show: true },
                dataView: { show: false },
                restore: { show: false },
                saveAsImage: {
                    show: true,
                    name: '情绪组成图',      // 自定义保存文件名
                    type: 'png',            // 指定保存格式
                    title: '保存为图片',      // 鼠标悬停提示文本
                    pixelRatio: 2           // 高清导出
                }
            }
        },
        series: [
            {
                name: '情绪占比',
                type: 'pie',
                radius: [12, 80],
                center: ['50%', '50%'],
                roseType: 'area',
                itemStyle: {
                    borderRadius: 5
                },
                label: {
                    color: '#666', // 文字颜色
                    formatter: ({ name, percent }) => {
                        return `{b|${name}}\n${Math.round(percent!)}%`;
                    },
                    rich: {
                        b: {
                            fontSize: 16,
                            lineHeight: 25,
                            fontWeight: 600,
                            color: '#937BFF'
                        }
                    }
                },
                labelLine: {
                    show: true,
                    length: 5,    // 引导线第一段长度
                    length2: 20,  // 引导线第二段长度
                    lineStyle: {
                        width: 1.5,
                        type: 'dashed'
                    }
                },
                data: [
                    { value: 60, name: '愉悦' },
                    { value: 20, name: '担忧' },
                    { value: 26, name: '愤怒' },
                    { value: 45, name: '伤心' },
                    { value: 22, name: '无聊' },

                ]
            }
        ]
    };

    return <ReactECharts
        option={option}
        style={{ height: '100%', width: '100%' }}
    />;
}

export function EmoFrequency() {
    const option: ECOption = {
        color: ['#67F9D8', '#FFE434', '#56A3F1', '#FF917C'],
        title: {
            text: '情绪频率',
            left: 'center',
            textStyle: {
                color: 'rgba(238, 249, 255, 0.9)',
                fontSize: 24,
                fontWeight: 'bold',
                textShadowColor: 'rgba(0, 0, 0, 0.5)',  // 阴影颜色
                textShadowBlur: 2,                       // 模糊半径
                textShadowOffsetY: 2                     // 垂直偏移
            }
        },
        legend: {},
        radar: [
            {
                indicator: [
                    { text: '愉悦', max: 100 },
                    { text: '担忧', max: 100 },
                    { text: '愤怒', max: 100 },
                    { text: '伤心', max: 100 },
                    { text: '无聊', max: 100 }
                ],
                center: ['50%', '50%'],
                radius: 75,
                startAngle: 90,
                splitNumber: 4,
                shape: 'circle',
                axisName: {
                    formatter: '{value}',
                    // 正确的位置应该在axisName对象内部
                    color: 'rgba(184, 253, 248, 0.8)',
                    fontSize: 16,
                    fontWeight: 600,
                },
                splitArea: {
                    areaStyle: {
                        color: ['#77EADF', '#26C3BE', '#64AFE9', '#428BD4'],
                        shadowColor: 'rgba(0, 0, 0, 0.2)',
                        shadowBlur: 10
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(211, 253, 250, 0.8)'
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: 'rgba(211, 253, 250, 0.8)'
                    }
                }
            }
        ],
        toolbox: {
            show: true,
            feature: {
                mark: { show: true },
                dataView: { show: false },
                restore: { show: false },
                saveAsImage: {
                    show: true,
                    name: '情绪频率图',      // 自定义保存文件名
                    type: 'png',            // 指定保存格式
                    title: '保存为图片',      // 鼠标悬停提示文本
                    pixelRatio: 2           // 高清导出
                }
            }
        },
        series: [
            {
                type: 'radar',
                name: '情绪频率', // 添加必需的名称字段
                emphasis: {
                    lineStyle: {
                        width: 4
                    }
                },
                data: [
                    {
                        // 数据值数组，按顺序对应：[愉悦, 担忧, 愤怒, 伤心, 无聊]的情绪频率值
                        value: [60, 45, 80, 70, 30], 
                        areaStyle: {
                            color: 'rgba(255, 228, 52, 0.6)'
                        }
                    }
                ]
            }
        ]
    };

    return <ReactECharts
        option={option}
        style={{ height: '105%', width: '100%', marginLeft: '-40px' }}
    />;
}