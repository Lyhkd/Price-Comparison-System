<template>
    <div class="home-page">
        <!-- 搜索框 -->
        <div class="logo-box">
            <img class="logo-image" src="@/assets/images/home.png" alt="logo"/>
        </div>
        <div class="search-box">
            <SearchBar :width="searchBarWidth" placeholder="搜索商品..." @search="handleSearch" />
        </div>
        <div class="empty-box" >
        </div>
    </div>
</template>

<script setup>
import useLoginStore from '@/store/login';
import SearchBar from './search-bar/index.vue';
import { defineComponent, h, ref, watch } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
const loginStore = useLoginStore();
// 处理搜索
const handleSearch = (searchText) => {
    router.push({
        name: 'search',
        query: {
            keyword: searchText,
            order: "default",
            pageNo: 1,
            pageSize: 30,
            platform: "all",
        },
    });
};

const searchBarWidth = ref(window.innerWidth <= 768 ? 300 : 500);

const updateSearchBarWidth = () => {
  searchBarWidth.value = window.innerWidth <= 768 ? 300 : 500;
};

onMounted(() => {
  window.addEventListener('resize', updateSearchBarWidth);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateSearchBarWidth);
});

</script>

<style scoped>
.home-page {
    display: flex;
  flex-direction: column; /* 垂直排列子元素 */
  padding-top: 100px;
  align-items: center;
  justify-content: flex-start; /* 从顶部开始排列子元素 */
  flex-grow: 1; /* 使 home-page 填充剩余空间 */

    .logo-box {
        display: flex;
        justify-content: center;
        margin-bottom: 50px;
        .logo-image {
            border-radius: 5%;
            object-fit: cover;
            box-shadow: 0 2px 2px rgba(0, 0, 0, 0.2);
            height: 200px; /* 设置合适的高度 */
        }
    }

    .search-box {
        padding-left: 20px;
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
}

.product-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    margin-top: 50px;
    margin-bottom: 100px;
}

.empty-box {
    flex-grow: 1;  
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;  /* 垂直排列子元素 */
}

@media (max-width: 768px) {

  .logo-box {
    margin-bottom: 50px;
    .logo-image {
      height: 200px; /* 调整高度以适配移动端 */
    }
  }

  .search-box {
    padding-left: 10px;
    margin-bottom: 20px;
  }

}
</style>