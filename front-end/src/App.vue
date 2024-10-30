<template>
<n-config-provider :locale="zhCN" :date-locale="dateZhCN" :theme-overrides="themeOverrides">
  <Header></Header>

  <router-view></router-view>
  
  <Footer v-show='$route.meta.showFooter'></Footer>
  
  </n-config-provider>
</template>

<script setup lang="ts">

import { onMounted } from 'vue';

import Header from '@/components/header/Header.vue'
import Footer from '@/components/footer/Footer.vue'

import { NConfigProvider, GlobalThemeOverrides, zhCN, dateZhCN } from 'naive-ui'


import useLoginStore from '@/store/login'
import useCategoryStore from '@/store/category'
import useSearchStore from '@/store/search'
import useCartStore from '@/store/cart'

const loginStore = useLoginStore()
const categoryStore = useCategoryStore()
const searchStore = useSearchStore()
const cartStore = useCartStore()

loginStore.load()
searchStore.updatePageData()
cartStore.loadList()

onMounted (async () => {
  //type store的初始数据载入
  await categoryStore.loadList()
})



  const themeOverrides: GlobalThemeOverrides = {
    common: {
      // primaryColor: '#FF0000',
      // primaryColorHover: '#00306e'
    },
    Button: {
      textColor: '#FF0000'
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

<style scoped>

</style>



