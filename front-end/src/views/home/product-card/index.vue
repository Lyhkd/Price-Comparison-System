<template>
    <div class="product-card">
      <div class="product-title">{{ product.name }}</div>
      <div class="product-price">¥{{ product.currentPrice.toFixed(2) }}</div>
      <!-- <PriceHistoryChart :priceHistory="product.priceHistory" /> -->
    </div>
  </template>
  
  <script setup>
//   import PriceHistoryChart from './PriceHistoryChart.vue';
  
  const props = defineProps({
    product: Object,
  });
  </script>
  
  <style scoped>
  .product-card {
    width: 250px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .product-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .product-price {
    font-size: 16px;
    color: #e94e77;
    margin-bottom: 15px;
  }
  </style>
  