<template>
  <div class="loading-overlay">
    <div class="loading-window window">
      <div class="window-title">
        Please Wait...
      </div>
      <div class="window-body">
        <div class="progress-container">
          <div class="progress-bar">
            <div class="progress-fill"></div>
          </div>
          <p style="margin-top: 12px; text-align: center;">Loading...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'LoadingBar',
});
</script>