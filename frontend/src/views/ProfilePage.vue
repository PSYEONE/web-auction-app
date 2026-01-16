<template>
  <div class="profile-page">
    <div class="window">
      <div class="window-title">👤 Edit Profile</div>
      <div class="window-body">
        <div v-if="userStore.loading" style="text-align: center; padding: 40px;">
          Loading...
        </div>
        <div v-else-if="userStore.profile">
          <ProfileEditor :profile="userStore.profile" @profile-updated="handleUpdate" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from '../stores/user';
import ProfileEditor from '../components/profile/ProfileEditor.vue';

export default defineComponent({
  name: 'ProfilePage',
  components: {
    ProfileEditor,
  },
  data() {
    return {
      userStore: useUserStore(),
    };
  },
  methods: {
    handleUpdate(): void {
      // Profile already updated in store
      alert('Profile updated successfully! ✨');
    },
  },
});
</script>

<style scoped>
.profile-page {
  max-width: 600px;
}
</style>