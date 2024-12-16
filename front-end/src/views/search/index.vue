<template>
  <div class="container">
    <n-spin :show="loading">
       <!-- 筛选选项 -->
       <div class="filters">
        <n-select v-model:value="selectedPlatform" :options="platformOptions" placeholder="选择平台" style="width: 200px;" />
        <n-select v-model:value="selectedOrder" :options="orderOptions" placeholder="价格排序" style="width: 200px;" />
      </div>
      <!-- 商品卡片容器 -->
      <div class="product-list">
        <div class="product-row" v-for="item in searchResults" :key="item.id">
          <n-card class="product-card" @click="goToProductPage(item.id)">
              <template #cover>
                <div class="image-box">
                  <img v-if="!loading" :src="item.defaultImg" alt="商品图片" class="product-img" />
                  <n-skeleton v-else height="40px" width="33%" />
                  
                </div>
              </template>
            <n-skeleton v-if="loading" text width="60%" />
            <template v-else>
              <div class="product-title">
                <span>{{ item.title }}</span>
              </div>

              <div class="product-footer">
                <p class="price">¥{{ item.currentPrice==0?"暂无价格":item.currentPrice  }}</p>
                <a :href="item.shopLink" target="_blank" class="shop-name">{{ item.shopName }}</a>
                <p class="platform">平台: {{ item.platform }}</p>

              </div>
            </template>

            <template>
              <div class="product-info">
                <n-button :href="item.link" target="_blank" size="small" class="view-product-btn">查看商品</n-button>
              </div>
            </template>
          </n-card>
        </div>
      </div>
      <n-flex justify="end">
        <n-pagination v-model:page="curPage" :page-count="pageInfo.totalPages"  @update:page="updatePage" />
      </n-flex>
    </n-spin>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted, computed } from 'vue';
import { NCard, NButton, NSpin } from 'naive-ui';
import useSearchStore from '@/store/search'; // 导入 store
import { useRoute, useRouter } from 'vue-router'; // 导入 useRoute

export default defineComponent({
  components: {
    NCard,
    NButton,
    NSpin
  },
  setup() {
    const loading = ref(false); // 加载状态
    const searchStore = useSearchStore(); // 获取 store 实例
    const route = useRoute(); // 使用 useRoute 获取路由对象
    const router = useRouter();
    let checkInterval = null; // 定时检查的 interval ID

    const selectedPlatform = ref('all'); // 平台筛选
    const selectedOrder = ref('default'); // 价格排序

    const platformOptions = [
      { label: '所有', value: 'all' },
      { label: '京东', value: 'JD' },
      { label: '亚马逊', value: 'AMAZON' }
    ];

    const orderOptions = [
      { label: '默认排序', value: 'default' },
      { label: '价格从低到高', value: 'price_asc' },
      { label: '价格从高到低', value: 'price_desc' }
    ];

    // 自动获取查询参数并触发搜索
    const fetchSearchResults = async () => {
      loading.value = true;
      // 获取查询参数
      const query = route.query;
      const platform = query.platform || 'all' ; // 获取平台参数
      const keyword = query.keyword || ''; // 获取搜索关键词
      selectedOrder.value = query.order || 'default'; //
      selectedPlatform.value = platform;
      const searchParams = {
        "keyword": keyword,
        "order": query.order,
        "platform": platform,
        "pageNo": query.pageNo || 1,
        "pageSize": query.pageSize || 30
      };
      console.log("search params: ", searchParams);

      // 更新 store 中的搜索条件
      await searchStore.updateParam(searchParams);
      loading.value = false;
    };

  const checkLoadingStatus = () => {
    if (loading.value) {
        console.log("Loading is still true, retrying...");
        setTimeout(fetchSearchResults, 5000); // 5秒后重新发出请求
      } else {
        clearInterval(checkInterval); // 取消定时检查
        console.log("Loading is false, stopping interval check.");
      }
  };

    const updatePage = (page) => {
      curPage.value = page; // 更新当前页码
      // 更新路由参数
      router.push({
        query: {
          ...route.query,
          pageNo: page,
        },
      }).then(() => {
        fetchSearchResults(); // 重新触发搜索
      });
    };

    function goToProductPage(id) {
      console.log('goToProductPage', id);
      router.push({
        name: 'item',
        params: { id }
      })
    }

    // 监听 selectedPlatform 和 selectedOrder 的变化
    watch([selectedPlatform, selectedOrder], () => {
      // 更新路由参数
      router.push({
        query: {
          ...route.query,
          platform: selectedPlatform.value,
          order: selectedOrder.value,
        },
      }).then(() => {
        fetchSearchResults(); // 重新触发搜索
      });
    });


    // 从 store 获取商品列表
    const searchResults = computed(() => searchStore.goodsList);
    const pageInfo = computed(() => searchStore.pageInfo);
    const curPage = ref(1);

    onMounted(() => {
      fetchSearchResults(); // 页面加载时触发搜索
      checkInterval = setInterval(checkLoadingStatus, 10000);
    });

    return {
      loading,
      searchResults,
      goToProductPage,
      pageInfo,
      curPage,
      updatePage,
      selectedPlatform,
      selectedOrder,
      platformOptions,
      orderOptions,
      fetchSearchResults
    };
  }
});
</script>

<style scoped>
/* 页面整体容器 */
.container {
  padding: 20px;
  max-width: 1200px;
  /* 最大宽度限制 */
  margin: 0 auto;
  /* 居中对齐 */
  position: relative;

  /* 为绝对定位的内容设置父容器 */
  .image-box {
    padding: 10px;
  }
}
.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
.product-list {
  width: 1200px;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  /* 设置卡片之间的间距 */
}

/* 每一行最多显示5个卡片 */
.product-row {
  flex: 1 1 calc(20% - 16px);
  max-width: calc(20% - 16px);
  box-sizing: border-box;
  margin-bottom: 30px;
}

/* 每个卡片包裹的 div，固定大小 */
/* .product-row {
  flex: 0 0 calc(20% - 16px);
  box-sizing: border-box;
} */

/* 卡片样式 */
.product-card {
  display: flex;
  flex-direction: column;
  height: 370px;
  /* 固定高度 */
  box-sizing: border-box;
  border-radius: 8px;
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  /* 卡片阴影 */
  transition: transform 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  /* 鼠标悬浮时的动画效果 */
}

/* 商品图片 */
/* .product-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-bottom: 1px solid #f1f1f1;
} */

/* 标题样式 */
.product-title {
  height: 45px;
  font-size: 14px;
  font-weight: bold;
  margin-top: 5px;
  /* word-wrap: break-word; */
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color 0.3s ease;
  /* 添加过渡效果，使颜色变化更加平滑 */
}

.product-title:hover {
  color: rgb(221, 0, 0);
  /* 鼠标悬停时字体变红 */
  cursor: pointer;
  /* 鼠标变成可点击手形 */
}


.platform {
  font-size: 12px;
  color: #999;
}

.price {
  font-size: 2em;
  font-weight: bold;
  color: #e74c3c;
  margin-top: 5px;
}

.shop-name {
  color: #8a8a8a;
  text-decoration: none;
}

/* 按钮样式 */
.view-product-btn {
  margin-top: auto;
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  color: #333;
  font-size: 14px;
}


.shop-name:hover {
  text-decoration: underline;
}

/* 商品信息区域 */
.product-info {
  padding: 20px;
  text-align: center;
}
</style>