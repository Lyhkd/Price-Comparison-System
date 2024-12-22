<template>
  <div class="wrapper">

  
  <n-config-provider :locale="zhCN" :date-locale="dateZhCN" :theme-overrides="themeOverrides">
    <n-message-provider>
      <n-dialog-provider>
        <n-notification-provider>

          <Header></Header>
          <router-view class="content">
          </router-view>
          <Message></Message>
        </n-notification-provider>
      </n-dialog-provider>
    </n-message-provider>
    <Footer v-show='$route.meta.showFooter'></Footer>

  </n-config-provider>
</div>
</template>

<script setup lang="ts">

import { onMounted } from 'vue';

import Header from '@/components/header/index.vue'
import Footer from '@/components/footer/Footer.vue'
import Message from '@/components/message/index.vue'
import { NConfigProvider, NDialogProvider, NNotificationProvider, NMessageProvider,GlobalThemeOverrides, zhCN, dateZhCN } from 'naive-ui'


import useLoginStore from '@/store/login'
import useSearchStore from '@/store/search'

const loginStore = useLoginStore()
const searchStore = useSearchStore()

// loginStore.load()
//searchStore.updatePageData()
//cartStore.loadList()

onMounted(async () => {
  //type store的初始数据载入
  //await categoryStore.loadList()
})



const themeOverrides: GlobalThemeOverrides = {
  common: {
    // primaryColor: '#FF0000',
    // primaryColorHover: '#00306e'
  },
  Button: {
    // textColor: '#FF0000'
  },
  Select: {
    peers: {
      InternalSelection: {
        // textColor: '#FF0000'
      }
    }
  }
}


</script>

<style scoped>

/* 整个页面的容器 */
.wrapper {
  display: flex;
  flex-direction: column; /* 垂直排列子元素 */
  min-height: 100vh;      /* 页面最小高度占满窗口 */
}

/* 主体内容区域 */
.content {
  min-height: calc(100vh - 320px);
}
</style>
