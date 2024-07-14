<template>
    <div class="home-page">
        <!-- Web 服务器相关信息 -->
        <div class="web-server" v-loading="loading.webServerLoading">
            <div class="visit-record">
                <div class="title">网站访问统计(近五天)</div>
                <div style="height: 85%" id="web-server-visit"></div>
            </div>
            <div class="hardware">
                <div class="title">Web 服务器</div>
                <div class="cpu-info">
                    <div id="web-server-cpu" style="height: 80%"></div>
                    <div style="height: 15%; text-align: center">CPU 使用情况</div>
                </div>
                <div class="memory-info">
                    <el-progress
                        style="width: 90%; margin: 5% auto; height: 10%"
                        :text-inside="true"
                        :stroke-width="18"
                        :percentage="webServerMemUtilization"
                        status="warning"
                    />
                    <div style="text-align: center">
                        内存使用情况：
                        {{ (webServerInfo.memory_info.used_memory / (1024 * 1024 * 1024)).toFixed(2) }}GB /
                        {{ (webServerInfo.memory_info.total_memory / (1024 * 1024 * 1024)).toFixed(2) }}GB
                    </div>
                </div>
            </div>
        </div>

        <!-- 大模型服务器相关信息 -->
        <div class="module-server" v-loading="loading.moduleServerLoading">
            <div class="header">模型服务器</div>
            <div class="container">
                <div class="hardware-left">
                    <el-card v-for="gpu in moduleServerInfo.gpu_info" :key="gpu.id" class="gpu-card" shadow="hover">
                        <div class="gpu-card-content">
                            <h3>{{ gpu.name }}</h3>
                            <el-row>
                                <el-col :span="8" class="info-item">
                                    <el-icon><i-ep-cpu></i-ep-cpu></el-icon>
                                    <strong>负载：</strong> {{ gpu.load }}%
                                </el-col>
                                <el-col :span="8" class="info-item">
                                    <el-icon><i-ep-sunrise></i-ep-sunrise></el-icon>
                                    <strong>温度：</strong> {{ gpu.temperature }}°C
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="8" class="info-item">
                                    <el-icon><i-ep-files></i-ep-files></el-icon>
                                    <strong>显存总量：</strong> {{ gpu.memory_total }} MB
                                </el-col>
                                <el-col :span="8" class="info-item">
                                    <el-icon><i-ep-check></i-ep-check></el-icon>
                                    <strong>可使用显存：</strong> {{ gpu.memory_free }} MB
                                </el-col>
                                <el-col :span="8" class="info-item">
                                    <el-icon><i-ep-box></i-ep-box></el-icon>
                                    <strong>已使用显存：</strong> {{ gpu.memory_used }} MB ({{
                                        usedMemoryPercentage(gpu)
                                    }}%)
                                </el-col>
                            </el-row>
                        </div>
                    </el-card>
                </div>
                <div class="hardware-right">
                    <div class="cpu-info">
                        <div id="module-server-cpu" style="height: 80%"></div>

                        <div style="height: 15%; text-align: center">CPU 使用情况</div>
                    </div>
                    <div class="memory-info">
                        <el-progress
                            style="width: 90%; margin: 5% auto; height: 10%"
                            :text-inside="true"
                            :stroke-width="18"
                            :percentage="moduleServerMemUtilization"
                            status="warning"
                        />
                        <div style="text-align: center">
                            内存使用情况：
                            {{ (moduleServerInfo.memory_info.used_memory / (1024 * 1024 * 1024)).toFixed(2) }}GB /
                            {{ (moduleServerInfo.memory_info.total_memory / (1024 * 1024 * 1024)).toFixed(2) }}GB
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import { getCurrentInstance } from 'vue'
import { getWebServerStatus, getModuleServerStatus, getVisitStatistic } from '@/api/server'

