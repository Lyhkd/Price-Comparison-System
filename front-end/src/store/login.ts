import { defineStore } from 'pinia'


import {
  reqRegValCode,
  postUserSignup,
  getUserLoginInfo,
  postUserLogin,
  logoutUserInfo,
  updateUserInfo
} from '@/api'

import {
  getToken,
  setToken,
  removeToken
} from '@/libs/token'

import { LoginInfo }  from '@/types/login'
import user from '@/mock/user'

//1定义并导出容器，容器ID必须唯一
export const useLoginStore = defineStore('useLoginStore', {
  state : () => {
    return { 
      loginInfo : {} as (LoginInfo | undefined),
      isLogin : false,
    }
  },
  getters: {
    userDisplayName: (state) => state.loginInfo?.username,
    userAvatar: (state) => state.loginInfo?.avatar,
    userId: (state) => state.loginInfo?.uid,
    userEmail: (state) => state.loginInfo?.email,
    userPhone: (state) => state.loginInfo?.phone,
  },
  
  //不能使用箭头函数定义actions,因为箭头函数绑定外部this
  actions: {
    async getValCode(email: string) {
      return (await reqRegValCode(email))
    },     
    async register(name: string, email: string, password: string) {
        await postUserSignup({ name, email, password })

    },
    async load() {
      if(getToken()){
        this.loginInfo = (await getUserLoginInfo())
        this.isLogin = true
        //const cartStore = useCartStore()
        //cartStore.loadList()
      }
      
    },
    async login(name: string, password: string) {
      const data : { token: string } = (await postUserLogin({ name, password }))
      if(data.token) {
        setToken(data.token)
        this.load()
        console.log('登录成功', data, this.isLogin)
      }
    },    
    async logout() {
      await logoutUserInfo()        
      removeToken()
      this.loginInfo = undefined
      this.isLogin = false
    },
    async updateUser(data: any) {
      const info = (await updateUserInfo(data))
      if (this.loginInfo!==undefined){
        this.loginInfo.email = info.email
        this.loginInfo.username = info.username
        this.loginInfo.phone = info.phone
      }
    }

  },

  persist: {
    enabled: true,
    strategies: [
      { storage: localStorage, paths: ['isLogin', 'loginInfo'] }
    ],
  },

})

export default useLoginStore