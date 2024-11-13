// 定义用户信息的接口
export interface UserInfo {
    uid: string | null;              // 用户 ID，可以为 null
    avatar: string;                  // 用户头像
    username: string;                // 用户名
    email: string;                   // 用户邮箱
    isLoggedIn: boolean;             // 登录状态
    watchList: Array<WatchItem>;     // 关注的商品列表
    priceCheckInterval: number;      // 价格查询时间间隔（单位为毫秒）
    discountNotifications: NotificationPreferences; // 提醒方式
}

export interface LoginData{
    name: string;
    password: string;
}
export interface LoginInfo {
    username: string,
    uid: string,
    email: string,
    avatar: string,
  }

export interface LoginResponse{
    token: string;
    loginInfo: LoginInfo;
}



export interface RegisterInfo{
    name: string;
    password: string;
    email: string;
}


// 定义关注商品的信息接口
export interface WatchItem {
    id: string;                      // 商品 ID
    name: string;                    // 商品名称
    targetPrice: number;             // 用户设置的目标价格
}

// 定义提醒方式的接口
export interface NotificationPreferences {
    email: boolean;                  // 是否开启邮件提醒
    appPush: boolean;                // 是否开启 App 推送提醒
}
