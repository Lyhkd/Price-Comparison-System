// userService.ts
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:5000/api', // Flask 服务器的地址
});

// 验证邮箱格式
export function validateEmail(email: string): boolean {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// 检查用户名和邮箱的唯一性
export async function checkUniqueUser(username: string, email: string): Promise<boolean> {
    const response = await api.post('/check_unique_user', { username, email });
    return response.data.is_unique;
}

// 注册用户到数据库
export async function registerToDatabase(username: string, password: string, email: string): Promise<string> {
    const response = await api.post('/register', { username, password, email });
    if (!response.data.success) throw new Error(response.data.message);
    return response.data.user_id; // 返回用户 ID
}

// 用户登录
export async function authenticateUser(username: string, password: string): Promise<{ success: boolean; uid?: string; email?: string }> {
    const response = await api.post('/login', { username, password });
    return response.data; // 返回登录响应
}

// 获取商品价格
export async function fetchProductPrice(itemId: number): Promise<number> {
    const response = await api.get(`/product_price/${itemId}`);
    return response.data.price; // 返回商品价格
}
