<template>
  <div class="product-details">
    <n-spin :show="loading">
    <n-card class="product-card">
      <n-row>
        <n-col span="24" class="bread-box">
          <n-breadcrumb>
            <n-breadcrumb-item to="/">首页</n-breadcrumb-item>
            <n-breadcrumb-item>商品详情</n-breadcrumb-item>
          </n-breadcrumb>
        </n-col>
      </n-row>

      <n-row>
        <n-col span="2">
        </n-col>
        <n-col span="10">
          <div class="product-gallery" v-if="!isMobile">
            <img :src="store.itemData.imageUrl" alt="商品图片" class="product-image" />
            <!-- <image-gallery :images="store.itemData.imgList" /> -->
          </div>

        </n-col>

        <n-col :span="mobileSpan">
          <div class="image-container" v-if="isMobile">
            <img :src="store.itemData.imageUrl" alt="商品图片" class="product-image" />
            <!-- <image-gallery :images="store.itemData.imgList" /> -->
          </div>
          <n-space vertical size="large">
            <div class="product-header">
              <n-space vertical size="small">
                <a class="title-link" :href="store.itemData.link" target="_blank">
                  <h1 class="title">{{ store.itemData.title }}</h1>
                </a>

              </n-space>
            </div>

            <!-- 价格区域 -->
            <n-card class="price-section" embedded>
              <n-space vertical size="small">
                <n-space align="center">
                  <n-text class="price-label">价格</n-text>
                  <n-text class="current-price">¥{{ store.itemData.currentPrice }}</n-text>
                  <n-tag type="error" size="small">
                    特价
                  </n-tag>
                </n-space>
              </n-space>
            </n-card>

            <!-- 商品信息区域 -->
            <n-card embedded>

              <n-descriptions label-placement="top" title="商品详情" size="small">
                <n-descriptions-item v-for="(value, key) in store.itemData.attrs" :key="key" :label="key">
                  {{ value }}
                </n-descriptions-item>
                <n-descriptions-item label="店铺">
                  <a :href="store.itemData.shopLink" target="_blank">{{ store.itemData.shop }}</a>
                </n-descriptions-item>
              </n-descriptions>

            </n-card>

            <!-- 价格提醒 -->
            <n-button type="info" secondary block @click="addToPriceAlert" class="alert-button">
              <template #icon>
                <n-icon>
                  <NotificationsOutline />
                </n-icon>
              </template>
              添加价格提醒
            </n-button>

          </n-space>

        </n-col>
      </n-row>
      <!-- 左侧图片展示区 -->

      <n-modal v-model:show="showDialog" title="设置价格提醒" preset="card" style="width: 400px; max-width: 90%;">
        <n-form ref="priceForm" :model="form" label-placement="left" class="alert-form">
          <n-form-item label="价格" path="price">
            <n-input-number v-model:value="form.price" placeholder="请输入希望的价格" />
          </n-form-item>
          <n-form-item label="提醒方式" path="method">
            <n-select v-model:value="form.method" :options="methods" placeholder="请选择提醒方式" />
          </n-form-item>
        </n-form>
        <template #action>
          <n-space justify="end">
            <n-button @click="showDialog = false">取消</n-button>
            <n-button type="primary" @click="handleSubmit">确定</n-button>
          </n-space>
        </template>
      </n-modal>
      <!-- 右侧商品信息区 -->

      <!-- 历史价格走势图 -->
      <n-card class="price-history" embedded>
        <n-tabs type="line" animated size="large">
          <n-tab-pane name="历史价格走势" tab="历史价格走势">
            <price-chart :priceHistory="store.priceHistory" />
          </n-tab-pane>

        </n-tabs>
      </n-card>


    </n-card>
  </n-spin>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { NCard, NButton, NTag } from 'naive-ui'
import PriceChart from './PriceChart/index.vue'
import { NotificationsOutline } from "@vicons/ionicons5";
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useItemStore } from '@/store/item';
import useLoginStore from '@/store/login';
const route = useRoute();
const router = useRouter();
const store = useItemStore();
const loginStore = useLoginStore();
const isMobile = ref(window.innerWidth <= 768);
const loading = ref(true); // 加载状态
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768;
};
onMounted(() => {
  window.addEventListener('resize', handleResize);
  handleResize(); // 初始化检查
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
});
const mobileSpan = computed(() => (isMobile.value ? 24 : 12));

