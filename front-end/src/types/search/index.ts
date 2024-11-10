export interface SearchPageInfo {
  total: number,
  pageSize: number,
  pageNo: number,
  totalPages: number,
}

export interface SearchPramas {
  keyword: string,
  order: string,
  pageNo: number,
  pageSize: number,
  props: string[],
  platform: string[]
}

export interface SearchPageData extends SearchPageInfo {
  itemsList: Items[]
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

