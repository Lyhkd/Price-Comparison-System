<template>
    <div class="layout-outerbox">
        <div class="layout-card">
            <n-card bordered>
                <n-tabs v-model:value="mode" size="large" justify-content="space-evenly">
                    <n-tab-pane name="login" tab="登录">
                        <n-form :model="loginForm" :rules="loginRules" ref="loginFormRef">
                            <n-form-item label="用户名" path="username">
                                <n-input v-model:value="loginForm.username" placeholder="请输入用户名" />
                            </n-form-item>
                            <n-form-item label="密码" path="password">
                                <n-input v-model:value="loginForm.password" type="password" placeholder="请输入密码" />
                            </n-form-item>
                            <n-button type="primary" @click="handleLogin" block secondary strong>登录</n-button>
                        </n-form>
                    </n-tab-pane>
                    <n-tab-pane name="signup" tab="注册">
                        <n-form :model="registerForm" :rules="registerRules" ref="registerFormRef">
                            <n-form-item label="用户名" path="username">
                                <n-input v-model:value="registerForm.username" placeholder="请输入用户名" />
                            </n-form-item>
                            <n-form-item label="邮箱" path="email">
                                <n-input v-model:value="registerForm.email" placeholder="请输入邮箱" />
                            </n-form-item>
                            <n-form-item label="密码" path="password">
                                <n-input v-model:value="registerForm.password" type="password" placeholder="请输入密码" />
                            </n-form-item>
                            <n-form-item label="确认密码" path="confirmPassword">
                                <n-input v-model:value="registerForm.confirmPassword" type="password"
                                    placeholder="请再次输入密码" />
                            </n-form-item>
                            <n-button type="primary" @click="handleRegister" block secondary strong>注册</n-button>
                        </n-form>
                    </n-tab-pane>
                </n-tabs>
            </n-card>
        </div>
    </div>

</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { FormInst, FormRules } from 'naive-ui'
import { useRouter, useRoute } from 'vue-router'
import useLoginStore from '@/store/login'

export default defineComponent({
    setup() {

        const router = useRouter()
        const route = useRoute()
        const loginStore = useLoginStore()
        onMounted(() => {
            mode.value = route.query.mode as string
        })

        const mode = ref('login')

        // 登录表单数据和验证规则
        const loginForm = ref({
            username: '',
            password: ''
        })
        const loginFormRef = ref<FormInst | null>(null)
        const loginRules: FormRules = {
            username: [
                { required: true, message: '请输入用户名', trigger: 'blur' }
            ],
            password: [
                { required: true, message: '请输入密码', trigger: 'blur' },
                { min: 6, message: '密码长度至少为6字符', trigger: 'blur' }
            ]
        }

        // 注册表单数据和验证规则
        const registerForm = ref({
            username: '',
            email: '',
            password: '',
            confirmPassword: ''
        })
        const registerFormRef = ref<FormInst | null>(null)
        const registerRules: FormRules = {
            username: [
                { required: true, message: '请输入用户名', trigger: 'blur' },
                { min: 6, message: '用户名长度至少为6字符', trigger: 'blur' }
            ],
            email: [
                { required: true, message: '请输入邮箱', trigger: 'blur' },
                { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
            ],
            password: [
                { required: true, message: '请输入密码', trigger: 'blur' },
                { min: 6, message: '密码长度至少为6字符', trigger: 'blur' }
            ],
            confirmPassword: [
                { required: true, message: '请确认密码', trigger: 'blur' },
                { validator: (rule, value) => value === registerForm.value.password, message: '两次密码不一致', trigger: 'blur' }
            ]
        }

        // 处理登录逻辑

        const handleLogin = async () => {
            await loginFormRef.value?.validate((errors) => {
                if (errors) {
                    console.log('校验失败:', errors);
                    return 
                }
            })
            try {
                const success = await loginStore.login(loginForm.value.username, loginForm.value.password)
                router.push({ name: 'home' })
            } catch (error) {
                // 处理登录过程中发生的错误
                console.error('登录过程中发生错误:', error);
            }

        }


        // 处理注册逻辑
        const handleRegister = async () => {
            await registerFormRef.value?.validate((errors) => {
                if (errors) {
                    console.log('校验失败:', errors);
                    return 
                }
            })
            try {
                await loginStore.register(registerForm.value.username, registerForm.value.email, registerForm.value.password)
                await loginStore.login(registerForm.value.username, registerForm.value.password)
                router.push({ name: 'home' })
            } catch (error) {
                // 处理注册过程中发生的错误
                console.error('注册过程中发生错误:', error)
            }
        }

        return {
            loginForm,
            loginFormRef,
            loginRules,
            registerForm,
            registerFormRef,
            registerRules,
            handleLogin,
            handleRegister,
            mode,
        }
    }
})
</script>

<style scoped>
.layout-outerbox {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 100px;

}

.layout-card {
    display: flex;
    justify-content: center;
    align-items: center;
    min-width: 500px;
    /* 设置最小宽度 */
    min-height: 40px;

    /* 设置最小高度 */
    .n-card {
        width: 450px;
        height: 500px;
        box-shadow: 0 1px 4px rgba(0, 12, 24, 0.2);
    }
}

.n-layout-header {
    margin-bottom: 20px;
}
</style>