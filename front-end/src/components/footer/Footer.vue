<template>
    <n-layout-footer class="footer">
      <n-space justify="center" align="center" class="footer-content">
        <!-- 网站信息 -->
        
  
        <!-- 社交媒体链接 -->
        <n-space vertical class="social-media">
          <div class="footer-title">关注我们</div>
          <n-space>
            <n-button size="large" tag="a" href="https://github.com/Lyhkd" target="_blank" circle >
                <template #icon>
                <n-icon><LogoGithub/></n-icon>
            </template>
            </n-button>
            <n-button tag="a" href="https://x.com/YuerZhou7" target="_blank" size="large" circle >
                <template #icon>
                <n-icon><LogoTwitter/></n-icon>
            </template>
            </n-button>
            <n-button tag="a" href="https://x.com/YuerZhou7" target="_blank" size="large" circle>
                <template #icon>
                <n-icon><QqOutlined/></n-icon>
            </template>
        </n-button>
            <n-button tag="a" href="https://x.com/YuerZhou7" target="_blank" size="large" circle>
                <template #icon>
                <n-icon><WechatOutlined/></n-icon>
            </template>
            </n-button>
          </n-space>
        </n-space>
      </n-space>
  
      <!-- 版权信息 -->
      <div class="footer-bottom">
        <span>&copy; 2025 My Price 云比价. All rights reserved.</span>
      </div>
    </n-layout-footer>
  </template>
  
  <script setup lang="ts">
  import { defineComponent } from 'vue';
  import { NLayoutFooter, NSpace, NButton } from 'naive-ui';
  import { LogoGithub, LogoTwitter, LogoInstagram } from '@vicons/ionicons5';
  import {QqOutlined,WechatOutlined,WeiboOutlined} from '@vicons/antd';
  // 跳转到页面的逻辑，可以根据需要修改
  const goTo = (page: string) => {
    console.log(`Redirecting to ${page}`);
    // 实际上这里会跳转到对应的页面，通常是路由跳转
  };
  </script>
  
  <style scoped lang="scss">
  .footer {
    background-color: #f5f5f5;
    padding: 20px 0;
    color: #333;
  }
  
  .footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .footer-info,
  .social-media {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .footer-title {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 10px;
    // color: #0073e6;
  }
  
  .footer-links n-button {
    margin: 5px;
    font-size: 14px;
  }
  
  .social-media n-button {
    margin: 0 10px;
  }
  
  .footer-bottom {
    text-align: center;
    margin-top: 20px;
    font-size: 12px;
    color: #999;
  }
  </style>
  