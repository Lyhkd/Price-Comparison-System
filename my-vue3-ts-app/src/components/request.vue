<template>
  <div>
    <button @click="sendRequest">点击发送请求</button>
    <p v-if="responseData">响应数据: {{ responseData }}</p>
    <p v-if="errorMessage" style="color: red;">错误信息: {{ errorMessage }}</p>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import axios from 'axios';

export default {
  name: 'GetRequestButton',
  setup() {
    const responseData = ref<string | null>(null);
    const errorMessage = ref<string | null>(null);

    // 发送 GET 请求的函数
    const sendRequest = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/search');
        responseData.value = JSON.stringify(response.data, null, 2); // 格式化显示返回的数据
        errorMessage.value = null; // 清除错误信息
      } catch (error) {
        if (axios.isAxiosError(error)) {
          errorMessage.value = `请求失败: ${error.message}`;
        } else {
          errorMessage.value = '未知错误';
        }
        responseData.value = null; // 清除响应数据
      }
    };

    return {
      sendRequest,
      responseData,
      errorMessage
    };
  }
};
</script>

<style scoped>
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

p {
  margin-top: 10px;
}
</style>
