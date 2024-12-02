import { defineStore } from 'pinia';
import { reqItemData, reqPriceHistory, postPriceAlert } from '@/api';
interface Item {
    id: number;
    title: string;
    link: string;
    imageUrl: string;
    currentPrice: number;
    shop: string;
    shopLink: string;
    platform: string;
    attrs: Record<string, any>;
    imgList: string[];
}

export interface priceHistory{
    date: string;
    price: number;
}

interface AddAlert{
    userID: number;
    itemID: number;
    targetPrice: number;
    notificationMethod: string;
}

export const useItemStore = defineStore('item', {
    state : () => {
        const itemData: Item = {
            id: 0,
            title: '',
            link: '',
            imageUrl: '',
            currentPrice: 0,
            shop: '',
            shopLink: '',
            platform: '',
            attrs: {},
            imgList: [],
        }
    
        const priceHistory: priceHistory[] = [
            {date: '2099-01-01', price: 0}
        ]

        return { 
          itemData,
          priceHistory
        }
      },
    
      getters: { 
        itemDetail(state) {
            return state.itemData
            },
        itemId(state) {
            return state.itemData.id
        },
        itemPrice(state) {
            return state.itemData.currentPrice
        },
      },
    actions: {
        async fetchItem(itemId: number) {
                this.itemData = (await reqItemData(itemId)) as Item
                this.priceHistory = (await reqPriceHistory(itemId)) as priceHistory[]
                console.log(this.priceHistory)
        },   
        async addAlert(data: AddAlert) {
            await postPriceAlert(data)
            console.log('add alert', data)
        }  
    },
});