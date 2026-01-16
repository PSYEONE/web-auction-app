<template>
  <div class="create-page">
    <div class="window">
      <div class="window-title">➕ Create New Auction</div>
      <div class="window-body">
        <CreateItem @item-created="handleCreated" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import CreateItem from '../components/auction/CreateItem.vue';

export default defineComponent({
  name: 'CreateItemPage',
  components: {
    CreateItem,
  },
  methods: {
    handleCreated(): void {
      alert('Auction created successfully! 🎉');
      this.$router.push('/');
    },
  },
});
</script>

<style scoped>
.create-page {
  max-width: 600px;
}
</style>