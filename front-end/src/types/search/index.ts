export interface SearchPageInfo {
  total: number,
  pageSize: number,
  pageNo: number,
  totalPages: number,
}

export interface SearchParams {
  keyword: string,
  order: string,
  pageNo: number,
  pageSize: number,
  platform: string[]
}

export interface SearchPageData extends SearchPageInfo {
  items: Items[]
}


export interface Items {
  id: number,
  defaultImg: string,
  currentPrice: number,
  title: string,
  link: string,
  shopName: string,
  shopLink: string,
  platform: string,
}

