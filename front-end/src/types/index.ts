export interface Category {
  categoryId: number,
  categoryName: string,
  categoryChild: Category[]
}

export interface Schema {
  id: number,
  text: string
}

export interface Attr {
  id: number,
  text: string,
  children?: Attr[]
}

// src/types/api.ts

// 用泛型 T 表示 data 的类型，使得 ApiResponse 可以适配不同的数据结构
export interface ApiResponse<T = any> {
  code: number     // 表示请求是否成功 0 表示成功，1 表示失败
  message?: string     // 请求返回的消息，例如错误提示
  data?: T             // 返回的数据内容
}