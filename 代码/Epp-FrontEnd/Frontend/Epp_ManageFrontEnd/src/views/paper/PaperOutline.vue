<template>
    <div class="container">
        <div class="title">
            {{ paperInfo.title }}
            <el-link :href="paperInfo.original_url" :underline="false" style="font-size: 18px">
                <el-icon><i-ep-Link /></el-icon>
            </el-link>
        </div>

        <div class="date">
            <svg
                t="1716217383139"
                class="icon"
                viewBox="0 0 1024 1024"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                p-id="2733"
                width="14"
                height="14"
            >
                <path
                    d="M512 85.333333c235.648 0 426.666667 191.018667 426.666667 426.666667s-191.018667 426.666667-426.666667 426.666667S85.333333 747.648 85.333333 512 276.352 85.333333 512 85.333333z m0 85.333334C323.477333 170.666667 170.666667 323.477333 170.666667 512s152.810667 341.333333 341.333333 341.333333 341.333333-152.810667 341.333333-341.333333S700.522667 170.666667 512 170.666667z m0 106.666666a21.333333 21.333333 0 0 1 21.333333 21.333334v234.666666h170.666667a21.333333 21.333333 0 0 1 21.333333 21.333334v42.666666a21.333333 21.333333 0 0 1-21.333333 21.333334H469.333333a21.333333 21.333333 0 0 1-21.333333-21.333334V298.666667a21.333333 21.333333 0 0 1 21.333333-21.333334h42.666667z"
                    fill="#606266"
                    p-id="2734"
                ></path>
            </svg>
            <span>发表日期：{{ paperInfo.publication_date }}</span>
        </div>
        <div class="author">
            <el-icon><i-ep-Avatar /></el-icon>
            <span>{{ paperInfo.authors.join(', ') }}</span>
        </div>
        <div class="subclass">
            <el-tag
                v-for="subclass in paperInfo.subclasses"
                :key="subclass"
                type="success"
                effect="light"
                size="large"
                round
            >
                {{ subclass }}
            </el-tag>
        </div>
        <div class="abstract">摘要：{{ paperInfo.abstract }}</div>
        <div class="additional-info">
            <div class="info-item">
                <el-icon><i-ep-Document /></el-icon>
                <span>引用次数：{{ paperInfo.citation_count }}</span>
            </div>
            <div class="info-item">
                <el-icon><i-ep-View /></el-icon>
                <span>阅读次数：{{ paperInfo.read_count }}</span>
            </div>
            <div class="info-item">
                <el-icon><i-ep-Download /></el-icon>
                <span>下载次数：{{ paperInfo.download_count }}</span>
            </div>
            <div class="info-item">
                <el-icon><i-ep-Star /></el-icon>
                <span>收藏次数：{{ paperInfo.collect_count }}</span>
            </div>
            <div class="info-item">
                <el-icon><i-ep-ChatDotRound /></el-icon>
                <span>评论次数：{{ paperInfo.comment_count }}</span>
            </div>
        </div>
    </div>
</template>

<script>
import { getPaperOutline } from '@/api/paper'
import { ElMessage } from 'element-plus'
export default {
    components: {},
    props: { paperID: String },
    data() {
        return {
            paperInfo: {
                paper_id: '',
                title: '',
                authors: [],
                abstract: '',
                publication_date: '',
                journal: null,
                citation_count: 0,
                read_count: 0,
                like_count: 0,
                collect_count: 0,
                download_count: 0,
                comment_count: 0,
                score: 0.0,
                score_count: 0,
                original_url: '',
                subclasses: []
            }
        }
    },
    watch: {
        paperID: {
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
            await getPaperOutline(this.$props.paperID)
                .then((response) => {
                    this.paperInfo = response.data
                })
                .catch((error) => {
                    ElMessage.error(error.response.data.message)
                })
        }
    }
}
</script>

<style lang="scss" scoped>
.container {
    max-height: 70vh;
    overflow: auto;
}
.title {
    width: 80%;
    margin: 0 auto;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    color: black;
}
.author {
    width: 75%;
    margin: 1vh auto;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;

    & > *:not(:last-child) {
        margin-right: 0.5vw;
    }
}

.subclass {
    width: 80%;
    margin: 0.5vh auto;
    text-align: center;
    & > *:not(:last-child) {
        margin-right: 0.5vw;
    }
}
.date {
    margin-top: 1vh;
    display: flex;
    align-items: center;
    justify-content: center;
    & > *:not(:last-child) {
        margin-right: 0.5vw;
    }
}
.abstract {
    width: 95%;
    margin: 1vh auto;
    margin-top: 1vh;
    overflow: auto;
}

.additional-info {
    width: 80%;
    margin: 0 auto;
    margin-top: 2vh;
    display: flex;
    justify-content: space-around;
    // flex-wrap: wrap;
    // text-align: center;
    .info-item {
        display: flex;
        align-items: center;
        .el-icon {
            margin-right: 5px;
        }
    }
}
</style>
