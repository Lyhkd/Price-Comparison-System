<template>
    <div class="home-page">
        <!-- 搜索框 -->
        <div class="logo-box">
            <img class="logo-image" src="@/assets/images/home.png" alt="logo"/>
        </div>
        <div class="search-box">
            <SearchBar :width="500" placeholder="搜索商品..." @search="handleSearch" />
        </div>
        <!-- 商品卡片列表 -->
        <div class="product-list" v-if="loginStore.isLogin">
            <ProductCard v-for="item in products" :key="item.id" :product="item" />
        </div>
        <!-- 今日特价 -->
        <div class="empty-box" v-else>
        </div>
    </div>
</template>

<script setup>
import useLoginStore from '@/store/login';
import SearchBar from './search-bar/index.vue';
import ProductCard from './product-card/index.vue';
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

// 假数据示例
const products = ref([
    { id: 1, name: '商品1', currentPrice: 99.99, priceHistory: [120, 110, 105, 99.99] },
    { id: 2, name: '商品2', currentPrice: 199.99, priceHistory: [220, 210, 199.99] },
    { id: 3, name: '商品3', currentPrice: 299.99, priceHistory: [350, 330, 310, 299.99] },
]);
</script>

<style scoped>
.home-page {
    padding-top: 100px;

    align-items: center;
    justify-content: center;

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
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
}
</style>