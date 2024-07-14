<template>
    <div style="width: 100%; height: 100%">
        <!-- 统计数据 -->
        <el-collapse v-model="isClsActive">
            <el-collapse-item name="1">
                <template #title>
                    <div class="collapse-title">
                        <el-icon><i-ep-Histogram /></el-icon>
                        <span class="collapse-title-text">用户统计数据</span>
                    </div>
                </template>
                <!-- 统计数字框 -->
                <div style="width: 100%; overflow: hidden; padding: 0 2%">
                    <div class="number-box">
                        <!-- 用户个数 -->
                        <svg
                            t="1715522008378"
                            class="number-box-icon"
                            viewBox="0 0 1024 1024"
                            version="1.1"
                            xmlns="http://www.w3.org/2000/svg"
                            p-id="1642"
                            width="200"
                            height="200"
                        >
                            <path d="M502.9 501.67z" p-id="1643" fill="#1296db"></path>
                            <path
                                d="M240.14 316.3a164.63 178.53 0 1 0 329.26 0 164.63 178.53 0 1 0-329.26 0Z"
                                p-id="1644"
                                fill="#1296db"
                            ></path>
                            <path
                                d="M502.9 501.67c-28.32 21.94-62 34.65-98.13 34.65S335 523.6 306.65 501.67C183.37 551.28 94.49 691.77 94.49 857.36q0 14.57 0.9 28.87h618.77q0.9-14.42 0.9-28.87c0-165.59-88.88-306.09-212.16-355.69zM591.64 346.58a160.39 160.39 0 0 1-5.64 43.19 157.47 157.47 0 0 1-47 75.36c22.38 49.4 70.66 83.62 126.64 83.62 77.31 0 140-65.17 140-145.56S743 257.62 665.69 257.62a135.79 135.79 0 0 0-83.08 28.44 78.94 78.94 0 0 1 9.06 26.81c1.7 11.21 2.19 22.94-0.03 33.71z"
                                p-id="1645"
                                fill="#1296db"
                            ></path>
                            <path
                                d="M749.12 559.11c-24.07 18.65-52.71 29.46-83.43 29.46a128.93 128.93 0 0 1-23.39-2.17c28.18 23.15 46.62 63.51 60.44 100.54 7.06 17.47 13.13 35.56 18.75 53.36 12.75 40.41 21.3 85.47 16.61 128.45 0.45 5.77 0.75 11.55 0.86 17.32h189.79q0.77-12.15 0.77-24.54c-0.01-140.78-75.58-260.25-180.4-302.42z"
                                p-id="1646"
                                fill="#1296db"
                            ></path>
                        </svg>
                        <div class="number-box-content">
                            <span class="number-box-title">用户总数</span>
                            <span class="number-box-digit"
                                ><AnimatedNumber
                                    :from="0"
                                    :to="userStatistic.userCnt"
                                    :key="userStatistic.userCnt"
                                    fromColor="#44cc00"
                                    toColor="#232323"
                                    easing="easeOutQuad"
                                ></AnimatedNumber
                            ></span>
                        </div>
                    </div>
                    <div class="number-box">
                        <!-- 用户文件个数 -->
                        <svg
                            t="1715522664977"
                            class="number-box-icon"
                            viewBox="0 0 1024 1024"
                            version="1.1"
                            xmlns="http://www.w3.org/2000/svg"
                            p-id="8262"
                            width="200"
                            height="200"
                        >
                            <path
                                d="M815.104 69.632q27.648 25.6 44.032 42.496t25.088 28.672 10.752 19.968 2.048 14.336l0 16.384-151.552 0q-10.24 0-17.92-7.68t-12.8-17.92-7.68-20.992-2.56-16.896l0-126.976 3.072 0q8.192 0 16.896 2.56t19.968 9.728 28.16 20.48 42.496 35.84zM640 129.024q0 20.48 6.144 42.496t19.456 40.96 33.792 31.232 48.128 12.288l149.504 0 0 577.536q0 29.696-11.776 53.248t-31.232 39.936-43.008 25.6-46.08 9.216l-503.808 0q-19.456 0-42.496-11.264t-43.008-29.696-33.28-41.984-13.312-49.152l0-696.32q0-21.504 9.728-44.544t26.624-42.496 38.4-32.256 45.056-12.8l391.168 0 0 128zM704.512 768q26.624 0 45.056-18.944t18.432-45.568-18.432-45.056-45.056-18.432l-384 0q-26.624 0-45.056 18.432t-18.432 45.056 18.432 45.568 45.056 18.944l384 0zM768 448.512q0-26.624-18.432-45.568t-45.056-18.944l-384 0q-26.624 0-45.056 18.944t-18.432 45.568 18.432 45.056 45.056 18.432l384 0q26.624 0 45.056-18.432t18.432-45.056z"
                                p-id="8263"
                                fill="#d81e06"
                            ></path>
                        </svg>
                        <div class="number-box-content">
                            <span class="number-box-title">用户文件总数</span>
                            <span class="number-box-digit"
                                ><AnimatedNumber
                                    :from="0"
                                    :to="userStatistic.documentCnt"
                                    :key="userStatistic.documentCnt"
                                    fromColor="#44cc00"
                                    toColor="#232323"
                                    easing="easeOutQuad"
                                ></AnimatedNumber
                            ></span>
                        </div>
                    </div>
                </div>
                <!-- 统计图表 -->
                <div class="chart-box">
                    <div class="chart-box-title"><span>新增用户数量统计（近十月）</span></div>
                    <div id="newUsersChart" class="chart-box-content"></div>
                </div>
            </el-collapse-item>
        </el-collapse>

        <!-- 用户管理 -->
        <div class="user-manage-container">
            <!-- 标题 -->
            <div class="collapse-title">
                <el-icon><i-ep-management /></el-icon>
                <span class="collapse-title-text">用户管理</span>
            </div>
            <!-- 搜索框 -->
            <div class="user-manage-search">
                <el-input v-model="keyword" style="width: 18vw" placeholder="输入用户名" clearable />
                <el-button type="primary" @click="handleSearch">搜索</el-button>
            </div>
            <!-- 表格内容 -->
            <div class="user-manage-table">
                <el-table
                    :data="userData.users"
                    stripe
                    :default-sort="{ prop: 'registration_date', order: 'descending' }"
                    style="width: 94%; border-top: 1px solid #edebeb; font-size: 15px"
                    size="large"
                    v-loading="isLoading"
                    :header-cell-style="{ 'text-align': 'center' }"
                    :cell-style="{ 'text-align': 'center' }"
                >
                    <el-table-column label="序号" width="100" type="index"> </el-table-column>
                    <el-table-column label="用户名">
                        <template v-slot="scope">
                            <el-tooltip effect="light" :content="scope.row.username" placement="bottom">
                                <div style="color: #409efe; cursor: pointer">
                                    {{ scope.row.username }}
                                </div>
                            </el-tooltip>
                        </template>
                    </el-table-column>
                    <el-table-column label="注册时间" prop="registration_date" sortable></el-table-column>
                    <el-table-column label="操作" width="250">
                        <template #default="{ row }">
                            <el-button circle plain type="danger" @click="handleEdit(row)">
                                <el-icon><i-ep-Edit></i-ep-Edit></el-icon>
                            </el-button>
                            <el-button circle plain type="success" @click="handleView(row)">
                                <el-icon><i-ep-view></i-ep-view></el-icon
                            ></el-button>
                        </template>
                    </el-table-column>
                    <template #empty>
                        <el-empty description="没有数据" />
                    </template>
                </el-table>
            </div>
            <!-- 用户资料 -->
            <el-dialog v-model="userProfile.visible" width="42vw">
                <UserProfile :username="userProfile.username"></UserProfile>
            </el-dialog>
            <!-- 分页组件 -->
            <el-pagination
                class="user-manage-pagination"
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 25, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="userData.total"
            />
        </div>
    </div>
