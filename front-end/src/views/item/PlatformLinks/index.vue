<template>
    <div class="platform-links">
      <n-button-group>
        <n-button 
          v-for="(link, index) in links" 
          :key="index" 
          :href="link.url" 
          target="_blank">
          {{ link.name }}
        </n-button>
      </n-button-group>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PlatformLinks',
    props: {
      links: {
        type: Array,
        required: true
      }
    }
  };
  </script>
  
  <style scoped>
  .platform-links {
    margin-top: 20px;
  }
  </style>
  