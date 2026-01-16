<template>
  <div class="item-card window" @click="$emit('click')">
    <div class="window-title">{{ item.title }}</div>
    <div class="window-body">
      <img
          :src="`/media/${item.image}`"
          :alt="item.title"
          class="item-image"
      />
      <div class="item-info">
        <p class="item-price">
          💰 Current: ${{ item.highest_bid || item.starting_price }}
        </p>
        <p class="item-bids">📊 {{ item.bids.length }} bid(s)</p>
        <p class="item-time">⏰ Ends: {{ formatDate(item.end_date) }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import type { Item } from '../../types/models';

export default defineComponent({
  name: 'ItemCard',
  props: {
    item: {
      type: Object as PropType<Item>,
      required: true,
    },
  },
  emits: ['click'],
  methods: {
    formatDate(dateString: string): string {
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
  },
});
</script>

<style scoped>
.item-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.item-card:hover {
  transform: translateY(-4px);
  box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.4);
}

.item-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border: 2px solid var(--win-dark-gray);
  margin-bottom: 12px;
  image-rendering: auto;
}

.item-info {
  font-size: 13px;
}

.item-info p {
  margin: 4px 0;
}

.item-price {
  font-weight: bold;
  color: var(--win-blue);
  font-size: 14px;
}
</style>