<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-window window" @click.stop>
      <div class="window-title error-title">
        Error
      </div>
      <div class="window-body">
        <div class="error-content">
          <div class="error-icon">X</div>
          <div class="error-text">{{ message }}</div>
        </div>
        <button class="btn-retro" @click="$emit('close')" style="margin-top: 16px;">
          OK
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ErrorModal',
  props: {
    message: {
      type: String,
      required: true,
    },
  },
  emits: ['close'],
});
</script>