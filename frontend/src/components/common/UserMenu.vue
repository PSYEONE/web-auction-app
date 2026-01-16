<template>
  <div class="user-menu window">
    <div v-if="userStore.profile" class="user-menu-content">
      <div class="user-info">
        <img
            v-if="userStore.profile.profile_image"
            :src="userStore.profile.profile_image"
            alt="Profile"
            class="menu-profile-img"
        />
        <div v-else class="menu-profile-placeholder">
          NO IMAGE
        </div>
        <div class="user-details">
          <strong>{{ userStore.profile.username }}</strong>
          <span style="font-size: 11px; color: var(--win-dark-gray);">
            {{ userStore.profile.email }}
          </span>
        </div>
      </div>
      <div class="menu-divider"></div>
      <button class="menu-item btn-retro" @click="$emit('go-to-profile')">
        Edit Profile
      </button>
      <button class="menu-item btn-retro" @click="$emit('logout')">
        Logout
      </button>
    </div>

    <div v-else class="user-menu-content">
      <div class="user-info">
        <div class="menu-profile-placeholder">
          GUEST
        </div>
        <div class="user-details">
          <strong>Not logged in</strong>
        </div>
      </div>
      <div class="menu-divider"></div>
      <button class="menu-item btn-retro" @click="$emit('go-to-login')">
        Login
      </button>
      <button class="menu-item btn-retro" @click="$emit('go-to-signup')">
        Sign Up
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from '../../stores/user';

export default defineComponent({
  name: 'UserMenu',
  emits: ['close', 'go-to-profile', 'go-to-login', 'go-to-signup', 'logout'],
  data() {
    return {
      userStore: useUserStore(),
    };
  },
});
</script>