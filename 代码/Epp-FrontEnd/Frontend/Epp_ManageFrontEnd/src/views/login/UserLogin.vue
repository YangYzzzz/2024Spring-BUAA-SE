<template>
    <div class="background">
        <div class="form-card">
            <div class="logo1">
                <div class="logo2"></div>
            </div>
            <!-- 注册 -->
            <div :class="{ register: true, 'register-change': !isLogin }">
                <el-form ref="registerForm" label-width="auto" :model="dataForm" :rules="rules" class="custom-form">
                    <el-form-item class="form-col">
                        <h1 class="title">注册</h1>
                    </el-form-item>
                    <el-col :span="18" :offset="3" class="form-col">
                        <el-form-item prop="username">
                            <el-input class="form-input" placeholder="请输入用户名" v-model="dataForm.username">
                                <template #prefix>
                                    <el-icon><i-ep-user /></el-icon>
                                </template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="18" :offset="3" class="form-col">
                        <el-form-item prop="password">
                            <el-input
                                name="password"
                                class="form-input"
                                type="password"
                                placeholder="请输入密码"
                                v-model="dataForm.password"
                                show-password
                            >
                                <template #prefix>
                                    <el-icon><i-ep-lock /></el-icon>
                                </template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="18" :offset="3" class="form-col">
                        <el-form-item prop="repassword">
                            <el-input
                                name="repassword"
                                class="form-input"
                                type="password"
                                placeholder="请再次输入密码"
                                v-model="dataForm.repassword"
                                show-password
                            >
                                <template #prefix>
                                    <el-icon><i-ep-lock /></el-icon>
                                </template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="18" :offset="3" class="form-col">
                        <el-button type="primary" round class="form-button" @click="handleRegister">注册</el-button>
                    </el-col>
                    <el-col :span="18" :offset="3" class="form-col">
                        <div class="skip" @click="handleToLogin">
                            已有账号？去登录 <el-icon style="vertical-align: middle"><i-ep-right /></el-icon>
                        </div>
                    </el-col>
                </el-form>
            </div>
            <!-- 登录 -->
            <div :class="{ login: true, 'login-change': !isLogin }">
                <el-form ref="loginForm" label-width="auto" :model="dataForm" :rules="rules" class="custom-form">
                    <el-form-item class="form-col">
                        <h1 class="title">登录</h1>
                    </el-form-item>
                    <el-col :span="18" :offset="3" class="form-col">
                        <el-form-item prop="username">
                            <el-input class="form-input" placeholder="请输入用户名" v-model="dataForm.username">
                                <template #prefix>
                                    <el-icon><i-ep-user /></el-icon>
                                </template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="18" :offset="3" class="form-col">
                        <el-form-item prop="password">
                            <el-input
                                name="password"
                                class="form-input"
                                type="password"
                                placeholder="请输入密码"
                                v-model="dataForm.password"
                                show-password
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
                    <el-col :span="18" :offset="3" class="form-col">
                        <div class="skip" @click="handleToRegister">
                            没有账号？注册一个 <el-icon style="vertical-align: middle"><i-ep-right /></el-icon>
                        </div>
                    </el-col>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
import { userLogin } from '@/api/user.js'
import { ElMessage } from 'element-plus'
export default {
    data() {
        return {
            isLogin: true,
            dataForm: {
                username: '',
                password: '',
                repassword: ''
            },

            rules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' },
                    { min: 3, max: 10, message: '用户名必须是3-10位的字符', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    {
                        pattern: /^\S{3,15}$/,
                        message: '密码必须是3-15位的非空字符',
                        trigger: 'blur'
                    }
                ],
                repassword: [
                    { required: true, message: '请再次输入密码', trigger: 'blur' },
                    {
                        pattern: /^\S{3,15}$/,
                        message: '密码必须是3-15的非空字符',
                        trigger: 'blur'
                    },
                    {
                        validator: (rule, value, callback) => {
                            if (value !== this.dataForm.password) {
                                callback(new Error('请输入相同密码！'))
                            } else {
                                callback()
                            }
                        },
                        trigger: 'blur'
                    }
                ]
            }
        }
    },
    methods: {
        async handleLogin() {
            await this.$refs.loginForm.validate()
            userLogin(this.dataForm)
                .then((response) => {
                    console.log(response.data.message)
                    ElMessage({ message: response.data.message, type: 'success' })
                })
                .catch((error) => {
                    ElMessage.error(error.response.data.error)
                })
        },
        async handleRegister() {
            await this.$refs.registerForm.validate()
        },
        handleToLogin() {
            this.isLogin = true
        },
        handleToRegister() {
            this.isLogin = false
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
            position: absolute;
            width: 50%;
            height: 100%;
            background-color: white;
            z-index: 1;
            .logo2 {
                width: 100%;
                height: 100%;
                background: url('@/assets/logo.png') no-repeat center/75%;
            }
        }
        .register {
            flex: 1;
            height: 100%;
            opacity: 0;
            transition: transform 0.5s ease;
        }
        .login {
            flex: 1;
            height: 100%;
            transition: transform 0.5s ease;
            opacity: 1;
        }
        .register-change {
            transform: translateX(100%);
            opacity: 1;
        }
        .login-change {
            transform: translateX(-100%);
            opacity: 0;
        }
    }
}
.right-move {
    transform: translateX(100%);
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
        .skip {
            margin: 0 auto;
            width: 20vh;
            color: rgb(0, 0, 0, 0.4);
            font-size: 1.8vh;
        }
        .skip:hover {
            cursor: pointer;
            color: rgb(0, 0, 0, 0.8);
        }
    }
}
</style>
