/** 用户全局数据 */

import { defineStore } from 'pinia';
import { UserInfo } from '@/types/user';

// 辅助函数：从localStorage中获取数据
function getStorageData(key: string): any {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

// 辅助函数：将数据存入localStorage
function setStorageData(key: string, value: any): void {
    localStorage.setItem(key, JSON.stringify(value));
}

export const useUserStore = defineStore('useUserStore', {
    state: () => {
        /** 校验数据 */
        let userInfo: UserInfo = getStorageData('user-container');
        return {
            userInfo: userInfo || {},
            isLoggedIn: false,
            watchList: [] as Array<{ id: string; name: string; targetPrice: number }>,
            priceCheckInterval: 6 * 60 * 60 * 1000, // 价格查询时间间隔（6小时，毫秒为单位）
            discountNotifications: { email: false, appPush: false } as { email: boolean; appPush: boolean },
        };
    },
    getters: {
        isAuthenticated: (state) => state.isLoggedIn,
        getUserDetails: (state) => ({ uid: state.userInfo.uid, username: state.userInfo.username, email: state.userInfo.email }),
    },
    actions: {
        setUid(newUid: string) {
            this.userInfo.uid = newUid;
            this.isLoggedIn = true;
          },
          logout() {
            this.userInfo.uid = null;
            this.isLoggedIn = false;
          },
          setUserInfo(value: UserInfo): void {
            this.userInfo = value || {};
            /** 存入缓存 */
            setStorageData('user-container', value);
          },

        // async registerUser(username: string, password: string, email: string) {
        //     if (username.length < 6 || password.length < 6 || !this.validateEmail(email)) {
        //       throw new Error('信息无效');
        //     }
      
        //     // 检查用户名和邮箱是否唯一，假设用伪代码与服务端通信
        //     const isUnique = await checkUniqueUser(username, email);
        //     if (!isUnique) throw new Error('用户名或邮箱已存在');
      
        //     // 注册用户到数据库（伪代码）
        //     const userId = await registerToDatabase(username, password, email);
        //     this.uid = userId;
        //     this.username = username;
        //     this.email = email;
        //     this.isLoggedIn = true;
        //   },
      
        //   // 用户登录
        //   async loginUser(username: string, password: string) {
        //     // 检查用户名和密码的正确性（假设服务端验证）
        //     const response = await authenticateUser(username, password);
        //     if (!response.success) throw new Error('用户名或密码错误');
      
        //     // 设置登录状态
        //     this.uid = response.uid;
        //     this.username = username;
        //     this.email = response.email;
        //     this.isLoggedIn = true;
        //   },
      
        //   // 退出登录
        //   logout() {
        //     this.uid = null;
        //     this.username = '';
        //     this.email = '';
        //     this.isLoggedIn = false;
        //   },
      
        //   // 添加到商品关注列表
        //   addToWatchList(item: { id: string; name: string; targetPrice: number }) {
        //     this.watchList.push(item);
        //   },
      
        //   // 定时查询商品最新价格
        //   async checkPrices() {
        //     setInterval(async () => {
        //       for (const item of this.watchList) {
        //         const currentPrice = await fetchProductPrice(item.id); // 获取商品价格
        //         if (currentPrice <= item.targetPrice) {
        //           this.sendNotification(item); // 发送降价提醒
        //         }
        //       }
        //     }, this.priceCheckInterval);
        //   },
      
        //   // 设置提醒方式
        //   setNotificationPreferences({ email, appPush }: { email: boolean; appPush: boolean }) {
        //     this.discountNotifications = { email, appPush };
        //   },
      
        //   // 发送提醒
        //   sendNotification(item: { id: string; name: string; targetPrice: number }) {
        //     if (this.discountNotifications.email) {
        //       sendEmailNotification(this.email, item); // 假设的发送邮件函数
        //     }
        //     if (this.discountNotifications.appPush) {
        //       sendAppPushNotification(item); // 假设的发送推送函数
        //     }
        //   },
      
        //   // Helper: 验证邮箱格式
        //   validateEmail(email: string) {
        //     const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        //     return emailRegex.test(email);
        //   },
        },
    
});