export default {
    components: {},
    data() {
        return {
            webServerInfo: {
                cpu_info: {
                    cpu_usage: [],
                    cpu_count: 1,
                    cpu_count_logical: 1
                },
                memory_info: {
                    total_memory: 1,
                    used_memory: 1,
                    available_memory: 1,
                    total_swap: 1,
                    used_swap: 1,
                    free_swap: 1
                },
                gpu_info: [
                    {
                        id: 1,
                        name: '',
                        load: 1,
                        memory_total: 1,
                        memory_used: 1,
                        memory_free: 1,
                        temperature: 1
                    }
                ]
            },
            moduleServerInfo: {
                cpu_info: {
                    cpu_usage: [],
                    cpu_count: 1,
                    cpu_count_logical: 1
                },
                memory_info: {
                    total_memory: 1,
                    used_memory: 1,
                    available_memory: 1,
                    total_swap: 1,
                    used_swap: 1,
                    free_swap: 1
                },
                gpu_info: [
                    {
                        id: 1,
                        name: '',
                        load: 1,
                        memory_total: 1,
                        memory_used: 1,
                        memory_free: 1,
                        temperature: 1
                    }
                ]
            },
            loading: {
                webServerLoading: false,
                moduleServerLoading: false
            }
        }
    },
    computed: {
        webServerCPUUtilization() {
            // web服务器CPU平均使用率
            let utilization = 0.0
            for (let use of this.webServerInfo.cpu_info.cpu_usage) {
                utilization += use
            }

            return (utilization / this.webServerInfo.cpu_info.cpu_count_logical).toFixed(2)
        },
        webServerMemUtilization() {
            // web 服务器内存使用
            return (
                (this.webServerInfo.memory_info.used_memory / this.webServerInfo.memory_info.total_memory) *
                100
            ).toFixed(2)
        },
        moduleServerCPUUtilization() {
            // 模型服务器CPU平均使用率
            let utilization = 0.0
            for (var use of this.webServerInfo.cpu_info.cpu_usage) {
                utilization += use
            }
            return (utilization / this.moduleServerInfo.cpu_info.cpu_count_logical).toFixed(2)
        },
        moduleServerMemUtilization() {
            // 模型服务器内存使用
            return (
                (this.moduleServerInfo.memory_info.used_memory / this.moduleServerInfo.memory_info.total_memory) *
                100
            ).toFixed(2)
        }
    },
    methods: {
        usedMemoryPercentage(gpu) {
            return ((gpu.memory_used / gpu.memory_total) * 100).toFixed(2)
        }
    },
    async mounted() {
        let internalInstance = getCurrentInstance()
        let echarts = internalInstance.appContext.config.globalProperties.$echarts
        // loading 效果
        this.loading.webServerLoading = true
        this.loading.moduleServerLoading = true
        // Web 服务器访问统计
        let visitData = []
        await getVisitStatistic()
            .then((response) => {
                visitData = response.data.hours.map((hour, index) => {
                    return [new Date(hour).getTime(), response.data.data[index]]
                })
            })
            .catch((error) => {
                ElMessage.error(error.response.data.message)
            })
        const webServerVisitChart = echarts.init(document.getElementById('web-server-visit'))
        const webServerVisitOption = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%']
                }
            },
            toolbox: {
                feature: {
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'time',
                boundaryGap: false
            },
            yAxis: {
                type: 'value',
                boundaryGap: [0, '100%']
            },
            dataZoom: [
                {
                    type: 'inside',
                    start: 0,
                    end: 100
                },
                {
                    start: 0,
                    end: 20,
                    height: 20,
                    handleSize: '80%', // 缩放手柄的大小
                    handleStyle: {
                        color: '#6AB1D7'
                    }
                }
            ],
            series: [
                {
                    name: '用户访问量',
                    type: 'line',
                    smooth: true,
                    symbol: 'none',
                    areaStyle: {
                        color: 'rgba(144,238,144,0.2)'
                    },
                    lineStyle: {
                        color: 'rgba(100,200,140)'
                    },
                    data: visitData
                }
            ]
        }
        webServerVisitOption && webServerVisitChart.setOption(webServerVisitOption)

        // Web 服务器 CPU
        const webServerCPUChart = echarts.init(document.getElementById('web-server-cpu'))
        const webServerCPUOption = {
            tooltip: {
                formatter: '{a} <br/>{b} : {c}%'
            },
            series: [
                {
                    name: 'Pressure',
                    type: 'gauge',
                    radius: '90%', // 增加仪表盘的半径以填充更多空间
                    progress: {
                        show: true
                    },
                    detail: {
                        valueAnimation: true,
                        formatter: '{value}%',
                        // 修改字体大小
                        fontSize: 13
                    },
                    axisLabel: {
                        fontSize: 10
                    },
                    title: {
                        fontSize: 13
                    },
                    data: [
                        {
                            value: 0
                        }
                    ]
                }
            ]
        }
        await getWebServerStatus()
            .then((response) => {
                this.webServerInfo = response.data
                webServerCPUOption.series[0].data[0].value = this.webServerCPUUtilization
                this.loading.webServerLoading = false
            })
            .catch((error) => {
                ElMessage.error(error.response.data.message)
            })
        webServerCPUOption && webServerCPUChart.setOption(webServerCPUOption)

        // 模型服务器 CPU
        const moduleServerCPUChart = echarts.init(document.getElementById('module-server-cpu'))
        const moduleServerCPUOption = {
            tooltip: {
                formatter: '{a} <br/>{b} : {c}%'
            },
            series: [
                {
                    name: 'Pressure',
                    type: 'gauge',
                    radius: '90%',
                    progress: {
                        show: true,
                        itemStyle: {
                            color: '#B22222'
                        }
                    },
                    detail: {
                        valueAnimation: true,
                        formatter: '{value}%',
                        // 修改字体大小
                        fontSize: 13
                    },
                    axisLabel: {
                        fontSize: 10
                    },
                    title: {
                        fontSize: 13
                    },
                    data: [
                        {
                            value: 0,
                            itemStyle: {
                                color: '#B22222'
                            }
                        }
                    ]
                }
            ]
        }
        await getModuleServerStatus()
            .then((response) => {
                this.moduleServerInfo = response.data
                moduleServerCPUOption.series[0].data[0].value = this.moduleServerCPUUtilization
                this.loading.moduleServerLoading = false
            })
            .catch((error) => {
                ElMessage.error(error.response.data.message)
            })
        moduleServerCPUOption && moduleServerCPUChart.setOption(moduleServerCPUOption)

        // 页面适应
        window.addEventListener('resize', function () {
            webServerCPUChart.resize()
            webServerVisitChart.resize()
            moduleServerCPUChart.resize()
        })
    }
}
</script>
<style lang="scss" scoped>
.home-page {
    width: 100%;
    background-color: white;
}
.web-server {
    height: 55vh;
    min-height: 270px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    padding: 10px 10px;
    background-color: rgb(249, 240, 227, 0.3);
    .visit-record {
        flex: 7;
        height: 50vh;
        border-right: solid 1px rgba(0, 0, 0, 0.2);
        padding-right: 10px;
        .title {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #303133;
        }
    }

    .hardware {
        flex: 2;
        height: 50vh;
        font-size: 14px;
        font-weight: bold;
        display: flex;
        color: rgba(0, 0, 0, 0.5);
        flex-direction: column;
        .title {
            flex: 1;
            text-align: center;
            font-size: 20px;
            color: #303133;
        }
        .cpu-info {
            flex: 6;
        }
        .memory-info {
            flex: 2;
        }
    }
}

