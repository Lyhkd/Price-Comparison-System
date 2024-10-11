<template>
  <!-- 头部 -->
   <el-menu
    :default-active="activeIndex2"
    class="el-menu-demo"
    mode="horizontal"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
    @select="handleSelect"
  >
    <el-menu-item index="1">Processing Center</el-menu-item>
    <el-sub-menu index="2">
      <template #title>Workspace</template>
      <el-menu-item index="2-1">item one</el-menu-item>
      <el-menu-item index="2-2">item two</el-menu-item>
      <el-menu-item index="2-3">item three</el-menu-item>
      <el-sub-menu index="2-4">
        <template #title>item four</template>
        <el-menu-item index="2-4-1">item one</el-menu-item>
        <el-menu-item index="2-4-2">item two</el-menu-item>
        <el-menu-item index="2-4-3">item three</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-menu-item index="3" disabled>Info</el-menu-item>
    <el-menu-item index="4">Orders</el-menu-item>
  </el-menu>
  <header class="header">
    <!--头部第一行 登录注册-->
    <div class="top">
      <div class="container">
        <div class="loginList">
          <p>尚品汇欢迎您！{{ userName }}</p>
          <p v-if="isLogin">
            <a href="#" @click.prevent="clickLogout">退出登录</a>
          </p>
          <p v-if="!isLogin">
            <span>请</span>
            
            <router-link class="register" to="/login">登录</router-link >
            <router-link class="register" to="/register">免费注册</router-link >
          </p>
        </div>
        <div class="typeList">
          <p v-if="!isLogin">
            <el-button-group>
            <el-button type="primary" color="#0a7029" round>Sign Up</el-button>
            <el-button color="#0a7029" plain round>Sign In</el-button>
          </el-button-group>
          </p>
          
          <router-link to="/my-order">我的订单</router-link>
          <router-link to="/cart">我的购物车</router-link>
        </div>
      </div>
    </div>
    <!--头部第二行 搜索区域-->
    <div class="bottom">
      <h1 class="logoArea">
        <router-link to="/home" class="logo" title="尚品汇">
          <img src="/images/logo.png" alt="" />
        </router-link>
      </h1>
      <div class="searchArea">
        <form action="###" class="searchForm">
          <input type="text" id="autocomplete" class="input-error input-xxlarge" v-model="keyword" />
          <button class="sui-btn btn-xlarge btn-danger" type="button" @click.prevent="goSearch">搜索</button>
        </form>
      </div>
    </div>
  </header>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router';

import useLoginStore from '@/store/login'
import useSearchStore from '@/store/search'

const activeIndex2 = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

const keyword = ref('')

const router = useRouter()

const searchStore = useSearchStore()
const loginStore = useLoginStore()
const userName = ref('')
const isLogin = ref(false)

watch(loginStore, () => {

  if(loginStore.loginInfo && Object.keys(loginStore.loginInfo).length > 0){
    isLogin.value = true
    userName.value = loginStore.loginInfo.name
  } else {
    isLogin.value = false
    userName.value = '游客'
  }

})

const goSearch = () => {
  searchStore.updateParam({ keyword: keyword.value })

  router.push({name: 'search'})
}

const clickLogout = () => {

  loginStore.logout()
}

</script>

<style lang="less" scoped>
.header {
  font-family: Arial, sans-serif; /* 设置字体系列 */
  font-size: 14px; /* 设置字体大小 */
  font-weight: normal; /* 设置字体粗细 */
  font-style: normal; /* 设置字体样式 */
  line-height: 1.5; /* 设置行高 */
  color: #333; /* 设置字体颜色 */
  & > .top {
    background-color: #ffffffff;
    height: 50px;
    line-height: 50px;
    border: none;
    border-bottom: 1.5px solid #e6e6e6d3;
    .container {
      width: 1200px;
      margin: 0 auto;
      overflow: hidden;

      .loginList {
        float: left;

        p {
          float: left;
          margin-left: 10px;

          .register {
            border-left: 1px solid #b3aeae;
            padding: 0 5px;
            margin-left: 5px;
          }
        }
      }
    }
    
    .typeList {
      float: right;

      a {
        padding: 0 10px;

        & + a {
          border-left: 1px solid #b3aeae;
        }
      }
    }
  }

  & > .bottom {
    width: 1200px;
    margin: 0 auto;
    overflow: hidden;
    
    .logoArea {
      float: left;

      img {
        width: 175px;
        margin: 25px 45px;
      }
    }

    .searchArea {
      float: right;
      margin-top: 35px;

      .searchForm {
        overflow: hidden;

        input {
          box-sizing: border-box;
          width: 490px;
          height: 32px;
          padding: 0px 4px;
          border: 2px solid #ea4a36;
          float: left;

          &:focus {
            outline: none;
          }
        }

        button {
          height: 32px;
          width: 68px;
          background-color: #ea4a36;
          border: none;
          color: #fff;
          float: left;
          cursor: pointer;

          &:focus {
            outline: none;
          }
        }

      }

    }

  }

}
</style>