<template>

  <body>
  <div class="container">
        <form>
            <button class="btn btn-ghost">
                <img src="./assets/images/google.png" alt="">
                 Log in with Google
            </button>

            <small>or</small>

            <div class="form-control">
                <label for="email">Email</label>
				<input type="text" v-model="phone" placeholder="手机号">
            </div>
			
            <div class="form-control">
                <label for="password">Password</label>
				<input type="password" id="password" v-model="password" placeholder="请输入密码">
            </div>
            <div class="checkbox-container">
				
                <input type="checkbox" id="remember" v-model="checked" style="margin-right: 2px;">

                <label for="remember">Remember me</label>

                <a href="#">Forgot Password</a>
            </div>

            <button class="btn" @click.prevent="clickLogin">Log In</button>

            <small>Don't have an account? <a href="#">Sign up</a></small>
        </form>

        <div class="features">
            <div class="feature">
                <i class="fas fa-code"></i>
                <h3>Development</h3>
                <p>A modern and clean design system for developing fast and powerful
                    web interfaces.</p>
            </div>
            <div class="feature">
                <i class="fas fa-gift"></i>
                <h3>Features</h3>
                <p>A modern and clean design system for developing fast and powerful
                    web interfaces.</p>
            </div>
            <div class="feature">
                <i class="fas fa-edit"></i>
                <h3>Updates</h3>
                <p>A modern and clean design system for developing fast and powerful
                    web interfaces.</p>
            </div>
        </div>
    </div>
</body>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router';

import useLoginStore from '@/store/login'

const phone = ref('')
const phoneMsg = ref('请输入正确的11位手机号码')

const checked = ref(false)

const password = ref('')
const passwordMsg = ref('请输入大于6位的密码')

const router = useRouter()
const loginStore = useLoginStore()

watch(phone, () => {
  if((/^1[3456789]\d{9}$/).test(phone.value)){
    return phoneMsg.value = ''
  } else {
    return phoneMsg.value = '请输入正确的11位手机号码'
  }
})

watch(password, () => {
  if(password.value.length < 6) {
    return passwordMsg.value = '请输入大于6位的任意密码'
  } else {
    return passwordMsg.value = ''
  }
})

const clickLogin = async () => {
  if(phoneMsg.value === '' && passwordMsg.value === '') {
    await loginStore.login(phone.value, password.value)
    router.push({ name: 'home' })
  }
}


</script>

<style lang="less" scoped>

@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');

* {
    box-sizing: border-box;
}

body {
	width: 100%;
	overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #f7f8fc;
    color: #141c2c;
    font-family: 'Open Sans', sans-serif;
    margin: 0;
}

a {
    color: #2762eb;
    text-decoration: none;
}

.container {
	margin-top: 60px;
    background-color: #fff;
    border-radius: 3px;
    border: 20px solid #dce7ff;
    width: 1000px;
    box-shadow: 0 4px 5px rgba(0,0,0,0.1);
    display: flex;
}

form {
    border-right: 1px solid #ecf2ff;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    flex: 1;
}

.form-control {
    margin: 10px 0;
    width: 100%;
}

label {
    display: inline-block;
    font-weight: bold;
    margin-bottom: 5px;
}

input:not([type="checkbox"]) {
    background-color: transparent;
    border: 2px solid #ecf2ff;
    border-radius: 3px;
    font-family: inherit;
    font-size: 14px;
    padding: 10px;
    width: 100%;
}

.checkbox-container {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    margin-bottom: 15px;
    width: 100%;
}

.checkbox-container a {
    margin-left: auto;
}

.checkbox-container label {
    color: #7a7e8c;
    font-weight: normal;
}

.btn {
    cursor: pointer;
    background-color: #141c2c;
    border: 2px solid #141c2c;
    border-radius: 3px;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: inherit;
    font-weight: bold;
    font-size: 14px;
    padding: 10px;
    margin: 20px 0;
    width: 100%;
}

.btn-ghost {
    background-color: transparent;
    border-color: #ecf2ff;
    color: #141c2c;
}

.btn img {
    margin-right: 5px;
    width: 20px;
}

.features {
    flex: 1.5;
    padding: 40px;
}

.feature {
    position: relative;
    padding-left: 30px;
    margin: 40px 0;
}

.feature i {
    color: #2762eb;
    position: absolute;
    top: 5px;
    left: 0;
}

.feature h3 {
    margin: 0;
}

.feature p {
    font-size: 14px;
    line-height: 1.8;
    margin: 5px 0;
}

@media(max-width: 768px) {
    .container {
        flex-direction: column;
    }

    form {
        border-right: 0;
    }
}
</style>