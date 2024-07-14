<template>
    <div>
        <div style="width: 100%">
            <el-collapse v-model="isClsActive">
                <el-collapse-item name="1">
                    <template #title>
                        <div class="collapse-title">
                            <el-icon><i-ep-Histogram /></el-icon>
                            <span class="collapse-title-text">论文统计数据</span>
                        </div>
                    </template>
                    <div style="width: 100%; overflow: hidden; padding: 0 2%">
                        <div class="number-box">
                            <!-- 论文个数 -->
                            <svg
                                t="1716042456541"
                                class="number-box-icon"
                                viewBox="0 0 1024 1024"
                                version="1.1"
                                xmlns="http://www.w3.org/2000/svg"
                                p-id="3259"
                                width="200"
                                height="200"
                            >
                                <path
                                    d="M356.573 768.21h-255.83v-36.537h255.83v-73.55h-255.83v-36.535h255.83v-72.435h-255.83v-37.93h255.83v-71.279h-255.83v-36.536h255.83V183.317H27.631V1024h621.388l0.08-146.741-292.526-0.319V768.21zM795.203 0v219.295h219.334L795.203 0zM760.02 1.355H393.15v839.05h621.388V256.786l-254.516-0.16V1.356z m181.405 693.384H466.26v-35.181h475.166v35.181z m0-109.17H466.26v-37.053h475.166v37.054z m0-146.222v36.535H466.26v-36.535h475.166z"
                                    fill="#eb8e05"
                                    p-id="3260"
                                ></path>
                            </svg>
                            <div class="number-box-content">
                                <span class="number-box-title">论文总数</span>
                                <span class="number-box-digit">
                                    <AnimatedNumber
                                        :from="0"
                                        :to="paperStatistic.paperCnt"
                                        :key="paperStatistic.paperCnt"
                                        fromColor="#44cc00"
                                        toColor="#232323"
                                        easing="easeOutQuad"
                                    >
                                    </AnimatedNumber
                                ></span>
                            </div>
                        </div>
                        <div class="number-box">
                            <!-- 论文个数 -->
                            <svg
                                t="1716042708042"
                                class="number-box-icon"
                                viewBox="0 0 1025 1024"
                                version="1.1"
                                xmlns="http://www.w3.org/2000/svg"
                                p-id="7897"
                                width="200"
                                height="200"
                            >
                                <path
                                    d="M450.87616 529.792L50.23616 339.264a72.448 72.448 0 0 1 0-135.104L450.87616 13.568a144.896 144.896 0 0 1 122.112 0l400.64 190.592a72.448 72.448 0 0 1 0 135.104l-400.64 190.528c-38.72 17.984-83.392 17.984-122.112 0z m61.056 254.912c-29.12 0-57.92-6.72-84.032-19.584L34.81216 569.856a54.4 54.4 0 1 1 48.192-96.896l392.704 195.2c22.912 11.136 49.6 11.136 72.448 0l393.088-195.2a54.4 54.4 0 1 1 48.192 96.896L595.96416 765.12a189.44 189.44 0 0 1-84.032 19.584z m0 229.632a189.44 189.44 0 0 1-84.032-19.52L34.81216 799.552a54.4 54.4 0 1 1 48.192-96.896l392.704 195.2c22.848 11.328 49.6 11.328 72.448 0l393.088-195.2a54.4 54.4 0 1 1 48.192 96.896l-393.472 195.2a189.44 189.44 0 0 1-84.032 19.584z"
                                    fill="#2aa515"
                                    p-id="7898"
                                ></path>
                            </svg>
                            <div class="number-box-content">
                                <span class="number-box-title">论文领域</span>
                                <span class="number-box-digit">
                                    <AnimatedNumber
                                        :from="0"
                                        :to="paperStatistic.subclassCnt"
                                        :key="paperStatistic.subclassCnt"
                                        fromColor="#44cc00"
                                        toColor="#232323"
                                        easing="easeOutQuad"
                                    >
                                    </AnimatedNumber
                                ></span>
                            </div>
                        </div>
                    </div>
                    <div class="chart-box" style="height: 45vh; margin-bottom: 3vh">
                        <div class="chart-box-title" style="flex: 2"><span>各年份论文统计（近五年）</span></div>
                        <div id="paperYearlyChart" class="chart-box-content"></div>
                    </div>
                    <div class="chart-box" style="height: 80vh">
                        <div class="chart-box-title" style="flex: 1"><span>各领域论文统计（近五年）</span></div>
                        <div id="paperClassChart" class="chart-box-content"></div>
                    </div>
                </el-collapse-item>
            </el-collapse>

            <!-- 论文管理 -->
            <div class="paper-manage-container">
                <!-- 标题 -->
                <div class="collapse-title">
                    <el-icon><i-ep-management /></el-icon>
                    <span class="collapse-title-text">论文管理</span>
                </div>
                <!-- 搜索框 -->
                <div class="paper-manage-search">
                    <el-input v-model="keyword" style="width: 18vw" placeholder="输入论文标题" clearable />
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                </div>
                <!-- 表格内容 -->
                <div class="paper-manage-table">
                    <el-table
                        :data="paperData.papers"
                        stripe
                        style="width: 94%; border-top: 1px solid #edebeb; font-size: 15px"
                        size="large"
                        v-loading="isLoading"
                        :header-cell-style="{ 'text-align': 'center' }"
                        :cell-style="{ 'text-align': 'center' }"
                        :default-sort="{ prop: 'publication_date', order: 'descending' }"
                    >
                        <el-table-column label="序号" width="100" type="index"></el-table-column>
                        <el-table-column label="标题">
                            <template v-slot="scope">
                                <el-tooltip class="item" effect="light" :content="scope.row.title" placement="bottom">
                                    <div class="text-left" style="color: #409efe; cursor: pointer">
                                        {{ scope.row.title }}
                                    </div>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                        <el-table-column label="作者" width="220">
                            <template v-slot="scope">
                                <el-tooltip effect="light" :content="scope.row.authors.join(', ')" placement="bottom">
                                    <div class="text-left" style="cursor: pointer">
                                        {{ scope.row.authors.join(', ') }}
                                    </div>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="发表日期"
                            prop="publication_date"
                            width="150"
                            sortable
                        ></el-table-column>
                        <el-table-column label="引用" prop="citation_count" width="120" sortable></el-table-column>
                        <el-table-column label="评分" width="120" sortable>
                            <template v-slot="scope">
                                <div style="cursor: pointer; color: rgb(215, 141, 2)">
                                    {{ scope.row.score }}
                                </div>
                            </template>
                        </el-table-column>
                        <el-table-column label="操作" width="80">
                            <template v-slot="scope">
                                <el-button circle plain type="success" @click="handleView(scope.row)">
                                    <el-icon><i-ep-view></i-ep-view></el-icon>
                                </el-button>
                            </template>
                        </el-table-column>
                        <template v-slot:empty>
                            <el-empty description="没有数据" />
                        </template>
                    </el-table>
                </div>
                <!-- 论文概述 -->
                <el-dialog v-model="paperOutline.visible" width="60vw">
                    <PaperOutline :paperID="paperOutline.paperID"></PaperOutline>
                </el-dialog>
                <!-- 分页组件 -->
                <el-pagination
                    class="paper-manage-pagination"
                    v-model:current-page="currentPage"
                    v-model:page-size="pageSize"
                    :page-sizes="[10, 25, 50, 100]"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="paperData.total"
                />
            </div>
        </div>
    </div>
