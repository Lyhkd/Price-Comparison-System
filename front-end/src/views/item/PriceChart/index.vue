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
  
        const option = {
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: data.map(item => item.date),
            axisLabel: {
              rotate: 45
            }
          },
          yAxis: {
            type: 'value'
          },
          series: [{
            data: data.map(item => item.price),
            type: 'line',
            smooth: true,
            lineStyle: {
              color: '#ff5733'
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
  /* 可以根据需要调整折线图样式 */
  </style>
  