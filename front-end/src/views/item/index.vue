<template>
  <div class="product-details">
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
          <div class="product-gallery">
          <image-gallery :images="product.images" />
        </div>

        </n-col>

        <n-col span="10">
          <n-space vertical size="large">
            <div class="product-header">
              <n-space vertical size="small">
                <h1 class="title">{{ product.name }}</h1>
                <n-text depth="3" class="subtitle">{{ product.subtitle }}</n-text>
              </n-space>
            </div>

            <!-- 价格区域 -->
            <n-card class="price-section" embedded>
              <n-space vertical size="small">
                <n-space align="center">
                  <n-text class="price-label">价格</n-text>
                  <n-text class="current-price">¥{{ product.price }}</n-text>
                  <n-tag v-if="product.discount" type="error" size="small">
                    {{ product.discountText }}
                  </n-tag>
                </n-space>
                <n-text class="original-price" v-if="product.originalPrice">
                  原价: <span class="line-through">¥{{ product.originalPrice }}</span>
                </n-text>
              </n-space>
            </n-card>

            <!-- 商品信息区域 -->
            <n-card embedded>
              <n-grid :cols="24" :x-gap="12" :y-gap="8">
                <n-grid-item :span="6">
                  <n-text depth="3">品牌</n-text>
                </n-grid-item>
                <n-grid-item :span="18">
                  <n-space>
                    <n-avatar
                      v-if="product.brandLogo"
                      :src="product.brandLogo"
                      :size="24"
                    />
                    <n-text>{{ product.brand }}</n-text>
                  </n-space>
                </n-grid-item>

                <n-grid-item :span="6">
                  <n-text depth="3">产地</n-text>
                </n-grid-item>
                <n-grid-item :span="18">
                  <n-text>{{ product.origin }}</n-text>
                </n-grid-item>

                <n-grid-item :span="6">
                  <n-text depth="3">库存</n-text>
                </n-grid-item>
                <n-grid-item :span="18">
                  <n-text>{{ product.stock }}件</n-text>
                </n-grid-item>

                <n-grid-item :span="6">
                  <n-text depth="3">类别</n-text>
                </n-grid-item>
                <n-grid-item :span="18">
                  <n-space>
                    <n-tag v-for="cat in product.categories" :key="cat">
                      {{ cat }}
                    </n-tag>
                  </n-space>
                </n-grid-item>

                <n-grid-item :span="6">
                  <n-text depth="3">店铺</n-text>
                </n-grid-item>
                <n-grid-item :span="18">
                  <n-text>{{ product.shop }}</n-text>
                </n-grid-item>

                <n-grid-item :span="6">
                  <n-text depth="3">渠道</n-text>
                </n-grid-item>
                <n-grid-item :span="18">
                  <n-text>{{ product.platform.name }}</n-text>
                </n-grid-item>
              </n-grid>
            </n-card>

            <!-- 价格提醒 -->
            <n-button
              type="info"
              secondary
              block
              @click="addToPriceAlert"
              class="alert-button"
            >
              <template #icon>
                <n-icon><NotificationsOutline /></n-icon>
              </template>
              添加价格提醒
            </n-button>
          </n-space>

        </n-col>
      </n-row>
        <!-- 左侧图片展示区 -->
        

        <!-- 右侧商品信息区 -->
        
      <!-- 历史价格走势图 -->
      <n-card class="price-history" embedded>
        <n-tabs type="line" animated size="large">
      <n-tab-pane name="历史价格走势" tab="历史价格走势">
        <price-chart :priceHistory="product.priceHistory" />
      </n-tab-pane>
    </n-tabs>
      </n-card>
      

      <!-- 相关商品推荐 -->
      <n-card class="related-products" embedded>
        <template #header>
          <n-space align="center">
            <n-icon><apps-outline /></n-icon>
            <n-text>相关商品推荐</n-text>
          </n-space>
        </template>
        <n-grid :cols="4" :x-gap="12" responsive="screen">
          <n-grid-item v-for="item in relatedProducts" :key="item.id">
            <n-card hoverable class="related-product-card">
              <template #cover>
                <img :src="item.image" :alt="item.name" class="related-product-image"/>
              </template>
              <n-space vertical>
                <n-text class="related-product-name">{{ item.name }}</n-text>
                <n-text type="error">¥{{ item.price }}</n-text>
              </n-space>
            </n-card>
          </n-grid-item>
        </n-grid>
      </n-card>

    </n-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { NCard, NButton, NTag } from 'naive-ui'
import ImageGallery from './ImageGallery/index.vue'
import PriceChart from '@/components/PriceChart/index.vue'
import {NotificationsOutline} from "@vicons/ionicons5";
const product = ref({
  id: '1',
  name: '一加 13 16GB+512GB 白露晨曦 高通骁龙®8至尊版 6000mAh 冰川电池 AI智能游戏手机 旗舰影像性能手机',
  description: '一款最新的智能手机，具备极高性价比。采用最新处理器，搭载高清摄像头，支持快速充电。',
  price: 2999,
  originalPrice: 3499,
  discount: true,
  discountText: '特价',
  category: '手机数码',
  origin: '中国广东',
  stock: 999,
  shop: "京东自营",
  images: [
    'https://img14.360buyimg.com/n0/jfs/t1/188881/37/48138/79664/6731d9b9F6687d116/1da6c8a74922838d.jpg',
    'https://img14.360buyimg.com/n0/jfs/t1/197364/36/44790/38276/67232fdbFeb5046c9/ae8082fa9ad66ae3.jpg',
    'https://img14.360buyimg.com/n0/jfs/t1/204657/25/46978/60818/6714e372F5a1993b4/c5b58415ff76bb7d.png'
  ],
  priceHistory: [
    { date: '2024-01-01', price: 3499 },
    { date: '2024-02-01', price: 3199 },
    { date: '2024-03-01', price: 2999 },
    { date: '2024-04-01', price: 2899 },
    { date: '2024-05-01', price: 2899 },
    { date: '2024-06-01', price: 2099 },
    { date: '2024-07-01', price: 2899 },
    { date: '2024-08-01', price: 3799 },
  ],
  platform: 
    {
      name: '京东',
      url: 'https://jd.com/product/12345',
      icon: '/icons/jd.png'
    }
})

const relatedProducts = ref([
  {
    id: '2',
    name: '智能手机 ABC',
    price: 2499,
    image: 'https://example.com/related1.jpg'
  },
  {
    id: '3',
    name: '智能手机 DEF',
    price: 3299,
    image: 'https://example.com/related2.jpg'
  },
  {
    id: '4',
    name: '智能手机 GHI',
    price: 2799,
    image: 'https://example.com/related3.jpg'
  },
  {
    id: '5',
    name: '智能手机 JKL',
    price: 3599,
    image: 'https://example.com/related4.jpg'
  }
])

const goToPlatform = (url) => {
  window.open(url, '_blank')
}

const addToPriceAlert = () => {
  // 实现添加价格提醒的逻辑
  console.log('添加价格提醒')
}
</script>

<style scoped>
.product-details {
  background-color: #f5f5f5;
  padding: 20px;
}

.bread-box{
  padding: 10px 20px;
  margin-bottom: 20px;
}
.product-card {
  background-color: white;
  border-radius: 8px;
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

.related-product-name {
  font-size: 14px;
  line-height: 1.4;
  height: 40px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.line-through {
  text-decoration: line-through;
}
</style>