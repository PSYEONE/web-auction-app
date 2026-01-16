<template>
  <div class="bid-section">
    <form @submit.prevent="submitBid">
      <div style="margin-bottom: 12px;">
        <label style="display: block; margin-bottom: 4px;">
          <strong>Your Bid Amount:</strong>
        </label>
        <input
            v-model="bidAmount"
            type="number"
            step="0.01"
            min="0"
            class="input-retro"
            placeholder="Enter bid amount"
            required
        />
      </div>

      <button
          type="submit"
          class="btn-retro"
          :disabled="itemsStore.loading"
          style="width: 100%;"
      >
        {{ itemsStore.loading ? 'Placing Bid...' : 'Place Bid' }}
      </button>

      <p v-if="error" style="color: red; margin-top: 12px;">
        {{ error }}
      </p>
      <p v-if="success" style="color: green; margin-top: 12px;">
        Bid placed successfully!
      </p>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import type { Item } from '../../types/models';
import { useItemsStore } from '../../stores/items';

export default defineComponent({
  name: 'BidSection',
  props: {
    item: {
      type: Object as PropType<Item>,
      required: true,
    },
  },
  emits: ['bid-placed'],
  data() {
    return {
      itemsStore: useItemsStore(),
      bidAmount: '',
      error: null as string | null,
      success: false,
    };
  },
  methods: {
    async submitBid(): Promise<void> {
      this.error = null;
      this.success = false;

      try {
        await this.itemsStore.placeBid(this.item.id, {
          amount: this.bidAmount,
        });
        this.success = true;
        this.bidAmount = '';
        this.$emit('bid-placed');
      } catch (e) {
        this.error = e instanceof Error ? e.message : 'Failed to place bid';
      }
    },
  },
});
</script>