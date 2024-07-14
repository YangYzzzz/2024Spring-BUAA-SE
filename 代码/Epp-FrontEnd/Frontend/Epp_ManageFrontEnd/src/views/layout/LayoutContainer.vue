<template>
    <el-container class="layout-container">
        <!-- 侧边栏 -->
        <el-aside style="width: 10vw; min-width: 160px">
            <el-menu
                active-text-color="#ffd04b"
                background-color="#2c2c2c"
                :default-active="activeMenu"
                text-color="#fff"
                router
            >
                <el-menu-item index="/home">
                    <el-icon>
                        <el-icon><i-ep-HomeFilled /></el-icon>
                    </el-icon>
                    <span>首页</span>
                </el-menu-item>
                <el-menu-item index="/user">
                    <el-icon>
                        <i-ep-userFilled />
                    </el-icon>
                    <span>用户管理</span>
                </el-menu-item>
                <el-menu-item index="/paper">
                    <el-icon><i-ep-document /></el-icon>
                    <span>论文管理</span>
                </el-menu-item>
                <el-menu-item index="/report">
                    <el-icon>
                        <i-ep-promotion />
                    </el-icon>
                    <span>用户审核</span>
                </el-menu-item>
            </el-menu>
        </el-aside>

        <!-- 主页 -->
        <el-container>
            <el-header>
                <span class="header-logo"></span>
                <span class="header-title">Easy Paper Plus 管理系统</span>
                <span class="header-setting">
                    <el-dropdown>
                        <div class="el-dropdown-link">
                            <el-icon>
                                <i-ep-setting />
                            </el-icon>
                        </div>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item @click="handleLogout">
                                    <el-icon><i-ep-fold /></el-icon>退出登录
                                </el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </span>
            </el-header>
            <el-main>
                <router-view></router-view>
            </el-main>
            <el-footer>BUAASE EPP 团队开发</el-footer>
        </el-container>
    </el-container>
</template>

<script>
import { managerLogout } from '@/api/manager.js'
import { ElMessage } from 'element-plus'
export default {
    methods: {
        async handleLogout() {
            await managerLogout()
                .then((response) => {
                    ElMessage({ message: response.data.message, type: 'success' })
                    this.$store.commit('resetManagerInfo', this.dataForm)
                    this.$router.push('/login')
                })
                .catch((error) => {
                    ElMessage.error(error.response.data.error)
                })
        }
    },
    computed: {
        activeMenu() {
            if (this.$route.path.startsWith('/report')) {
                return '/report'
            }
            return this.$route.path
        }
    }
}
</script>

<style lang="scss" scoped>
.layout-container {
    height: 100vh;

    .el-aside {
        background-color: #2c2c2c;

        .el-menu {
            margin-top: 5vh;
            border-right: none;
        }
    }
    .el-header {
        height: 8vh;
        width: 100%;
        color: #0674ea;
        background-color: white;
        font-weight: bold;
        font-size: 25px;
        margin: 0 auto;
        line-height: 10vh;

        .header-logo {
            float: left;
            height: 8vh;
            width: 10vh;
            background: url('@/assets/logo.png') no-repeat center / 70% auto;
        }
        .header-title {
            float: left;
            height: 8vh;
            width: 50vw;
            line-height: 8vh;
        }
        .header-setting {
            float: right;
            height: 8vh;
            width: 3vw;
            .el-dropdown-link {
                font-size: 3vh;
                height: 8vh;
                line-height: 8vh;
                cursor: pointer;
                align-items: center;
            }
        }
    }

    .el-footer {
        height: 5vh;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        color: #666;
    }
}
</style>
