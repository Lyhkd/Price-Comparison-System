// mock/user.ts
// mock/user.ts


export default [
    // 用户登录
    {
        url: "/api/user/login",
        method: "post",
        response: (res) => {
            return {
                code: 0,
                message: 'success',
                data: {
                    token: "Token"
                }
            }
        }
    },{
        url: "/api/user/signup",
        method: "post",
        response: (res) => {
            return {
                code: 0,
                message: 'success',
                data: {}
            }
        }
    },
    // 获取用户信息
    {
        url: "/api/user/auth/loginInfo",
        method: "get",
        response: (res) => {
            return {
                code: 0,
                message: 'success',
                data: {
                    uid: "3220102179",
                    username: "UserABC",
                    password: "123456",
                    email: "K@qq.com",
                    avatar: "https://i.pinimg.com/564x/5b/e6/2b/5be62baf1715a8b7c16cd0c7348b3365.jpg",
                }
            }
        }
    },

    // 一个失败的请求
    {
        url: "/api/error",
        method: "get",
        response: (res) => {
            return {
                code: 1,
                message: '密码错误',
                data: null
            }
        }
    }
]
