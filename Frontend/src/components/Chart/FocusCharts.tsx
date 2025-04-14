import React from 'react';
import ReactECharts from 'echarts-for-react';
import * as echarts from 'echarts/core';

// 在顶部添加类型导入
import type { EChartsOption, SeriesOption } from 'echarts';

export default function FocusCharts() {
    // 修改 option 定义方式
    const option: EChartsOption = {
        title: {
            text: '最近一周',
            left: 'center',
            top: -5,
            textStyle: {
                color: 'rgb(255, 255, 255)',
                fontSize: 24,
                fontWeight: 'bold',
                textShadowColor: 'rgba(0, 0, 0, 0.5)',  // 阴影颜色
                textShadowBlur: 2,                       // 模糊半径
                textShadowOffsetY: 2                     // 垂直偏移
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            }
        },
        legend: {
            data: ['专注时长', '摸鱼时长'],
            top: 30
        },
        toolbox: {
            feature: {
                saveAsImage: {
                    title: '保存为图片'
                }
            },
            right: 20,
            top: 30
        },
        grid: {
            left: 50,
            right: 50,
            bottom: 50,
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            }
        ],
        yAxis: [
            {
                type: 'value',
                axisLabel: {
                    formatter: '{value}'
                }
            }
        ],
        series: [
            {
                name: '专注时长',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(128, 255, 165)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(1, 191, 236)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: [5, 4, 7, 9, 2, 4, 3]
            },
            {
                name: '摸鱼时长',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                  width: 0
                },
                showSymbol: false,
                areaStyle: {
                  opacity: 0.8,
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    {
                      offset: 0,
                      color: 'rgb(0, 221, 255)'
                    },
                    {
                      offset: 1,
                      color: 'rgb(77, 119, 255)'
                    }
                  ])
                },
                emphasis: {
                  focus: 'series'
                },
                data: [1, 2, 1, 2.3, 3.1, 2.5, 0.6]
              },
        ] as SeriesOption[] // 添加类型断言
    };

    return <ReactECharts
        option={option}
        style={{ height: '110%', width: '110%', position: 'relative', right: '10px', top: '10px' }}
        opts={{ renderer: 'canvas' }}
    />
};