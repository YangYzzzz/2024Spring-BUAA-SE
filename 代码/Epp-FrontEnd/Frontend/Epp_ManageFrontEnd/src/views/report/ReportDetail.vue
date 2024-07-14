<template>
    <div style="padding: 5px">
        <div class="report-card">
            <el-card class="report-content" shadow="hover">
                <div>
                    <el-descriptions title="评论信息" :column="1" border>
                        <el-descriptions-item label="评论用户">
                            {{ reportData.comment.user.user_name }}
                        </el-descriptions-item>
                        <el-descriptions-item label="评论日期">
                            {{ reportData.comment.date }}
                        </el-descriptions-item>
                        <el-descriptions-item label="评论内容">
                            {{ reportData.comment.content }}
                        </el-descriptions-item>
                    </el-descriptions>
                    <el-divider></el-divider>
                    <el-descriptions title="相关论文" :column="1" border>
                        <el-descriptions-item label="论文ID">
                            {{ reportData.comment.paper.paper_id }}
                        </el-descriptions-item>
                        <el-descriptions-item label="论文标题">
                            {{ reportData.comment.paper.title }}
                        </el-descriptions-item>
                    </el-descriptions>
                    <el-divider></el-divider>
                    <el-descriptions title="举报信息" :column="1" border>
                        <el-descriptions-item label="举报用户">
                            {{ reportData.user.user_name }}
                        </el-descriptions-item>
                        <el-descriptions-item label="举报日期">
                            {{ reportData.date }}
                        </el-descriptions-item>
                        <el-descriptions-item label="举报内容">{{ reportData.content }} </el-descriptions-item>
                    </el-descriptions>
                </div>
            </el-card>
            <div class="report-judge">
                <div class="report-judge-header">举报审核</div>
                <div style="padding: 16px">
                    <el-input
                        v-model="judgment.text"
                        style="width: 100%; min-height: 50%"
                        :autosize="{ minRows: 10, maxRows: 20 }"
                        type="textarea"
                        placeholder="请输入反馈意见"
                        maxlength="200"
                        show-word-limit
                    />
                    <div style="margin-top: 20px">
                        <span>屏蔽评论</span>
                        <el-switch
                            v-model="judgment.unvisibility"
                            style="margin-left: 10px; --el-switch-on-color: #13ce66; --el-switch-off-color: #d0d0d0"
                        />
                    </div>

                    <div style="margin-top: 20px">
                        <el-button
                            v-if="reportData.processed"
                            class="button"
                            type="primary"
                            round
                            style="margin: 0 auto"
                            @click="handleSubmit"
                        >
                            确认修改
                        </el-button>
                        <el-button
                            v-else
                            class="button"
                            type="primary"
                            round
                            style="margin: 0 auto"
                            @click="handleSubmit"
                        >
                            确认提交
                        </el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { getReportDetail, judgeReport } from '@/api/report'
import { ElMessage } from 'element-plus'
export default {
    components: {},
    props: { reportID: Number },
    data() {
        return {
            reportData: {
                id: 10,
                comment: {
                    comment_id: '',
                    user: {
                        user_id: '',
                        user_name: ''
                    },
                    paper: {
                        paper_id: '',
                        title: ''
                    },
                    date: '',
                    content: '',
                    visibility: false
                },
                user: {
                    user_id: '',
                    user_name: ''
                },
                comment_level: 1,
                date: '',
                content: '',
                judgment: '',
                processed: false
            },
            judgment: {
                text: '',
                unvisibility: false
            }
        }
    },
    watch: {
        reportID: {
            handler() {
                this.draw()
            },
            immediate: true,
            deep: true
        }
    },
    computed: {},
    methods: {
        async draw() {
            await getReportDetail(this.$props.reportID)
                .then((response) => {
                    this.reportData = response.data
                    this.judgment.text = response.data.judgment
                    this.judgment.unvisibility = !response.data.comment.visibility
                })
                .catch((error) => {
                    ElMessage.error(error.response.data.message)
                })
        },
        async handleSubmit() {
            await judgeReport({
                report_id: this.$props.reportID,
                text: this.judgment.text,
                visibility: !this.judgment.unvisibility
            })
                .then((response) => {
                    ElMessage.success(response.data.message)
                })
                .catch((error) => {
                    ElMessage.error(error.response.data.message)
                })
        }
    }
}
</script>

<style lang="scss" scoped>
.report-card {
    display: flex;
    flex-direction: row;
    justify-content: center;
    .report-content {
        width: 60%;
        padding: 20px;
        border: 0px !important;
        border-right: 1px solid #dbdbdb !important;
        border-radius: 0px !important;
        background-color: #fff;
    }

    .report-judge {
        width: 40%;
        padding: 20px;
        .report-judge-header {
            margin-top: 20px;
            color: #303133;
            font-weight: bold;
        }
    }
}

:deep(.el-descriptions__label) {
    width: 20% !important;
}

.button {
    display: block;
    width: 30%;
}
</style>