.module-server {
    height: 50vh;
    min-height: 250px;
    padding: 20px 10px;
    background-color: rgb(245, 249, 240);
    .header {
        font-size: 20px;
        font-weight: bold;
        color: #303133;
        text-align: center;
    }
    .container {
        margin-top: 10px;
        display: flex;
        flex-direction: row;
        .hardware-left {
            flex: 7;
            border-right: solid 1px rgba(0, 0, 0, 0.2);
            .gpu-card {
                background-color: rgb(241, 248, 252);
                width: 100%;
                transition: all 0.3s;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }

            .gpu-card-content {
                display: flex;
                flex-direction: column;
                gap: 16px;
            }

            .gpu-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }

            .info-item {
                display: flex;
                align-items: center;
                gap: 5px;
            }

            .el-icon {
                font-size: 18px;
                color: #b22222;
            }
        }

        .hardware-right {
            flex: 2;
            height: 45vh;
            font-size: 14px;
            font-weight: bold;
            display: flex;
            color: rgba(0, 0, 0, 0.5);
            flex-direction: column;

            .title {
                flex: 1;
                text-align: center;
                font-size: 20px;
                color: #303133;
            }
            .cpu-info {
                flex: 3;
            }
            .memory-info {
                flex: 1;
            }
        }
    }
}

.loading-card {
    background-color: transparent;
}
</style>
