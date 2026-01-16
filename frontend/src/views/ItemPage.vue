<template>
  <div class="item-page">
    <div v-if="itemsStore.loading" style="text-align: center; padding: 40px;">
      Loading...
    </div>
    <div v-else-if="itemsStore.error" class="window">
      <div class="window-title">❌ Error</div>
      <div class="window-body" style="color: red;">
        {{ itemsStore.error }}
      </div>
    </div>
    <div v-else-if="item">
      <!-- Main Item Info -->
      <div class="window" style="margin-bottom: 20px;">
        <div class="window-title">{{ item.title }}</div>
        <div class="window-body">
          <div class="item-layout">
            <img :src="item.image" :alt="item.title" class="item-image" />
            <div class="item-details">
              <p><strong>Owner:</strong> {{ item.owner.username }}</p>
              <p><strong>Description:</strong></p>
              <p style="margin-top: 8px;">{{ item.description }}</p>
              <p style="margin-top: 16px;"><strong>Starting Price:</strong> ${{ item.starting_price }}</p>
              <p><strong>Current Bid:</strong> ${{ item.highest_bid || item.starting_price }}</p>
              <p><strong>Total Bids:</strong> {{ item.bids.length }}</p>
              <p><strong>Ends:</strong> {{ formatDate(item.end_date) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Bid Section -->
      <div class="window" style="margin-bottom: 20px;">
        <div class="window-title">💰 Place Bid</div>
        <div class="window-body">
          <BidSection :item="item" @bid-placed="refreshItem" />
        </div>
      </div>

      <!-- Bid History -->
      <div class="window" style="margin-bottom: 20px;">
        <div class="window-title">📊 Bid History</div>
        <div class="window-body">
          <div v-if="item.bids.length === 0" style="padding: 20px; text-align: center;">
            No bids yet!
          </div>
          <div v-else>
            <div
                v-for="bid in sortedBids"
                :key="bid.id"
                style="padding: 8px; border-bottom: 1px solid var(--win-dark-gray);"
            >
              <strong>{{ bid.bidder.username }}</strong> bid ${{ bid.amount }}
              <span style="float: right; color: var(--win-dark-gray);">
                {{ formatDate(bid.timestamp) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Q&A Section -->
      <div class="window">
        <div class="window-title">💬 Questions & Answers</div>
        <div class="window-body">
          <QuestionAnswer
              :item="item"
              :current-user-id="userStore.profile?.id"
              @question-posted="refreshItem"
              @reply-posted="refreshItem"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { Item, Bid } from '../types/models';
import { useItemsStore } from '../stores/items';
import { useUserStore } from '../stores/user';
import BidSection from '../components/auction/BidSection.vue';
import QuestionAnswer from '../components/qa/QuestionAnswer.vue';

export default defineComponent({
  name: 'ItemPage',
  components: {
    BidSection,
    QuestionAnswer,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      itemsStore: useItemsStore(),
      userStore: useUserStore(),
    };
  },
  computed: {
    item(): Item | null {
      return this.itemsStore.currentItem;
    },
    sortedBids(): Bid[] {
      if (!this.item) return [];
      return [...this.item.bids].sort((a, b) =>
          new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
      );
    },
  },
  mounted() {
    this.itemsStore.fetchItem(parseInt(this.id));
  },
  methods: {
    formatDate(dateString: string): string {
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    refreshItem(): void {
      this.itemsStore.fetchItem(parseInt(this.id));
    },
  },
});
</script>

<style scoped>
.item-page {
  max-width: 900px;
}

.item-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.item-image {
  width: 100%;
  height: auto;
  border: 2px solid var(--win-dark-gray);
}

.item-details p {
  margin: 8px 0;
}

@media (max-width: 768px) {
  .item-layout {
    grid-template-columns: 1fr;
  }
}
</style>