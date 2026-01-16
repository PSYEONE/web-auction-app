import { defineStore } from 'pinia';
import { ref } from 'vue';
import type {ProfileUpdate, UserProfile} from '../types/models';
import { api } from '../api/client';

export const useUserStore = defineStore('user', () => {
    const profile = ref<UserProfile | null>(null);
    const loading = ref(false);
    const error = ref<string | null>(null);

    async function fetchProfile(): Promise<void> {
        loading.value = true;
        error.value = null;
        try {
            profile.value = await api.getProfile();
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to fetch profile';
        } finally {
            loading.value = false;
        }
    }

    async function updateProfile(data: ProfileUpdate): Promise<void> {
        loading.value = true;
        error.value = null;
        try {
            profile.value = await api.updateProfile(data);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to update profile';
            throw e;
        } finally {
            loading.value = false;
        }
    }

    function logout(): void {
        profile.value = null;
    }

    return {
        profile,
        loading,
        error,
        fetchProfile,
        updateProfile,
        logout,
    };
});