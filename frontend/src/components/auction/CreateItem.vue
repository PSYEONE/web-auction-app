<template>
  <div class="create-item">
    <form @submit.prevent="submitItem">
      <div style="margin-bottom: 12px;">
        <label style="display: block; margin-bottom: 4px;">
          <strong>Title:</strong>
        </label>
        <input
            v-model="formData.title"
            type="text"
            class="input-retro"
            placeholder="Enter item title"
            required
        />
      </div>

      <div style="margin-bottom: 12px;">
        <label style="display: block; margin-bottom: 4px;">
          <strong>Description:</strong>
        </label>
        <textarea
            v-model="formData.description"
            class="input-retro"
            placeholder="Describe your item..."
            rows="5"
            style="resize: vertical;"
            required
        ></textarea>
      </div>

      <div style="margin-bottom: 12px;">
        <label style="display: block; margin-bottom: 4px;">
          <strong>Starting Price:</strong>
        </label>
        <input
            v-model="formData.starting_price"
            type="number"
            step="0.01"
            min="0.01"
            class="input-retro"
            placeholder="0.00"
            required
        />
      </div>

      <div style="margin-bottom: 12px;">
        <label style="display: block; margin-bottom: 4px;">
          <strong>Auction End Date & Time:</strong>
        </label>
        <input
            v-model="formData.end_date"
            type="datetime-local"
            class="input-retro"
            required
        />
      </div>

      <div style="margin-bottom: 16px;">
        <label style="display: block; margin-bottom: 4px;">
          <strong>Item Image:</strong>
        </label>
        <input
            type="file"
            accept="image/*"
            @change="handleImageChange"
            class="input-retro"
            required
        />
        <div v-if="previewImage" style="margin-top: 12px; text-align: center;">
          <img
              :src="previewImage"
              alt="Preview"
              style="max-width: 300px; max-height: 300px; border: 2px solid var(--win-dark-gray);"
          />
        </div>
      </div>

      <button
          type="submit"
          class="btn-retro"
          :disabled="itemsStore.loading"
          style="width: 100%;"
      >
        {{ itemsStore.loading ? 'Creating...' : 'Create Auction' }}
      </button>

      <p v-if="error" style="color: red; margin-top: 12px;">
        {{ error }}
      </p>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useItemsStore } from '../../stores/items';

export default defineComponent({
  name: 'CreateItem',
  emits: ['item-created'],
  data() {
    return {
      itemsStore: useItemsStore(),
      formData: {
        title: '',
        description: '',
        starting_price: '',
        end_date: '',
        image: null as File | null,
      },
      previewImage: null as string | null,
      error: null as string | null,
    };
  },
  methods: {
    handleImageChange(event: Event): void {
      const target = event.target as HTMLInputElement;
      const file = target.files?.[0];
      if (file) {
        this.formData.image = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.previewImage = e.target?.result as string;
        };
        reader.readAsDataURL(file);
      }
    },
    async submitItem(): Promise<void> {
      this.error = null;

      if (!this.formData.image) {
        this.error = 'Please select an image';
        return;
      }

      try {
        const endDate = new Date(this.formData.end_date).toISOString();

        await this.itemsStore.createItem({
          title: this.formData.title,
          description: this.formData.description,
          starting_price: this.formData.starting_price,
          end_date: endDate,
          image: this.formData.image,
        });

        this.$emit('item-created');
      } catch (e) {
        this.error = e instanceof Error ? e.message : 'Failed to create item';
      }
    },
  },
});
</script>