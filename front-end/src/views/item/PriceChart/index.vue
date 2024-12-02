<template>
  <div ref="chart" style="height: 400px; margin-top: 20px;"></div>
</template>

<script>
import * as echarts from 'echarts';
import { onMounted, ref } from 'vue';

export default {
  name: 'PriceChart',
  props: {
    priceHistory: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const chart = ref(null);
    let myChart = null; // 保存 ECharts 图表实例

    // 图表更新逻辑
    const updateChart = () => {
      if (!myChart) return;

      const data = props.priceHistory.map(item => ({
        date: item.date,
        price: item.price,
      }));
      console.log("data", data)
      // 计算均价、最高价、最低价
      const prices = data.map(item => item.price);
      const maxPrice = Math.max(...prices);
      const minPrice = Math.min(...prices);
      const epsilon = 1e-6; // 容忍误差范围
      const maxPriceItem = data.find(item => Math.abs(item.price - maxPrice) < epsilon);
      const minPriceItem = data.find(item => Math.abs(item.price - minPrice) < epsilon);

      const maxPriceDate = maxPriceItem ? maxPriceItem.date : '未知';
      const minPriceDate = minPriceItem ? minPriceItem.date : '未知';

      // console.log(maxPriceDate, minPriceDate);
      const option = {
        tooltip: {
          trigger: 'axis',
          formatter: params => {
            const date = params[0].name;
            const price = params[0].value;
            return `${date}<br/>价格: ${price} 元`;
          },
        },
        grid: {
          left: '10%',
          right: '10%',
          top: '20%',
          bottom: '20%',
        },
        xAxis: {
          type: 'category',
          data: data.map(item => item.date),
          axisLabel: {
            fontSize: 13,
          },
          axisLine: {
            lineStyle: {
              color: '#111',
            },
          },
          axisTick: {
            show: true,
          },
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value} 元',
            fontSize: 13,
          },
          axisLine: {
            lineStyle: {
              color: '#111',
            },
          },
          splitLine: {
            lineStyle: {
              type: 'dashed',
              color: '#ddd',
            },
          },
        },
        series: [
          {
            name: '价格',
            type: 'line',
            data: data.map(item => item.price),
            lineStyle: {
              color: '#aaa',
              width: 1.5,
            },
            symbol: 'circle',
            symbolSize: 6,
            itemStyle: {
              color: '#18a058',
            },
            markPoint: {
              data: [
                {
                  type: 'max',
                  name: '最高价格',
                  value: maxPrice,
                  xAxis: maxPriceDate,
                  yAxis: maxPrice,
                  label: {
                    show: true,
                    position: 'top',
                    formatter: `最高价: ${maxPrice} 元\n(${maxPriceDate})`,
                    fontSize: 12,
                    color: '#FFB800',
                  },
                  itemStyle: {
                    color: '#FFB800',
                  },
                },
                {
                  type: 'min',
                  name: '最低价格',
                  value: minPrice,
                  xAxis: minPriceDate,
                  yAxis: minPrice,
                  label: {
                    show: true,
                    position: 'bottom',
                    formatter: `最低价: ${minPrice} 元\n(${minPriceDate})`,
                    fontSize: 12,
                    color: '#18a058',
                  },
                  itemStyle: {
                    color: '#18a058',
                  },
                },
              ],
            },
          },
        ],
      };

      myChart.setOption(option); // 更新图表数据
    };

    // 初始化图表
    onMounted(() => {
      console.log(props.priceHistory)
      myChart = echarts.init(chart.value); // 初始化 ECharts 实例
      updateChart(); // 设置初始数据
    });

    // 监听 props.priceHistory 的变化
    watch(
      () => props.priceHistory,
      () => {
        console.log('priceHistory changed', props.priceHistory);
        updateChart(); // 数据变化时更新图表
      },
      { deep: true } // 深度监听
    );
    return {
      chart
    };
  }
};
</script>

<style scoped>
/* 样式优化 */
.chart {
  background-color: #f4f4f4;
  border-radius: 8px;
}
</style>