</template>

<script>
import { getCurrentInstance, ref } from 'vue'
import UserProfile from './UserProfile.vue'
import { getUserList, getUserOverviewStatistic, getUserMonthlyStatistic } from '@/api/user'
import { ElMessage } from 'element-plus'

export default {
    components: {
        UserProfile
    },
    props: {},
    data() {
        return {
            isClsActive: '1', //折叠框
            userStatistic: ref({
                // 统计数字板
                userCnt: 0,
                documentCnt: 0
            }),
            userProfile: {
                // 用户详情弹窗
                visible: false,
                username: ''
            },
            keyword: '', // 用户搜索框信息
            keywordBuffer: '',
            isLoading: false,
            userData: {
                total: 0,
                users: []
            },
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
    created() {
        this.handleSearch() // 初始化用户搜索列表
        getUserOverviewStatistic().then((response) => {
            this.userStatistic.documentCnt = response.data.document_cnt
            this.userStatistic.userCnt = response.data.user_cnt
        })
    },
    async mounted() {
        // 渲染图表
        let internalInstance = getCurrentInstance()
        let echarts = internalInstance.appContext.config.globalProperties.$echarts
        const newUsersChart = echarts.init(document.getElementById('newUsersChart'))
        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    crossStyle: {
                        color: '#888'
                    }
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
            legend: {
                data: ['用户月增量', '平台用户总数']
            },
            xAxis: [
                {
                    type: 'category',
                    data: ['2023-11', '2023-12', '2024-1', '2024-2', '2024-3', '2024-4', '2024-5', '2024-6'],
                    axisPointer: {
                        type: 'shadow'
                    }
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: '用户月增',
                    min: 0,
                    max: 100,
                    interval: 20,
                    axisLabel: {
                        formatter: '{value} 人'
                    }
                },
                {
                    type: 'value',
                    name: '用户总数',
                    min: 0,
                    max: 25,
                    interval: 5,
                    axisLabel: {
                        formatter: '{value} 人'
                    }
                }
            ],
            series: [
                {
                    name: '用户月增量',
                    type: 'bar',
                    tooltip: {
                        valueFormatter: function (value) {
                            return value + ' 人'
                        }
                    },
                    itemStyle: {
                        color: '#077aea'
                    },
                    data: [1, 2, 4, 7, 23, 25, 76, 13, 16, 3, 2, 6, 3]
                },
                {
                    name: '平台用户总数',
                    type: 'line',
                    yAxisIndex: 1,
                    tooltip: {
                        valueFormatter: function (value) {
                            return value + ' 人'
                        }
                    },
                    itemStyle: {
                        color: '#e87d04'
                    },
                    data: [1, 2, 2, 3, 5, 6, 10, 20, 23, 25, 40, 50, 61]
                }
            ]
        }
        // 获取实时数据
        await getUserMonthlyStatistic().then((response) => {
            // 坐标轴设置
            option.xAxis[0].data = response.data.months
            option.yAxis[0].max = response.data.user_addition.max
            option.yAxis[0].interval = option.yAxis[0].max / 5
            option.yAxis[1].max = response.data.user_total.max
            option.yAxis[1].interval = option.yAxis[1].max / 5
            // 数据
            option.series[0].data = response.data.user_addition.data
            option.series[1].data = response.data.user_total.data
        })
        // 设置实例参数
        newUsersChart.setOption(option)
        window.addEventListener('resize', function () {
            newUsersChart.resize()
        })
    },
    methods: {
        handleView(item) {
            this.userProfile.username = item.username
            this.$nextTick(() => {
                this.userProfile.visible = true
            })
        },
        async handleSearch() {
            this.isLoading = true
            await getUserList({
                keyword: this.keyword,
                page_num: this.currentPage,
                page_size: this.pageSize
            })
                .then((response) => {
                    this.keywordBuffer = this.keyword
                    this.userData = response.data
                })
                .catch((error) => {
                    ElMessage.error(error.response.data.message)
                })
            this.isLoading = false
        }
    }
}
</script>

<style lang="scss" scoped>
.collapse-title {
    display: flex;
    align-items: center;
    color: rgb(0, 0, 0, 0.6);
    font-size: 16px;
    font-weight: 700;
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
    height: 45vh;
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
        flex: 2;
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
.user-manage-container {
    margin-top: 2vh;
    background-color: white;
    overflow: hidden;
    .user-manage-search {
        float: right;
        height: 8vh;
        line-height: 8vh;
        padding: 0 3%;
    }
    .user-manage-table {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    .user-manage-pagination {
        height: 10vh;
        margin-right: 3%;
        float: right;
    }
}
</style>
