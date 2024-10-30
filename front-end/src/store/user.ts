/** 用户全局数据 */

import { defineStore } from 'pinia';

// 定义用户信息的接口
interface UserInfo {
    [key: string]: any; // 可以根据具体的用户信息结构定义详细的属性类型
}

// 辅助函数：从localStorage中获取数据
function getStorageData(key: string): any {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

// 辅助函数：将数据存入localStorage
function setStorageData(key: string, value: any): void {
    localStorage.setItem(key, JSON.stringify(value));
}

export const userDataStore = defineStore('userDataStore', {
    state: () => {
        /** 校验数据 */
        let userInfo: UserInfo = getStorageData('user-container');
        if (typeof userInfo !== 'object') {
            userInfo = {};
        }
        return {
            userInfo: userInfo || {}, // 当前登录用户的基础数据
            userMenuConfigNameMap: [] as string[], // 用户自定义的目录name配置（有该配置表示拥有该目录权限）
            userMenuConfigPathMap: [] as string[], // 用户自定义的目录path配置（有该配置表示拥有该目录权限）
            userMenuList: [] as any[], // 用于展示的菜单列表，结构树形化
            tagsMap: {} as Record<string, any>, // 页面标签MAP，layoutName为键名
            iframeList: [] as any[], // iframe 数组，iframe也属于标签，跟标签挂钩
        };
    },
    getters: {},
    actions: {
        setUserInfo(value: UserInfo): void {
            this.userInfo = value || {};
            /** 存入缓存 */
            setStorageData('user-container', value);
        },
        setUserMenuConfigNameMap(value: string[]): void {
            this.userMenuConfigNameMap = value || [];
        },
        setUserMenuConfigPathMap(value: string[]): void {
            this.userMenuConfigPathMap = value || [];
        },
        setUserMenuList(value: any[]): void {
            this.userMenuList = value || [];
        },
        setTagsMap(value: Record<string, any>): void {
            this.tagsMap = value || {};
        },
        setIframeList(value: any[]): void {
            this.iframeList = value || [];
        },
    },
});
