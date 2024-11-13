import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteMockServe } from 'vite-plugin-mock'

import path from 'path'

import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'


// https://vitejs.dev/config/
export default defineConfig({

  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      'comps': path.resolve(__dirname, 'src/components'),
      'views': path.resolve(__dirname, 'src/views'),
    },
  },   
  // css: {
  //   preprocessorOptions: {
  //     scss: {
  //       additionalData: `@use "src/styles/element/index.scss" as *;`,
  //     },
  //   },
  // },
  plugins: [
    vue(),
    AutoImport({
      imports: [
        'vue',
        {
          'naive-ui': [
            'useDialog',
            'useMessage',
            'useNotification',
            'useLoadingBar'
          ]
        }
      ]
    }),
    Components({
      resolvers: [NaiveUiResolver()]
    }),
    // viteMockServe({
    //   mockPath: './src/mock',
    // }),
  ],
  server:{
    
    proxy:{
      '/api': 'http://localhost:5000'
    }
  }

})
