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

    onMounted(() => {
      const myChart = echarts.init(chart.value);
      const data = props.priceHistory.map(item => ({
        date: item.date,
        price: item.price
      }));

      // 计算均价、最高价、最低价
      const prices = data.map(item => item.price);
      const maxPrice = Math.max(...prices);
      const minPrice = Math.min(...prices);
      const avgPrice = prices.reduce((acc, cur) => acc + cur, 0) / prices.length;
      const maxPriceDate = data.find(item => item.price === maxPrice).date;
      const minPriceDate = data.find(item => item.price === minPrice).date;

      const option = {
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            const date = params[0].name;
            const price = params[0].value;
            return `${date}<br/>价格: ${price} 元`;
          }
        },
        grid: {
          left: '10%',
          right: '10%',
          top: '20%',
          bottom: '20%'
        },
        xAxis: {
          type: 'category',
          data: data.map(item => item.date),
          axisLabel: {
            fontSize: 13
          },
          axisLine: {
            lineStyle: {
              color: '#111'
            }
          },
          axisTick: {
            show: true
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value} 元',
            fontSize: 13
          },
          axisLine: {
            lineStyle: {
              color: '#111'
            }
          },
          splitLine: {
            lineStyle: {
              type: 'dashed',
              color: '#ddd'
            }
          }
        },
        series: [{
          name: '价格',
          type: 'line',
          data: data.map(item => item.price),
          lineStyle: {
            color: '#aaa',
            width: 1.5
          },
          symbol: 'circle',
          symbolSize: 6,
          itemStyle: {
            color: '#18a058'
          },
          // markLine: {
          //   symbol: ['none', 'none'],
          //   data: [
          //     { name: '最高价格', yAxis: maxPrice, lineStyle: { color: '#ff0000', type: 'solid', } },
          //     { name: '最低价格', yAxis: minPrice, lineStyle: { color: '#00ff00', type: 'solid' } },
          //     { name: '均价', yAxis: avgPrice, lineStyle: { color: '#0000ff', type: 'dotted' } }
          //   ]
          // },
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
                  color: '#FFB800'  // 深蓝色
                },
                itemStyle: {
                  color: '#FFB800'  // 深蓝色
                }
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
                  color: '#18a058'  // 金色
                },
                itemStyle: {
                  color: '#18a058'  // 金色
                }
              }
            ]
          }

        }]
      };

      myChart.setOption(option);
    });

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