onMounted(async () => {
  const itemId = route.params.id;
  if (itemId) {
    try {
      console.log("fetching item", itemId);
      await store.fetchItem(itemId);
      console.log("attrs", store.itemDetail.attrs)
      if (!(store.itemDetail.attrs && store.itemDetail.attrs.length > 0)) {
        setTimeout(async () => {
        console.log("fetching item decription again after 3 seconds", itemId);
        await store.updateDescription(itemId);
      }, 5000);
      }
      
    } catch (err) {
      console.error('Failed to fetch item:', err);
    } finally {
      loading.value = false; // 数据加载完成后设置为 false
    }
  }
});



const methods = [
  { label: '短信', value: 'sms' },
  { label: '邮件', value: 'email' },
]; // 提醒方式选项

const handleSubmit = async () => {
  console.log(store.itemData.id, store.itemId)
  const data = {
    "targetPrice": form.value.price,
    "notificationMethod": form.value.method,
    "userId": loginStore.userId,
    "itemId": store.itemId,
  }
  await store.addAlert(data);
  console.log(form.value);
  showDialog.value = false;
};

const showDialog = ref(false); // 控制对话框显示

const form = ref({
  price: store.itemData.currentPrice,
  method: null,
}); // 表单数据

watch(() => store.itemData.currentPrice, (newPrice) => {
  form.value.price = newPrice;  // 如果 currentPrice 变化了，更新 form.price
});


const addToPriceAlert = () => {
  console.log(loginStore.isLogin);
  console.log('user ID', loginStore.userId)
  if (loginStore.isLogin) {
    showDialog.value = true;
  } else {
    // 未登录，跳转到登录页面
    router.push({ path: '/auth', query: { mode: 'login' } });
  }
  console.log('添加价格提醒')
}
</script>

<style scoped>
.product-details {
  background-color: #f5f5f5;
  padding: 20px;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  min-height: 100vh; /* 确保背景高度至少为视口高度 */
}

.bread-box {
  padding: 10px 20px;
  margin-bottom: 20px;
}

.product-image {
  width: 80%;
  margin-bottom: 20px; /* 添加间隔 */
  border: 1px solid #ddd; /* 添加边框 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

.product-card {
  width: 1200px; /* 最大宽度限制 */
  background-color: white;
  border-radius: 8px;
  /* align-items: center; */
  /* display: flex; */
  /* flex-direction: column; */
}


.title {
  font-size: 22px;
  font-weight: bold;
  margin: 0;
  line-height: 1.4;
}

.subtitle {
  font-size: 14px;
}

.description-box {
  margin: 5px 0;
  line-height: 1.6;
  color: #666;
}

.price-section {
  background: #fafafa;
}

.price-label {
  font-size: 14px;
  color: #666;
}

.current-price {
  font-size: 28px;
  color: #f5222d;
  font-weight: bold;
}

.original-price {
  color: #999;
  font-size: 14px;
}

.platform-button {
  height: 40px;
}

.platform-icon {
  margin-right: 4px;
}

.alert-button {
  margin-top: 16px;
}

.price-history {
  margin-top: 24px;
}

.related-products {
  margin-top: 24px;
}

.related-product-card {
  transition: transform 0.2s;
}

.related-product-card:hover {
  transform: translateY(-4px);
}

.related-product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}



.line-through {
  text-decoration: line-through;
}

.alert-form {
  width: 300px;

}

/* .title-link {
  text-decoration: none; 
}

.title {
  color: black; 
  transition: color 0.3s; 
}

.title-link:hover .title {
  color: red; 
  cursor: pointer;
} */

 /* 媒体查询，适配移动端 */
@media (max-width: 768px) {
  .product-image {
    width: 80%;
    max-width: 300px;
    align-items: center;
  margin-bottom: 20px; /* 添加间隔 */
  border: 1px solid #ddd; /* 添加边框 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  }

  .product-card{
    width: 100%;
    justify-content: center;
  }

  .bread-box {
    padding: 5px 10px;
    margin-bottom: 10px;
  }

  .title {
    font-size: 18px;
  }

  .current-price {
    font-size: 24px;
  }

  .related-product-image {
    height: 150px;
  }
  
}


.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}
</style>