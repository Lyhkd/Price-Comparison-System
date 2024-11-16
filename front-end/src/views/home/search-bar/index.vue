<!-- SearchComponent.vue -->
<template>
    <div class="search-box" :style="{ minWidth: boxWidth }">
      <n-input
        round
        clearable
        :placeholder="placeholder"
        v-model:value="localSearchInput"
        @keydown.enter="handleSearch"
        :style="{ width: inputWidth }"
        size="large"
      />
      <div style="width: 5px;"></div>
      <n-button round type="primary" @click="handleSearch">
        <template #icon>
          <n-icon>
            <SearchIcon />
          </n-icon>
        </template>
      </n-button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed, watch, onMounted, onBeforeUnmount } from 'vue';
  import { NIcon } from 'naive-ui';
  import { Search as SearchIcon } from "@vicons/ionicons5";
  
  export default defineComponent({
    name: 'SearchBar',
    components: {
      NIcon,
      SearchIcon
    },
    props: {
      // 搜索框宽度，支持传入具体数值
      width: {
        type: [String, Number],
        default: '500'
      },
      // 搜索框占位符文本
      placeholder: {
        type: String,
        default: '搜索商品...'
      },
    },
    emits: ['search'],
    setup(props, { emit }) {
      const localSearchInput = ref('');
      const isSearchHidden = ref(false);
      const windowWidth = ref(window.innerWidth);
  
      // 计算搜索框宽度
      const inputWidth = computed(() => {
        return typeof props.width === 'number' ? `${props.width}px` : props.width;
      });

      const boxWidth = computed(() => {
        return typeof props.width === 'number' ? `${props.width+200}px` : props.width;
      });
  

      // 处理搜索事件
      const handleSearch = () => {
        if (localSearchInput.value.trim()) {
          emit('search', localSearchInput.value);
        }
      };
  
  
      return {
        localSearchInput,
        inputWidth,
        boxWidth,
        handleSearch
      };
    }
  });
  </script>
  
  <style scoped>
  .search-box {
    display: flex;
    align-items: center;
  }
  
  /* @media (max-width: 800px) {
    .search-box :deep(.n-input) {
      width: 150px !important;
    }
  } */
  </style>