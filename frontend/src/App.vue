<template>
  <div class="app-container">
    <Sidebar
        @go-to-home="goToHome"
        @go-to-my-auctions="goToMyAuctions"
        @go-to-profile="goToProfile"
        @go-to-create="goToCreate"
        @go-to-login="goToLogin"
        @go-to-signup="goToSignup"
        @logout="handleLogout"
    />

    <main class="main-content">
      <router-view />
    </main>

    <ErrorModal
        v-if="showError"
        :message="errorMessage"
        @close="showError = false"
    />

    <LoadingBar v-if="isLoading" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from './stores/user';
import Sidebar from './components/common/Sidebar.vue';
import ErrorModal from './components/common/ErrorModal.vue';
import LoadingBar from './components/common/LoadingBar.vue';

export default defineComponent({
  name: 'App',
  components: {
    Sidebar,
    ErrorModal,
    LoadingBar,
  },
  data() {
    return {
      userStore: useUserStore(),
      showError: false,
      errorMessage: '',
    };
  },
  computed: {
    isLoading(): boolean {
      return this.userStore.loading;
    },
  },
  mounted() {
    this.userStore.fetchProfile().catch(() => {});
  },
  methods: {
    goToHome(): void {
      this.$router.push('/');
    },
    goToMyAuctions(): void {
      this.$router.push('/my-auctions');
    },
    goToProfile(): void {
      this.$router.push('/profile');
    },
    goToCreate(): void {
      this.$router.push('/create');
    },
    goToLogin(): void {
      window.location.href = '/login/';
    },
    goToSignup(): void {
      window.location.href = '/signup/';
    },
    handleLogout(): void {
      window.location.href = '/logout/';
    },
  },
});
</script>