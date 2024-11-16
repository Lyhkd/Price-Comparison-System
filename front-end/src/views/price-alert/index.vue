<template>
    <div class="price-alert-page">
        <n-row>
            <n-col span="5">
                <UserPanel />
            </n-col>
            <n-col span="1"></n-col>
            <n-col span="18">
                <n-flex vertical justify="space-between">
                    <n-card v-for="product in products" :key="product.id" :hoverable="true" class="product-card"
                        embedded>
                        <n-grid x-gap="12" :cols="24">
                            <n-gi span="5">
                                <img :src="product.image" alt="product" class="product-image" />
                                <div class="reminder-history">
                                    <h3>提醒历史</h3><br />
                                    <n-timeline :reverse="true">
                                        <n-timeline-item v-for="(alert, index) in product.alertHistory.slice(-3)"
                                            :key="index" :title="alert.message" :time="alert.timestamp">
                                        </n-timeline-item>
                                    </n-timeline>
                                </div>
                            </n-gi>
                            <n-gi span="5">
                                <div class="product-card-left">
                                    
                                    <div class="product-info">
                                        <p>{{ product.name }}
                                        </p>
                                        
                                        <p class="product-price">提醒价格：{{ product.price }} 元</p>
                                        

                                        <n-button size="small" @click="editPrice(product)">修改价格</n-button>
                                        <span>提醒方式：</span>
                                        <n-checkbox-group v-model:value="methods">
                                            <n-space item-style="display: flex;">
                                                <n-checkbox value="Email" label="邮箱" />
                                                <n-checkbox value="Message" label="短信" />
                                            </n-space>
                                        </n-checkbox-group>
                                        <span>开启提醒：<n-switch v-model:value="active" /></span>
                                    </div>
                                </div>

                                
                            </n-gi>
                            <n-gi span="14">
                                <div class="product-card-right">
                                    <PriceChart :priceHistory="product.priceHistory.slice(-5)" />
                                </div>
                            </n-gi>
                        </n-grid>


                    </n-card>
                </n-flex>


            </n-col>
        </n-row>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { NCard, NButton, NTimeline, NTimelineItem } from 'naive-ui';
import UserPanel from './UserPanel/index.vue';
import PriceChart from './PriceChart/index.vue'

// 模拟数据
const products = ref([
    {
        id: 1,
        name: '商品 A',
        price: 199,
        image: 'https://via.placeholder.com/150',
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
        alertHistory: [
            { title: '商品 A 价格提醒', timestamp: '2024-10-01', message: '降至 199 元' },
            { title: '商品 A 价格提醒', timestamp: '2024-10-02', message: '降至 199 元' },
        ],
    },
    {
        id: 2,
        name: '商品 B',
        price: 299,
        image: 'https://via.placeholder.com/150',
        priceHistory: [
            { date: '2024-01-01', price: 3199 },
            { date: '2024-02-01', price: 3100 },
            { date: '2024-03-01', price: 2900 },
            { date: '2024-04-01', price: 2800 },
            { date: '2024-05-01', price: 2800 },
            { date: '2024-06-01', price: 2600 },
        ],
        alertHistory: [
            { title: '商品 B 价格提醒', timestamp: '2024-10-02', message: '降至 270 元' },
        ],
    },
    {
        id: 3,
        name: '商品 C',
        price: 199,
        image: 'https://via.placeholder.com/150',
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
        alertHistory: [
            { title: '商品 C 价格提醒', timestamp: '2024-10-01', message: '价格降至 199 元' },
        ],
    },
    {
        id: 4,
        name: '商品 D',
        price: 199,
        image: 'https://via.placeholder.com/150',
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
        alertHistory: [
            { title: '商品 D 价格提醒', timestamp: '2024-10-01 ', message: '价格降至 199 元' },
            { title: '商品 D 价格提醒', timestamp: '2024-10-02', message: '价格降至 199 元' },
        ],
    },
]);

const reminderHistory = ref([
    { title: '商品 A 价格提醒', timestamp: '2024-10-01', message: '价格降至 199 元' },
    { title: '商品 B 价格提醒', timestamp: '2024-10-02', message: '价格降至 270 元' },
]);

const editPrice = (product) => {
    console.log(`修改价格: ${product.name}`);
};

const editAlertMethod = (product) => {
    console.log(`修改提醒方式: ${product.name}`);
};

const active = ref(false)
const methods = ref(null)
</script>

<style scoped>
.price-alert-page {
    display: flex;
    justify-content: space-between;
    padding: 20px;
    width: 1200px;
}

.left-panel {
    width: 20%;
}

.right-panel {
    width: 75%;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.product-card {
    margin-bottom: 30px;
    display: flex;
    justify-content: left;
    padding: 5px;
    /* width: 1000px; */
}

.product-card-left {
    display: flex;
    gap: 15px;
    align-items: center;
}

.product-image {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 8px;
}

.product-info {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.product-price {
    font-weight: bold;
}

.product-card-right {
    /* width: 200px; */
    height: 300px;
}


.reminder-history {
    margin-top: 10px;
    height: auto;
}
</style>