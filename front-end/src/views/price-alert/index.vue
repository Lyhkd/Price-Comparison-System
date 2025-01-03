<template>
    <div class="price-alert-page">
        <n-row>
            <n-col span="5" v-if="!isMobile">
                <UserPanel />
            </n-col>
            <n-col span="1" v-if="!isMobile"></n-col>
            <n-col :span="mobileSpan">
                <UserPanel v-if="isMobile"/>
                <n-flex vertical justify="space-between">
                    <n-card v-for="alert in alertStore.alertList" :key="alert.id" :hoverable="true" class="product-card"
                        embedded>
                        <n-grid x-gap="12" :cols="mobileSpan2">
                            <n-gi span="5">
                                <img :src="alert.imageUrl" alt="product" class="product-image" />
                                <div class="reminder-history">
                                    <h3>提醒历史</h3><br />
                                    <n-timeline :reverse="true">
                                        <n-timeline-item v-for="(alertHist, index) in validAlertHistory(alert.alertHistory).slice(-3)"
                                            :key="index" :title="generateTitle(alertHist)" :time="generateTime(alertHist.createAt)">
                                        </n-timeline-item>
                                    </n-timeline>
                                </div>
                            </n-gi>
                            <n-gi span="5">
                                <div class="product-card-left">

                                    <div class="product-info">
                                        <n-text @click="goToItem(alert.itemId)" class="alert-title">{{ alert.title }}</n-text>

                                        <p class="product-price">当前价格：{{ alert.currentPrice }} 元</p>

                                        <p class="product-price">提醒价格：{{ alert.targetPrice }} 元</p>
                                        
                                        <span>提醒方式：</span>
                                        <n-radio-group v-model:value="alert.notificationMethod" @change="Update(alert)">
                                                <n-radio-button value="email" label="邮箱" />
                                                <n-radio-button :disabled="!isSmsEnabled" value="sms" label="短信" />
                                        </n-radio-group>
                                        <span>开启提醒：<n-switch v-model:value="alert.enable" @change="Update(alert)"/></span>
                                        <n-space >
                                            <n-button size="small"  @click="editAlert(alert)">修改</n-button>
                                            <n-button size="small" @click="deleteAlert(alert.id)">删除</n-button>
                                        </n-space>
                                    </div>
                                </div>


                            </n-gi>
                            <n-gi span="14" v-if="!isMobile">
                                <div class="product-card-right">
                                    <PriceChart :priceHistory="validAlertHistory(alert.priceHistory).slice(-5)" />
                                </div>
                            </n-gi>
                        </n-grid>


                    </n-card>
                </n-flex>


            </n-col>
        </n-row>
        <!-- 修改警报的 Modal -->
    <n-modal v-model:show="showEdit" style="width: 400px;" title="修改" preset="card" label-placement="left" >
      <n-form :model="editForm">
        <n-form-item label="目标价格" path="targetPrice">
          <n-input-number v-model:value="editForm.targetPrice" />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space>
            
        <n-button @click="showEdit = false">取消</n-button>
        <n-button type="primary" @click="updateAlert">确认</n-button>
    </n-space>
      </template>
    </n-modal>
    
    <!-- 删除警报的确认框 -->
    <n-modal v-model:show="showDelete" style="width: 400px;" title="确认删除" preset="card" label-placement="left" >
      <div>你确定要删除这个提醒吗？</div>
      <template #footer>
        <n-space>
        <n-button @click="showDelete = false">取消</n-button>
        <n-button type="error" @click="deleteAlertConfirmed">确认</n-button>
    </n-space>
      </template>
    </n-modal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { NCard, NButton, NTimeline, NTimelineItem } from 'naive-ui';
