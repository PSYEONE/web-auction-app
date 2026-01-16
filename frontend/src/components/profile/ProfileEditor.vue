<template>
  <div class="profile-editor">
    <form @submit.prevent="submitProfile">
      <div style="margin-bottom: 16px; text-align: center;">
        <img
            v-if="previewImage || profile.profile_image"
            :src="previewImage || profile.profile_image"
            alt="Profile"
            style="width: 128px; height: 128px; border: 2px solid var(--win-black); object-fit: cover;"
        />
        <div v-else style="width: 128px; height: 128px; border: 2px solid var(--win-black); background: var(--win-light-gray); display: inline-flex; align-items: center; justify-content: center;">
          No Image
        </div>
      </div>

      <div style="margin-bottom: 12px;">
        <label style="display: block; margin-bottom: 4px;">
          <strong>Profile Image:</strong>
        </label>
        <input
            type="file"
            accept="image/*"
            @change="handleImageChange"
            class="input-retro"
        />
      </div>

      <div style="margin-bottom: 12px;">
        <label style="display: block; margin-bottom: 4px;">
          <strong>Username:</strong>
        </label>
        <input
            :value="profile.username"
            type="text"
            class="input-retro"
            disabled
        />
      </div>

      <div style="margin-bottom: 12px;">
        <label style="display: block; margin-bottom: 4px;">
          <strong>Email:</strong>
        </label>
        <input
            v-model="formData.email"
            type="email"
            class="input-retro"
            required
        />
      </div>

      <div style="margin-bottom: 16px;">
        <label style="display: block; margin-bottom: 4px;">
          <strong>Date of Birth:</strong>
        </label>
        <input
            v-model="formData.date_of_birth"
            type="date"
            class="input-retro"
        />
      </div>

      <button
          type="submit"
          class="btn-retro"
          :disabled="userStore.loading"
          style="width: 100%;"
      >
        {{ userStore.loading ? 'Saving...' : 'Save Profile' }}
      </button>

      <p v-if="error" style="color: red; margin-top: 12px;">
        {{ error }}
      </p>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import type { UserProfile, ProfileUpdate } from '../../types/models';
import { useUserStore } from '../../stores/user';

export default defineComponent({
  name: 'ProfileEditor',
  props: {
    profile: {
      type: Object as PropType<UserProfile>,
      required: true,
    },
  },
  emits: ['profile-updated'],
  data() {
    return {
      userStore: useUserStore(),
      formData: {
        email: this.profile.email,
        date_of_birth: this.profile.date_of_birth || '',
        profile_image: null as File | null,
      },
      previewImage: null as string | null,
      error: null as string | null,
    };
  },
  methods: {
    handleImageChange(event: Event): void {
      const target = event.target as HTMLInputElement;
      const file = target.files?.[0];
      if (file) {
        this.formData.profile_image = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.previewImage = e.target?.result as string;
        };
        reader.readAsDataURL(file);
      }
    },
    async submitProfile(): Promise<void> {
      this.error = null;
      try {
        await this.userStore.updateProfile({
          email: this.formData.email,
          date_of_birth: this.formData.date_of_birth || null,
          profile_image: this.formData.profile_image || undefined,
        });
        this.$emit('profile-updated');
      } catch (e) {
        this.error = e instanceof Error ? e.message : 'Failed to update profile';
      }
    },
  },
});
</script>