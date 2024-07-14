<template>
    <div class="background">
        <div class="form-card">
            <div class="logo1">
                <div class="logo2"></div>
            </div>
            <!-- 登录 -->
            <div :class="{ login: true }">
                <el-form ref="loginForm" label-width="auto" :model="dataForm" :rules="rules" class="custom-form">
                    <el-form-item class="form-col">
                        <h1 class="title">管理员登录</h1>
                    </el-form-item>
                    <el-col :span="18" :offset="3" class="form-col">
                        <el-form-item prop="managerName">
                            <el-input class="form-input" placeholder="请输入管理员名" v-model="dataForm.managerName">
                                <template #prefix>
                                    <el-icon><i-ep-user /></el-icon>
                                </template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="18" :offset="3" class="form-col">
                        <el-form-item prop="managerPassword">
                            <el-input
                                name="password"
                                class="form-input"
                                type="password"
                                placeholder="请输入密码"
                                v-model="dataForm.managerPassword"
                                show-password
                                @keyup.enter="handleEnter"
                            >
                                <template #prefix>
                                    <el-icon><i-ep-lock /></el-icon>
                                </template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="18" :offset="3" class="form-col">
                        <el-button type="primary" round class="form-button" @click="handleLogin">登录</el-button>
                    </el-col>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
import { managerLogin } from '@/api/manager.js'
import { ElMessage } from 'element-plus'
export default {
    data() {
        return {
            dataForm: {
                managerName: '',
                managerPassword: ''
            },

            rules: {
                managerName: [
                    { required: true, message: '请输入管理员名', trigger: 'blur' },
                    { min: 3, max: 10, message: '管理员名必须是3-10位的字符', trigger: 'blur' }
                ],
                managerPassword: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    {
                        pattern: /^\S{3,15}$/,
                        message: '密码必须是3-15位的非空字符',
                        trigger: 'blur'
                    }
                ]
            }
        }
    },
    methods: {
        async handleEnter() {
            await this.$refs.loginForm.validate()
            await this.handleLogin()
        },
        async handleLogin() {
            await this.$refs.loginForm.validate()
            await managerLogin(this.dataForm)
                .then((response) => {
                    ElMessage({ message: response.data.message, type: 'success' })
                    this.$store.commit('setManagerInfo', this.dataForm)
                    this.$router.push('/home')
                })
                .catch((error) => {
                    ElMessage.error(error.response.data.error)
                })
        }
    }
}
</script>

<style scoped lang="scss">
.background {
    display: flex;
    justify-content: center;
    align-items: center;
    background: no-repeat center/100% url('@/assets/login-backgroud.jpg');
    width: 100vw;
    height: 100vh;

    .form-card {
        position: relative;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 60vw;
        height: 60vh;
        background-color: rgb(255, 255, 255, 0.9);
        border-radius: 3vh;
        box-shadow: 6px 7px 15px 1px rgba(0, 0, 0, 0.3);
        overflow: hidden;
        .logo1 {
            flex: 1;
            height: 100%;
            background-color: white;
            .logo2 {
                width: 100%;
                height: 100%;
                background: url('@/assets/login-logo.png') no-repeat center/120%;
            }
        }
        .login {
            flex: 1;
            height: 100%;
            // transition: transform 0.5s ease;
        }
    }
}

.custom-form {
    display: flex;
    flex-direction: column;
    margin: 0 auto;
    width: 80%;
    height: 100%;

    .form-col {
        flex: 1;
        vertical-align: middle;
        height: 100%;
        .title {
            margin: 10% auto;
            color: rgb(0, 157, 255);
            font-size: 3.5vh;
        }
        .form-input {
            border: none;
            border-bottom: 1.4px solid;
            size: 18px;
        }
        :deep(.el-input__wrapper) {
            font-size: 1.8vh;
            margin-top: 1vh;
            box-shadow: 0 0 0 0px var(--el-input-border-color, var(--el-border-color)) inset;
            border: none;
            background: rgb(0, 0, 0, 0);
        }
        .form-button {
            width: 80%;
            height: 40%;
            margin: 6% 10%;
            font-size: 1.8vh;
        }
    }
}
</style>
