<template>
  <n-config-provider :locale="zhCN" :date-locale="dateZhCN" :theme-overrides="themeOverrides">
    <n-message-provider>
      <n-dialog-provider>
        <n-notification-provider>

          <Header></Header>
          <router-view>
          </router-view>
          <Message></Message>
        </n-notification-provider>
      </n-dialog-provider>
    </n-message-provider>
    <Footer v-show='$route.meta.showFooter'></Footer>

  </n-config-provider>
</template>

<script setup lang="ts">

import { onMounted } from 'vue';

import Header from '@/layout/components/header/index.vue'
import Footer from '@/components/footer/Footer.vue'
import Message from '@/components/message/index.vue'
import { NConfigProvider, NDialogProvider, NNotificationProvider, NMessageProvider,GlobalThemeOverrides, zhCN, dateZhCN } from 'naive-ui'


import useLoginStore from '@/store/login'
import useCategoryStore from '@/store/category'
import useSearchStore from '@/store/search'
import useCartStore from '@/store/cart'

const loginStore = useLoginStore()
const categoryStore = useCategoryStore()
const searchStore = useSearchStore()
const cartStore = useCartStore()

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
        textColor: '#FF0000'
      }
    }
  }
}


</script>

<style scoped></style>
