import request, {http} from './request'
import { ApiResponse } from '@/types'
import { LoginData, LoginResponse, RegisterInfo} from '@/types/user'
import { LoginInfo } from '@/types/login'
import { SearchPageData } from '@/types/search'

export const reqCategoryList = () => request({ url: '/product/getBaseCategoryList', method: 'get' })

//search
import { SearchParams } from '@/types/search'
export const reqSearchData = (params: SearchParams) => http.get<SearchPageData>('/search', { params })
//({ url: '/search', method: 'get', data: params })

//detail
//export const reqItemData = (id: number) => request({ url: `/item/${ id }`, method: 'get' })
export const reqItemData = (id: number) => http.get(`/item/${ id }`)
export const reqPriceHistory = (id: number) => http.get(`/item/price/${ id }`)

//price-alert
export const postPriceAlert = (data: any) => http.post('/alert', data)
export const getAlertList = (uid: number) => http.get(`/alert/${ uid }`)
export const updateAlert = (id: number, data: any) => http.put(`/alert/${ id }`, data)
export const getAlertHistory = (id: number) => http.get(`/alert/history/${ id }`)
export const deleteAlert = (id: number) => http.delete(`/alert/${ id }`)

//login
export const reqRegValCode = (email: string) => http.get(`/user/code/${ email }`)
export const postUserSignup = (params: RegisterInfo) => http.post('/user/signup', params)
export const postUserLogin = (params: LoginData) => http.post<LoginResponse>('/user/login', params)
export const getUserLoginInfo = () => http.get<LoginInfo>('/user/auth/loginInfo')
export const logoutUserInfo = () => http.get('/user/logout')
export const updateUserInfo = (data: any) => http.put('/user/auth/loginInfo', data)
//request({ url: `/user/logout`, method: 'get' })

//pay




//要是启用了MOCK就可以使用这里
/*
import requestMock from './request_mock'

//home
export const reqBannerList = () => requestMock({ url: '/home/banner', method: 'get' })
export const reqHomeFloor = () => requestMock({ url: '/home/floor', method: 'get' })
*/