</template>

<script>
import { getCurrentInstance } from 'vue'
import PaperOutline from './PaperOutline.vue'
import { getPaperList, getPaperOverviewStatistic, getPaperYearlyStatistic, getPaperClassStatistic } from '@/api/paper'
import { ElMessage } from 'element-plus'
export default {
    components: { PaperOutline },
    props: {},
    data() {
        return {
            isClsActive: '1',
            paperStatistic: {
                paperCnt: 0,
                subclassCnt: 0
            },
            paperOutline: {
                visible: false,
                paperID: ''
            },
            paperData: {
                total: 0,
                papers: [
                    {
                        paper_id: '',
                        title: '',
                        authors: [],
                        publication_date: '',
                        journal: null,
                        citation_count: 0,
                        score: 0
                    }
                ]
            },
            keyword: '', // 搜索框信息
            keywordBuffer: '',
            isLoading: false,
            currentPage: 1, // 分页当前页
            pageSize: 10 // 分页大小
        }
    },
    watch: {
        currentPage() {
            this.handleSearch()
        },
        pageSize() {
            this.handleSearch()
        }
    },
    computed: {},
    methods: {
        handleView(item) {
            this.$nextTick(() => {
                this.paperOutline.visible = true
                this.paperOutline.paperID = item.paper_id
            })
        },
        async handleSearch() {
            this.isLoading = true
            await getPaperList({
                keyword: this.keyword,
                page_num: this.currentPage,
                page_size: this.pageSize
            })
                .then((response) => {
                    this.keywordBuffer = this.keyword
                    this.paperData = response.data
                })
                .catch((error) => {
                    ElMessage.error(error.response.data.message)
                })
            this.isLoading = false
        }
    },
    created() {
        this.handleSearch() // 初始化论文搜索列表
        getPaperOverviewStatistic() // 初始化统计数据
            .then((response) => {
                this.paperStatistic.paperCnt = response.data.paper_cnt
                this.paperStatistic.subclassCnt = response.data.subclass_cnt
            })
            .catch((error) => {
                ElMessage.error(error.response.data.message)
            })
    },
    async mounted() {
        let internalInstance = getCurrentInstance()
        let echarts = internalInstance.appContext.config.globalProperties.$echarts
        // 渲染论文领域图表
        const paperClassChart = echarts.init(document.getElementById('paperClassChart'))
        const option1 = {
            legend: {
                left: 'center' // 图例水平居中
            },
            tooltip: {
                trigger: 'axis',
                showContent: true
            },
            dataset: {
                source: []
            },
            xAxis: { type: 'category' },
            yAxis: { gridIndex: 0 },
            grid: { top: '55%' },
            series: []
        }
        await getPaperClassStatistic()
            .then((response) => {
                option1.dataset.source = [response.data.years, ...response.data.data]
                for (let i = 0; i < response.data.data.length; ++i) {
                    option1.series.push({
                        type: 'line',
                        smooth: true,
                        seriesLayoutBy: 'row',
                        emphasis: { focus: 'series' }
                    })
                }
                option1.series.push({
                    type: 'pie',
                    id: 'pie',
                    radius: '35%',
                    center: ['50%', '30%'],
                    emphasis: {
                        focus: 'self'
                    },
                    label: {
                        formatter: '{b}: {@' + response.data.years[1] + '} ({d}%)'
                    },
                    encode: {
                        itemName: 'subclass',
                        value: response.data.years[1],
                        tooltip: response.data.years[1]
                    }
                })
            })
            .catch((error) => {
                ElMessage.error(error.response.data.message)
            })

        paperClassChart.on('updateAxisPointer', function (event) {
            const xAxisInfo = event.axesInfo[0]
            if (xAxisInfo) {
                const dimension = xAxisInfo.value + 1
                paperClassChart.setOption({
                    series: {
                        id: 'pie',
                        label: {
                            formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                        },
                        encode: {
                            value: dimension,
                            tooltip: dimension
                        }
                    }
                })
            }
        })
        paperClassChart.setOption(option1)

        // 渲染各年份论文统计图
        const paperYearlyChart = echarts.init(document.getElementById('paperYearlyChart'))
        const option2 = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            toolbox: {
                feature: {
                    dataView: { show: true, readOnly: false },
                    magicType: { show: true, type: ['line', 'bar'] },
                    restore: { show: true },
                    saveAsImage: { show: true }
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    data: ['2019', '2020', '2021', '2022', '2023'],
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            visualMap: {
                top: 0,
                left: 'center',
                orient: 'horizontal',
                pieces: [
                    {
                        gt: 0,
                        lte: 100,
                        color: '#93CE07'
                    },
                    {
                        gt: 100,
                        lte: 300,
                        color: '#FBDB0F'
                    },
                    {
                        gt: 300,
                        lte: 500,
                        color: '#FC7D02'
                    },
                    {
                        gt: 500,
                        lte: 1000,
                        color: '#FD0100'
                    },
                    {
                        gt: 1000,
                        color: '#AA069F'
                    }
                ],
                outOfRange: {
                    color: '#999'
                }
            },
            series: [
                {
                    name: 'Direct',
                    type: 'bar',
                    barWidth: '60%',
                    data: [1001, 52, 200, 334, 390],
                    label: {
                        show: true,
                        position: 'top'
                    }
                }
            ]
        }
        await getPaperYearlyStatistic()
            .then((response) => {
                option2.xAxis[0].data = response.data.years
                option2.series[0].data = response.data.data
            })
            .catch((error) => {
                ElMessage.error(error.response.data.message)
            })
        paperYearlyChart.setOption(option2)
    }
}
</script>

<style lang="scss" scoped>
.collapse-title {
    display: flex;
    align-items: center;
    font-weight: bold;
    color: rgb(0, 0, 0, 0.6);
    font-size: 16px;
    padding: 10px;
    .collapse-title-text {
        margin-left: 10px;
    }
}
.number-box {
    float: left;
    width: 22%;
    height: 14vh;
    margin-left: 1%;
    margin-right: 1%;
    margin-bottom: 2%;
    margin-top: 1%;
    box-shadow: 0px 0px 3px 1px rgba(0, 0, 0, 0.2);
    .number-box-icon {
        float: left;
        width: 35%;
        height: 100%;
        margin-left: 5%;
    }

    .number-box-content {
        float: right;
        width: 60%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        .number-box-title {
            flex: 2;
            font-size: 20px;
            font-weight: bold;
            padding: 5%;
            border-bottom: 1px solid black;
        }
        .number-box-digit {
            flex: 3;
            margin-top: 5%;
            font-weight: 500;
            font-size: 21px;
        }
    }
}
.chart-box {
    width: 94%;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0px 0px 3px 1px rgba(0, 0, 0, 0.2);
    .chart-box-title {
        display: flex;
        justify-content: center;
        align-items: center;
        span {
            font-size: 20px;
            font-weight: bold;
        }
    }
    .chart-box-content {
        flex: 8;
        width: 95%;
    }
}
.paper-manage-container {
    margin-top: 2vh;
    background-color: white;
    overflow: hidden;
    .paper-manage-search {
        float: right;
        height: 8vh;
        line-height: 8vh;
        padding: 0 3%;
    }
    .paper-manage-table {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    .paper-manage-pagination {
        height: 10vh;
        margin-right: 3%;
        float: right;
    }
}
.text-left {
    text-align: left;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
