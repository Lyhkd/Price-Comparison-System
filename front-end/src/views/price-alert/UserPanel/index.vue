<template>
  <n-card>
    <template #header>
      <h3>用户信息</h3>
    </template>
    <div class="user-info">
      <p><strong>用户名：</strong>{{ loginStore.userDisplayName }}</p>
      <p><strong>邮箱：</strong>{{ loginStore.userEmail }}</p>
      <p :v-if="loginStore.userPhone"><strong>手机：</strong>{{ loginStore.userPhone }}</p>
    </div>
  </n-card>
</template>

<script setup>
import { ref } from 'vue';
import useLoginStore from '@/store/login';
const loginStore = useLoginStore();
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
