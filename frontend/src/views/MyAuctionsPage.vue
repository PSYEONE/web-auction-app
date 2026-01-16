<template>
  <div class="my-auctions">
    <div class="window">
      <div class="window-title">My Auctions ({{ myItems.length }})</div>
      <div class="window-body">
        <div v-if="itemsStore.loading" style="text-align: center; padding: 40px;">
          Loading...
        </div>
        <div v-else-if="itemsStore.error" style="color: red; padding: 20px;">
          Error: {{ itemsStore.error }}
        </div>
        <div v-else-if="myItems.length === 0" style="padding: 40px; text-align: center;">
          You haven't created any auctions yet
        </div>
        <div v-else class="items-grid">
          <ItemCard
              v-for="item in myItems"
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
import { useUserStore } from '../stores/user';
import ItemCard from '../components/auction/ItemCard.vue';
import type { Item } from '../types/models';

export default defineComponent({
  name: 'MyAuctionsPage',
  components: {
    ItemCard,
  },
  data() {
    return {
      itemsStore: useItemsStore(),
      userStore: useUserStore(),
    };
  },
  computed: {
    myItems(): Item[] {
      if (!this.userStore.profile) return [];
      return this.itemsStore.items.filter(
          item => item.owner.id === this.userStore.profile!.id
      );
    },
  },
  mounted() {
    this.itemsStore.fetchItems();
  },
  methods: {
    goToItem(id: number): void {
      this.$router.push(`/items/${id}`);
    },
  },
});
</script>