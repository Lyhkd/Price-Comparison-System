<template>
    <div class="search-results">
    <n-input
      v-model="searchParams.keyword"
      @keyup.enter="handleSearch"
      placeholder="搜索商品..."
    />
    <n-button @click="handleSearch">搜索</n-button>

    <n-card v-if="results.length" v-for="item in results" :key="item.id" class="result-card">
      <n-card-header>
        <h3>{{ item.title }}</h3>
      </n-card-header>
      <n-card-content>
        <img :src="item.defaultImg" alt="商品图" />
        <p>价格: {{ item.price }} 元</p>
        <p>商标: {{ item.tmName }}</p>
        <n-button @click="viewDetails(item.id)">查看详情</n-button>
      </n-card-content>
    </n-card>
    
    <n-empty v-else />

    <n-pagination
      v-model:page="currentPage"
      :page-count="pageInfo.totalPages"
      @update:page="updatePage"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, computed } from 'vue';
import useSearchStore from '@/store/search';
import { useRoute } from 'vue-router';

export default defineComponent({
    setup() {
        const store = useSearchStore();
        const route = useRoute();

        // 读取路由参数并初始化搜索参数
        const searchParams = computed(() => store.params);
        const results = computed(() => store.goodsList);
        const pageInfo = computed(() => store.pageInfo);

        // 读取路由参数中的查询关键词
        const query = route.params.query as string;

        const handleSearch = async () => {
            await store.updatePageData();
        };

        const updatePage = async (page: number) => {
            await store.updatePageNum(page);
        };

        // 获取搜索结果
        onMounted(async () => {
            await store.updatePageData();
        });

        const viewDetails = (id: number) => {
            // 跳转到详情页，可以根据需求实现
        };

        return {
            searchParams,
            results,
            pageInfo,
            handleSearch,
            updatePage,
            viewDetails,
        };
    },
});
</script>

<style scoped>
.search-results {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    padding: 20px;
}

.result-card {
    width: 300px;
}
</style>