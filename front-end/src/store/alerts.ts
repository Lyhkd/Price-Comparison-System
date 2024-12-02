import { defineStore } from 'pinia';
import { getAlertList, updateAlert, deleteAlert, getAlertHistory } from '@/api/index';
import { reqPriceHistory } from '@/api/index';
import {priceHistory} from '@/store/item'

interface Alert {
    id: number;
    itemId: number;
    title: string;
    imageUrl: string;
    currentPrice: number;
    enable: boolean;
    targetPrice: number;
    notificationMethod: string;
    createdAt: string;
    alertHistory: AlertHistory[];
    priceHistory: priceHistory[];
}

interface AlertHistory {
    id: number;
    alertId: number;
    priceBefore: number;
    priceAfter: number;
    notificationStatus: string;
    createdAt: string;
}

export const useAlertStore = defineStore('alerts', {
    state: () => ({
        alerts: [] as Alert[],
        loading: false,
        error: null as string | null,
    }),

    getters: {
        alertList(state) {
            return state.alerts;
        },
        isLoading(state) {
            return state.loading;
        },
        hasError(state) {
            return state.error !== null;
        },
    },

    actions: {
        async fetchAlerts(userId: number) {
            this.loading = true;
            this.error = null;
            try {
                this.alerts = await getAlertList(userId);
            } catch (err) {
                this.error = 'Failed to fetch alerts';
            } finally {
                this.loading = false;
            }
        },

        async updateAlert(alertId: number, userId: number, data: any) {
            this.loading = true;
            this.error = null;
            try {
                await updateAlert(alertId, data);
                await this.fetchAlerts(userId);
            } catch (err) {
                this.error = 'Failed to update alert';
            } finally {
                this.loading = false;
            }
        },

        async deleteAlert(alertId: number, userId: number) {
            this.loading = true;
            this.error = null;
            try {
                await deleteAlert(alertId);
                await this.fetchAlerts(userId);
            } catch (err) {
                this.error = 'Failed to delete alert';
            } finally {
                this.loading = false;
            }
        },
    },
});