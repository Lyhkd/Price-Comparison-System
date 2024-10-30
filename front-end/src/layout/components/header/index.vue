<template>
    <n-layout >
      <n-layout-header>颐和园路</n-layout-header>
      <n-layout has-sider>
        <n-layout-sider content-style="padding: 24px;">
            <img src="../../assets/logo.png" alt="logo" />
        </n-layout-sider>
        <n-layout-sider content-style="padding: 24px;">

            <div class="options">
                <n-menu 
                :options="menuOptions"
                mode="horizontal"/>
            </div>
        
        </n-layout-sider>
        <n-layout-sider content-style="top: 30px;">
            <n-button>naive-ui</n-button>
        </n-layout-sider>
        <n-layout-content content-style="padding: 24px;">
          平山道
        </n-layout-content>
      </n-layout>
      <n-layout-footer bordered></n-layout-footer>
    </n-layout>
  
</template>

<script lang="ts">
import type { Component } from 'vue'
import { defineComponent, h } from 'vue'
import { NIcon } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import { RouterLink } from 'vue-router'
import {
  LogOutOutline as HomeIcon,
  LaptopOutline as WorkIcon
} from '@vicons/ionicons5'

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions: MenuOption[] = [
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'home',
            params: {
              lang: 'zh-CN'
            }
          }
        },
        { default: () => '回家' }
      ),
    key: 'go-back-home',
    icon: renderIcon(HomeIcon)
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            path: '/zh-CN/os-theme/components/code'
          }
        },
        { default: () => '上班' }
      ),
    key: 'go-to-work',
    icon: renderIcon(WorkIcon)
  }
]

export default defineComponent({
  setup() {
    return {
      menuOptions
    }
  }
})
</script>

<style scoped>
.n-layout-sider {
  background: rgba(209, 209, 209, 0.3);
}

.n-layout-content {
  background: rgba(128, 128, 128, 0.4);
}

.options {
    align-items: center; 
}
</style>