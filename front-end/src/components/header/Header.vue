<template>
  <!-- 头部 -->
   <header class="header">
    <n-button>naive-ui</n-button>
    <n-split :default-size="0.8">
    <template #1>
      <n-menu
        v-model:value="activeKey"
        mode="horizontal"
        :options="menuOptions"
        responsive
      />
    </template>
  </n-split>
    <!-- <el-menu
    :default-active="activeIndex2"
    class="el-menu-demo"
    mode="horizontal"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
    @select="handleSelect"
    :ellipsis="false"
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
    <div class="search-area">
      <el-row>
        <el-col :span="21">
          <el-input 
          v-model="keyword" 
          placeholder="Search" 
          style="width: 300px;"></el-input>
        </el-col>
        <el-col :span="3">
        <el-button class="search-botton" :icon="Search" @click="goSearch"></el-button>
      </el-col>
      </el-row>
      
    </div>
    <div class="login-button">
      <el-button type="primary" color="#ffd04b" round @click="goToSignUp">Sign Up</el-button>
    <el-button link type="info" color="#545c64" @click="goToSignIn">Sign In</el-button>
    </div>
  </el-menu> -->
   </header>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';
import useLoginStore from '@/store/login'
import useSearchStore from '@/store/search'

import type { Component } from 'vue'
import { defineComponent, h, ref, watch} from 'vue'

import { NIcon } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import {
  BookOutline as BookIcon,
  PersonOutline as PersonIcon,
  WineOutline as WineIcon
} from '@vicons/ionicons5'

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions: MenuOption[] = [
  {
    label: () =>
      h(
        'a',
        {
          href: 'https://baike.baidu.com/item/%E4%B8%94%E5%90%AC%E9%A3%8E%E5%90%9F',
          target: '_blank',
          rel: 'noopenner noreferrer'
        },
        '且听风吟'
      ),
    key: 'hear-the-wind-sing',
    icon: renderIcon(BookIcon)
  },
  {
    label: '1973年的弹珠玩具',
    key: 'pinball-1973',
    icon: renderIcon(BookIcon),
    disabled: true,
    children: [
      {
        label: '鼠',
        key: 'rat'
      }
    ]
  },
  {
    label: '寻羊冒险记',
    key: 'a-wild-sheep-chase',
    icon: renderIcon(BookIcon),
    disabled: true
  },
  {
    label: '舞，舞，舞',
    key: 'dance-dance-dance',
    icon: renderIcon(BookIcon),
    children: [
      {
        type: 'group',
        label: '人物',
        key: 'people',
        children: [
          {
            label: '叙事者',
            key: 'narrator',
            icon: renderIcon(PersonIcon)
          },
          {
            label: '羊男',
            key: 'sheep-man',
            icon: renderIcon(PersonIcon)
          }
        ]
      },
      {
        label: '饮品',
        key: 'beverage',
        icon: renderIcon(WineIcon),
        children: [
          {
            label: '威士忌',
            key: 'whisky'
          }
        ]
      },
      {
        label: '食物',
        key: 'food',
        children: [
          {
            label: '三明治',
            key: 'sandwich'
          }
        ]
      },
      {
        label: '过去增多，未来减少',
        key: 'the-past-increases-the-future-recedes'
      }
    ]
  }
]

const activeKey = ref('hear-the-wind-sing')

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

const goToSignUp = () => {
  router.push({ name: 'login' });
};

const goToSignIn = () => {
  router.push({ name: 'login' });
};

</script>

<style lang="less" scoped>

.header{
  .login-button {
  float: left;
  white-space: nowrap;
  margin-left: auto;  
  margin-right: 20px;
  margin-top: 13px;
}
  .search-area{
    white-space: nowrap;
    float: left;
    margin-left: 20px;
    margin-right: 20px;;
    margin-top: 13px;
  }
  .search-button{
    float: left;
  }

}
</style>