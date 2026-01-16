<template>
  <div class="taskbar">
    <div class="taskbar-left">
      <span style="font-weight: bold;">Auction House</span>
    </div>
    <div class="taskbar-right">
      <span v-if="userStore.profile">{{ userStore.profile.username }}</span>
      <span v-else>Guest</span>
      <span style="margin-left: 16px;">{{ currentTime }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from '../../stores/user';

export default defineComponent({
  name: 'Taskbar',
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