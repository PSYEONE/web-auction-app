<template>
  <div class="taskbar">
    <div class="taskbar-left">
      <button class="start-button btn-retro" @click="toggleUserMenu">
        <span v-if="userStore.profile">{{ userStore.profile.username }}</span>
        <span v-else>User</span>
      </button>

      <UserMenu
          v-if="showUserMenu"
          @close="showUserMenu = false"
          @go-to-profile="handleGoToProfile"
          @go-to-login="handleGoToLogin"
          @go-to-signup="handleGoToSignup"
          @logout="handleLogout"
      />
    </div>

    <div class="taskbar-center">
      <button class="taskbar-btn btn-retro" @click="$emit('go-to-home')">
        All Auctions
      </button>
      <button
          class="taskbar-btn btn-retro"
          @click="$emit('go-to-my-auctions')"
          :disabled="!userStore.profile"
      >
        My Auctions
      </button>
      <button
          class="taskbar-btn btn-retro"
          @click="$emit('go-to-create')"
          :disabled="!userStore.profile"
      >
        Create Auction
      </button>
    </div>

    <div class="taskbar-right">
      <span>{{ currentTime }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from '../../stores/user';
import UserMenu from './UserMenu.vue';

export default defineComponent({
  name: 'Taskbar',
  components: {
    UserMenu,
  },
  emits: ['go-to-home', 'go-to-my-auctions', 'go-to-create', 'go-to-profile', 'go-to-login', 'go-to-signup', 'logout'],
  data() {
    return {
      userStore: useUserStore(),
      currentTime: '',
      showUserMenu: false,
    };
  },
  mounted() {
    this.updateTime();
    setInterval(this.updateTime, 1000);
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
  },
  methods: {
    updateTime(): void {
      const now = new Date();
      this.currentTime = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    toggleUserMenu(): void {
      this.showUserMenu = !this.showUserMenu;
    },
    handleClickOutside(event: MouseEvent): void {
      const target = event.target as HTMLElement;
      if (!target.closest('.start-button') && !target.closest('.user-menu')) {
        this.showUserMenu = false;
      }
    },
    handleGoToProfile(): void {
      this.showUserMenu = false;
      this.$emit('go-to-profile');
    },
    handleGoToLogin(): void {
      this.showUserMenu = false;
      this.$emit('go-to-login');
    },
    handleGoToSignup(): void {
      this.showUserMenu = false;
      this.$emit('go-to-signup');
    },
    handleLogout(): void {
      this.showUserMenu = false;
      this.$emit('logout');
    },
  },
});
</script>