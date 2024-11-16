<template>
  <n-card>
    <template #header>
      <h3>用户信息</h3>
    </template>
    <div class="user-info">
      <p><strong>用户名：</strong>{{ userInfo.username }}</p>
      <p><strong>邮箱：</strong>{{ userInfo.email }}</p>
      <p><strong>提醒设置：</strong>{{ userInfo.alertMethod }}</p>
    </div>
  </n-card>
</template>

<script setup>
import { ref } from 'vue';

const userInfo = ref({
  username: '张三',
  email: 'zhangsan@example.com',
  alertMethod: '邮件',
});
</script>

<style scoped>
.user-info {
  padding: 10px;
  font-size: 14px;
}
</style>
