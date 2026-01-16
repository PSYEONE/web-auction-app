import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Item, ItemCreate, BidCreate, QuestionCreate, ReplyCreate } from '../types/models';
import { api } from '../api/client';

export const useItemsStore = defineStore('items', () => {
    const items = ref<Item[]>([]);
    const currentItem = ref<Item | null>(null);
    const loading = ref(false);
    const error = ref<string | null>(null);

    async function fetchItems(search?: string): Promise<void> {
        loading.value = true;
        error.value = null;
        try {
            items.value = await api.getItems(search);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to fetch items';
        } finally {
            loading.value = false;
        }
    }

    async function fetchItem(id: number): Promise<void> {
        loading.value = true;
        error.value = null;
        try {
            currentItem.value = await api.getItem(id);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to fetch item';
        } finally {
            loading.value = false;
        }
    }

    async function createItem(data: ItemCreate): Promise<void> {
        loading.value = true;
        error.value = null;
        try {
            const newItem = await api.createItem(data);
            items.value.unshift(newItem);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to create item';
            throw e;
        } finally {
            loading.value = false;
        }
    }

    async function placeBid(itemId: number, data: BidCreate): Promise<void> {
        loading.value = true;
        error.value = null;
        try {
            await api.placeBid(itemId, data);
            // Refresh the item to get updated bids
            await fetchItem(itemId);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to place bid';
            throw e;
        } finally {
            loading.value = false;
        }
    }

    async function postQuestion(itemId: number, data: QuestionCreate): Promise<void> {
        loading.value = true;
        error.value = null;
        try {
            await api.postQuestion(itemId, data);
            await fetchItem(itemId);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to post question';
            throw e;
        } finally {
            loading.value = false;
        }
    }

    async function replyQuestion(questionId: number, data: ReplyCreate): Promise<void> {
        loading.value = true;
        error.value = null;
        try {
            await api.replyQuestion(questionId, data);
            // Refresh current item if it's loaded
            if (currentItem.value) {
                await fetchItem(currentItem.value.id);
            }
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to reply to question';
            throw e;
        } finally {
            loading.value = false;
        }
    }

    return {
        items,
        currentItem,
        loading,
        error,
        fetchItems,
        fetchItem,
        createItem,
        placeBid,
        postQuestion,
        replyQuestion,
    };
});