import { useRoute, useRouter } from 'vue-router';
import UserPanel from './UserPanel/index.vue';
import PriceChart from './PriceChart/index.vue'
import useLoginStore from '@/store/login';
import { useAlertStore } from '@/store/alerts';
const loginStore = useLoginStore();
const alertStore = useAlertStore();
const router = useRouter();
const generateTime = (time) => {
    console.log(`UTC Time: ${time}`);
    const utcDate = new Date(time);  // 转为 JS 日期对象
    const localDate = new Date(utcDate.getTime() + 8 * 60 * 60 * 1000);  // 转换为北京时间
    const formattedDate = localDate.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    console.log(`Local Time: ${formattedDate}`);
    return formattedDate;
};
const generateTitle = (alertHist) => {
//   const status = alertHist.notificationStatus === 'sent' ? '已提醒' : '未提醒';
  return `价格提醒 ${alertHist.priceAfter} 元`;
};
const validAlertHistory = (alertHistory) => {
  return Array.isArray(alertHistory) ? alertHistory : [];
};

const isSmsEnabled = computed(() => {
  return loginStore.loginInfo?.phone !== null && loginStore.loginInfo?.phone !== '';
});

onMounted(async () => {
        try {
            await alertStore.fetchAlerts(loginStore.userId);
            console.log('Fetched alerts:', alertStore.alertList);
        } catch (err) {
            console.error('Failed to fetch item:', err);
        }
    console.log('price alert page mounted');
});
// 模拟数据
const goToItem = (itemId) => {
  router.push({ path: `/item/${itemId}` });
};

const showEdit = ref(false);
const showDelete = ref(false);
const deleteAlertId = ref(null);

const deleteAlert = (alertId) => {
    console.log('delete alert:', alertId);
  deleteAlertId.value = alertId;
  showDelete.value = true;
  console.log('show delete:', showDelete.value);
};

const deleteAlertConfirmed = async () => {
  await alertStore.deleteAlert(deleteAlertId.value, loginStore.userId); // 假设用户ID为1
  showDelete.value = false;
};

const editForm = ref({
  id: null,
  targetPrice: null,
  notificationMethod: null,
  enable: null,
});

const editAlert = (alert) => {
    console.log('edit alert:', alert);
    editForm.value = { ...alert };
    showEdit.value = true;
};
const updateAlert = async () => {
  await alertStore.updateAlert(editForm.value.id, loginStore.userId, { "targetPrice":editForm.value.targetPrice, "notificationMethod": editForm.value.notificationMethod, "enable": editForm.enable } ); // 假设用户ID为1
  showEdit.value = false;
};
const Update = async (alert) => {
    await alertStore.updateAlert(alert.id, loginStore.userId, { "targetPrice":alert.targetPrice, "notificationMethod": alert.notificationMethod, "enable": alert.enable } ); // 假设用户ID为1
    console.log('method update:', alert);
};

const isMobile = ref(window.innerWidth <= 768);
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
const mobileSpan2 = computed(() => (isMobile.value ? 10 : 24));
</script>

<style scoped>
.price-alert-page {
    display: flex;
    justify-content: space-between;
    padding: 20px;
    width: 1200px;
}

.product-card {
    margin-bottom: 30px;
    display: flex;
    justify-content: left;
    padding: 5px;
    width: 1000px;
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
.alert-title{
    cursor: pointer; 
    font-size: 15px;
    max-height: 70px;
    overflow: hidden;
    text-overflow: ellipsis;
    
}

.alert-title :hover {
  color: #0056b3; /* 悬浮时更深的颜色 */
}

@media (max-width: 768px) {
  .price-alert-page {
    width: 92%;
    align-items: center;
  }

  .product-card {
    flex-direction: column;
    align-items: flex-start;
    margin-top: 15px;
    margin-bottom: 15px;
    width: 100%;
  }

  .product-image {
    width: 100%;
    height: auto;
  }

  .product-card-left {
    flex-direction: column;
    align-items: flex-start;
  }

  .product-info {
    width: 100%;
  }

  .product-card-right {
    width: 100%;
    height: auto;
  }
}
</style>