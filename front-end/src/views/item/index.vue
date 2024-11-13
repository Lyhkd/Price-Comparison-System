<template>
    <div class="product-details">
      <n-card class="product-card">
        <div class="product-header">
          <!-- 商品名称和描述 -->
          <div class="product-title">
            <h2>{{ product.name }}</h2>
            <p class="product-description">{{ product.description }}</p>
          </div>
          
          <div class="product-price">
            <n-tag :type="product.discount ? 'error' : 'success'" size="small">
              {{ product.discount ? '折扣' : '原价' }}: ¥{{ product.price }}
            </n-tag>
          </div>
        </div>
  
        <!-- 商品图片轮播 -->
        <image-gallery :images="product.images" />
  
        <!-- 历史价格折线图 -->
        <price-chart :priceHistory="product.priceHistory" />
  
        <!-- 各平台跳转链接 -->
        <platform-links :links="product.platformLinks" />
      </n-card>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { NCard, NAvatar, NTag } from 'naive-ui';
  import ImageGallery from '@/views/item/ImageGallery/index.vue';
  import PriceChart from '@/views/item/PriceChart/index.vue';
  import PlatformLinks from '@/views/item/PlatformLinks/index.vue';
  
  export default {
    name: 'ProductDetails',
    components: {
      NCard,
      NAvatar,
      NTag,
      ImageGallery,
      PriceChart,
      PlatformLinks
    },
    setup() {
      const product = ref({
        name: '智能手机 XYZ',
        description: '一款最新的智能手机，具备极高性价比。',
        price: 2999,
        discount: true,
        image: 'https://example.com/product-image.jpg',
        images: [
          'https://images.pexels.com/photos/28147837/pexels-photo-28147837.jpeg',
          'https://images.pexels.com/photos/10123484/pexels-photo-10123484.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load',
          'https://images.pexels.com/photos/29037372/pexels-photo-29037372.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load'
        ],
        priceHistory: [
          { date: '2024-01-01', price: 3499 },
          { date: '2024-02-01', price: 3199 },
          { date: '2024-03-01', price: 2999 },
          { date: '2024-04-01', price: 2899 }
        ],
        platformLinks: [
          { name: '淘宝', url: 'https://taobao.com/product/12345' },
          { name: '京东', url: 'https://jd.com/product/12345' },
          { name: '拼多多', url: 'https://pinduoduo.com/product/12345' }
        ]
      });
  
      return {
        product
      };
    }
  };
  </script>
  
  <style scoped>
  .product-details {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .product-card {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .product-header {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .product-title h2 {
    font-size: 2rem;
    font-weight: bold;
    margin: 0;
  }
  
  .product-description {
    font-size: 1rem;
    color: #666;
  }
  
  .product-price {
    margin-top: 10px;
  }
  
  .product-price .n-tag {
    font-size: 1.2rem;
    font-weight: bold;
    color: #ff5733; /* 示例颜色 */
  }
  
  .product-info {
    margin-top: 20px;
  }
  
  .product-links {
    margin-top: 20px;
  }
  
  @media (max-width: 768px) {
    .product-card {
      padding: 10px;
    }
  
    .product-title h2 {
      font-size: 1.5rem;
    }
  
    .product-description {
      font-size: 0.9rem;
    }
  }
  </style>
  