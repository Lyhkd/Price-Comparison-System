import { defineStore } from 'pinia'

import { SearchPageInfo, SearchPageData, SearchParams } from '@/types/search'

import { reqSearchData } from '@/api'

const useSearchStore = defineStore('search', {
  state : () => {
    const pageData: SearchPageData = {
      total: 0,
      pageSize: 0,
      pageNo: 0,
      totalPages: 0,
      items: [],
    }

    const searchParams: SearchParams = {
      keyword: 'iphone',
      order: 'desc',
      pageNo: 1,
      pageSize: 10,
      platform: ['all'],
    }

    return { 
      pageData,
      searchParams,
    }
  },

  getters: { 
    goodsList(state) {
      return state.pageData.items
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
      return state.searchParams
    },

  },

  actions: { 

    async updatePageData() {
      this.searchParams.pageNo = 1
      this.pageData = (await reqSearchData(this.searchParams)) as SearchPageData
    },

    async updateParam(schema: {}) {
      Object.assign(this.searchParams, schema)
      await this.updatePageData()
    },

    // async updateParamAttr(attr: { name: string, value: string | number }) {
    //   Reflect.set(this.searchParams, attr.name, attr.value)
    //   await this.updatePageData()
    // },
  

    // async deleteParamProps(propValue: string) {
    //   this.searchParams.props.splice(this.searchParams.props.findIndex(m => m === propValue), 1)
    //   await this.updatePageData()
    // },

    async updateParamOrder(order: string) {
      await this.updateParam({ order })
    },   

    async updatePageNum(pageNo: number) {
      Object.assign(this.searchParams, { pageNo })
      this.pageData = (await reqSearchData(this.searchParams)) as SearchPageData
    },  

  },
})

export default useSearchStore