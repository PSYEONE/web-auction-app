<template>
  <div class="home">
    <div class="window" style="margin-bottom: 20px;">
      <div class="window-title">🔍 Search Auctions</div>
      <div class="window-body">
        <input
            v-model="searchQuery"
            @input="handleSearch"
            class="input-retro"
            type="text"
            placeholder="Search by title or description..."
        />
      </div>
    </div>

    <div class="window">
      <div class="window-title">🎯 Active Auctions ({{ itemsStore.items.length }})</div>
      <div class="window-body">
        <div v-if="itemsStore.loading" style="text-align: center; padding: 40px;">
          Loading...
        </div>
        <div v-else-if="itemsStore.error" style="color: red; padding: 20px;">
          Error: {{ itemsStore.error }}
        </div>
        <div v-else-if="itemsStore.items.length === 0" style="padding: 40px; text-align: center;">
          No auctions found 😔
        </div>
        <div v-else class="items-grid">
          <ItemCard
              v-for="item in itemsStore.items"
              :key="item.id"
              :item="item"
              @click="goToItem(item.id)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useItemsStore } from '../stores/items';
import ItemCard from '../components/auction/ItemCard.vue';

export default defineComponent({
  name: 'Home',
  components: {
    ItemCard,
  },
  data() {
    return {
      itemsStore: useItemsStore(),
      searchQuery: '',
      searchTimeout: undefined as number | undefined,
    };
  },
  mounted() {
    this.itemsStore.fetchItems();
  },
  methods: {
    handleSearch(): void {
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }
      this.searchTimeout = window.setTimeout(() => {
        this.itemsStore.fetchItems(this.searchQuery || undefined);
      }, 300);
    },
    goToItem(id: number): void {
      this.$router.push(`/items/${id}`);
    },
  },
});
</script>

<style scoped>
.home {
  max-width: 1200px;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  padding: 8px;
}
</style>