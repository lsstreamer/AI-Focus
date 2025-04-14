import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import type { ECharts } from 'echarts';

interface BubbleData {
    label: string;
    value: number;
}

const LikeCharts = () => {
    const chartRef = useRef<HTMLDivElement>(null);
    let chartInstance: ECharts | null = null;

    // 初始化图表
    useEffect(() => {
        if (chartRef.current) {
            chartInstance = echarts.init(chartRef.current);
            const demoData: BubbleData[] = [
                { label: "治愈系", value: 15 },
                { label: "快乐", value: 4 },
                { label: "伤感", value: 5 },
                { label: "白噪音", value: 10 },
                { label: "流行乐", value: 3 },
            ];
            chartInstance.setOption(getChartOptions(demoData));
        }

        return () => {
            chartInstance?.dispose();
        };
    }, []);

    // 生成图表配置
    const getChartOptions = (dataList: BubbleData[]) => {
        const maxValue = Math.max(1, ...dataList.map(item => item.value));
        let symbolSize = 120; // 增加基础尺寸
        const dataLength = dataList.length;

        if (dataLength < 3) {
            symbolSize = 180;
        } else if (dataLength < 5) {
            symbolSize = 150;
        }

        const colors = [
            '#E8FFF0', '#DEFFE8', '#D4FFE0', // 绿色系
            '#F0E8FF', '#EBE3FF', '#E6DEFF', // 紫色系
            '#E0E2FF', '#DADDFF', '#D4D8FF', // 蓝紫色系
            '#E0FFF7', '#D2FFF5', '#C4FFF3', // 青色系
            '#D8F0FF', '#C5E7FF', '#B2DEFF'  // 蓝色系
        ];

        return {
            series: [{
                data: dataList.map((item, index) => {
                    const bubbleSize = Math.max(
                        symbolSize * Math.pow(item.value / maxValue, 1.1),
                        80
                    );
                    return {
                        name: item.label,
                        value: item.value,
                        symbolSize: bubbleSize,
                        itemStyle: {
                            color: colors[Math.floor(Math.random() * colors.length)]
                        }
                    };
                }),
                type: 'graph',
                layout: 'force',
                force: {
                    repulsion: symbolSize * 4, // 增加斥力系数
                    gravity: 0.2,           // 中等向心力
                },
                draggable: true,       // 启用拖拽功能
                label: {
                    show: true,
                    position: 'inside',
                    formatter: (params: any) => [
                        `{title|${params.data.name}}`,
                        `{num|${params.data.value}首}`
                    ].join('\n'),
                    rich: {
                        title: {
                            align: 'center',
                            // 改用函数形式获取预存值
                            fontSize: 16,
                            lineHeight: 18,
                            fontWeight: 500,
                            color: '#000'
                        },
                        num: {
                            align: 'center',
                            // 改用函数形式获取预存值
                            fontSize: 12,
                            lineHeight: 21,
                            color: '#666'
                        }
                    }
                },
                itemStyle: {
                    borderWidth: 1,
                    color: function(params: any) {
                        return params.data.itemStyle?.color || colors[0];
                    },
                    // 添加阴影效果
                    shadowBlur: 15,
                    shadowColor: 'rgba(0, 0, 0, 0.15)',
                    shadowOffsetX: 0,
                    shadowOffsetY: 3,

                    emphasis: {
                        scale: 1.1,  // 鼠标悬停时放大1.1倍
                        shadowBlur: 25,  // 增加阴影模糊半径
                        shadowColor: 'rgba(0, 0, 0, 0.25)',  // 加深阴影颜色
                        shadowOffsetX: 0,
                        shadowOffsetY: 5,  // 增加阴影偏移
                    },
                },
            }]
        };
    };

    return (
        <div
            ref={chartRef}
            style={{
                width: '100%',
                height: '290px',
                minHeight: '270px'
            }}
        />
    );
};

export default LikeCharts;