<template>
    <div class="profile">
        <div class="upper-box">
            <div class="avatar-box">
                <el-avatar class="avatar" :src="userProfile.avatar" />
            </div>
            <div class="base-info">
                <div class="base-info-username">
                    {{ userProfile.username }}
                    <el-icon color="#409efc" style="width: 8%; height: 8%"><i-ep-InfoFilled /></el-icon>
                </div>
                <div class="base-info-userid">
                    <el-icon><i-ep-UserFilled /></el-icon>
                    <span style="margin-left: 2%">{{ userProfile.user_id }}</span>
                </div>
                <div class="base-info-date">
                    <el-icon><i-ep-Calendar /></el-icon>
                    <span style="margin-left: 2%">{{ userProfile.registration_date }}</span>
                </div>
            </div>
        </div>

        <div class="lower-box">
            <div class="statistic-card">
                <div class="statistic-title">收藏文献</div>
                <div class="statistic-content">{{ userProfile.collected_papers_cnt }}</div>
            </div>
            <div class="statistic-card">
                <div class="statistic-title">点赞文献</div>
                <div class="statistic-content">{{ userProfile.liked_papers_cnt }}</div>
            </div>
            <div class="statistic-card">
                <div class="statistic-title">上传文件</div>
                <div class="statistic-content">{{ userProfile.documents_cnt }}</div>
            </div>
        </div>
    </div>
</template>

<script>
import { getUserProfile } from '@/api/user'
import { ElMessage } from 'element-plus'
import { ref } from 'vue'
import { serverURL } from '@/utils/request'

export default {
    components: {},
    props: { username: String },
    data() {
        return {
            userProfile: ref({
                user_id: '',
                username: '',
                avatar: '',
                registration_date: '',
                collected_papers_cnt: 0,
                liked_papers_cnt: 0,
                documents_cnt: 0
            })
        }
    },
    watch: {
        username: {
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
            await getUserProfile(this.$props.username)
                .then((response) => {
                    this.userProfile = response.data
                    this.userProfile.avatar = serverURL + this.userProfile.avatar
                })
                .catch((error) => {
                    ElMessage.error(error.response.data.message)
                })
        }
    }
}
</script>
<style lang="scss" scoped>
.profile {
    width: 100%;
    height: 45vh;
}
.upper-box {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    height: 60%;
    .avatar-box {
        flex: 1.8;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        .avatar {
            height: 70%;
            width: 80%;
        }
    }
    .base-info {
        flex: 3;
        height: 100%;
        .base-info-username {
            height: 30%;
            padding-top: 20%;
            font-size: 35px;
            color: black;
            font-weight: bold;
        }
        .base-info-userid {
            display: flex;
            align-items: center;
        }
        .base-info-date {
            display: flex;
            align-items: center;
            height: 20%;
        }
    }
}
.lower-box {
    box-sizing: border-box;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    height: 30%;
    .statistic-card {
        // flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0 8%;
        height: 80%;
        border-right: 1.5px solid rgb(0, 0, 0, 0.2);
        .statistic-title {
            flex: 1;
            font-size: 20px;
            color: rgb(95, 95, 95);
        }
        .statistic-content {
            flex: 1;
            font-size: 19px;
        }
    }
    .statistic-card:last-of-type {
        border-right: none;
    }
}
</style>
