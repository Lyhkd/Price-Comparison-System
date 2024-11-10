import { defineStore } from 'pinia'

import { SearchPageInfo, SearchPageData, SearchPramas } from '@/types/search'

import { reqSearchData } from '@/api'

const useSearchStore = defineStore('search', {
  state : () => {
    const pageData: SearchPageData = {
      total: 0,
      pageSize: 0,
      pageNo: 0,
      totalPages: 0,
      itemsList: [],
    }

    const searchPramas: SearchPramas = {
      keyword: '111',
      order: '1:desc',
      pageNo: 1,
      pageSize: 10,
      props: [],
      platform: ['all'],
    }

    return { 
      pageData,
      searchPramas
    }
  },

  getters: { 
    goodsList(state) {
      return state.pageData.itemsList
    },
    pageInfo(state): SearchPageInfo  {
      
      return {
        total: state.pageData.total,
        pageNo: state.pageData.pageNo,
        pageSize: state.pageData.pageSize,
        totalPages: state.pageData.totalPages
      }
    },    
    params(state) {
      return state.searchPramas
    },

  },

  actions: { 

    async updatePageData() {
      this.searchPramas.pageNo = 1
      this.pageData = (await reqSearchData(this.searchPramas)) as SearchPageData
    },

    async updateParam(schema: {}) {
      Object.assign(this.searchPramas, schema)
      await this.updatePageData()
    },

    async updateParamAttr(attr: { name: string, value: string | number }) {
      Reflect.set(this.searchPramas, attr.name, attr.value)
      await this.updatePageData()
    },
  

    async deleteParamProps(propValue: string) {
      this.searchPramas.props.splice(this.searchPramas.props.findIndex(m => m === propValue), 1)
      await this.updatePageData()
    },

    async updateParamOrder(order: string) {
      await this.updateParam({ order })
    },   

    async updatePageNum(pageNo: number) {
      Object.assign(this.searchPramas, { pageNo })
      this.pageData = (await reqSearchData(this.searchPramas)) as SearchPageData
    },  

  },
})

export default useSearchStore