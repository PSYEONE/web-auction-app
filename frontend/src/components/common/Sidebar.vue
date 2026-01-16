<template>
  <aside class="sidebar">
    <div class="window" style="margin-bottom: 16px;">
      <div class="window-title">User Info</div>
      <div class="window-body">
        <!-- Logged IN -->
        <div v-if="userStore.profile">
          <img
              v-if="userStore.profile.profile_image"
              :src="userStore.profile.profile_image"
              alt="Profile"
              class="profile-img"
          />
          <div v-else class="profile-img-placeholder">
            NO IMAGE
          </div>
          <p style="font-weight: bold; margin-top: 8px;">{{ userStore.profile.username }}</p>
          <button class="btn-retro" style="margin-top: 8px; width: 100%;" @click="$emit('go-to-profile')">
            Edit Profile
          </button>
          <button class="btn-retro" style="margin-top: 8px; width: 100%;" @click="$emit('logout')">
            Logout
          </button>
        </div>

        <!-- Logged OUT -->
        <div v-else>
          <div class="profile-img-placeholder">
            GUEST
          </div>
          <p style="margin-top: 8px; color: var(--win-dark-gray);">Not logged in</p>
          <button class="btn-retro" style="margin-top: 8px; width: 100%;" @click="$emit('go-to-login')">
            Login
          </button>
          <button class="btn-retro" style="margin-top: 8px; width: 100%;" @click="$emit('go-to-signup')">
            Sign Up
          </button>
        </div>
      </div>
    </div>

    <div class="window">
      <div class="window-title">Menu</div>
      <div class="window-body">
        <button class="btn-retro" style="width: 100%; margin-bottom: 8px;" @click="$emit('go-to-home')">
          All Auctions
        </button>
        <button
            class="btn-retro"
            style="width: 100%; margin-bottom: 8px;"
            @click="$emit('go-to-my-auctions')"
            :disabled="!userStore.profile"
        >
          My Auctions
        </button>
        <button
            class="btn-retro"
            style="width: 100%;"
            @click="$emit('go-to-create')"
            :disabled="!userStore.profile"
        >
          Create Auction
        </button>
      </div>
    </div>

    <div class="window" style="margin-top: 16px;">
      <div class="window-title">Time</div>
      <div class="window-body" style="text-align: center; font-size: 12px;">
        {{ currentTime }}
      </div>
    </div>
  </aside>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from '../../stores/user';

export default defineComponent({
  name: 'Sidebar',
  emits: ['go-to-home', 'go-to-my-auctions', 'go-to-profile', 'go-to-create', 'go-to-login', 'go-to-signup', 'logout'],
  data() {
    return {
      userStore: useUserStore(),
      currentTime: '',
    };
  },
  mounted() {
    this.updateTime();
    setInterval(this.updateTime, 1000);
  },
  methods: {
    updateTime(): void {
      const now = new Date();
      this.currentTime = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
  },
});
</script>