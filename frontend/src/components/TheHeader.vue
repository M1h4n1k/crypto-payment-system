<script setup lang="ts">
defineProps<{
  amount: number;
  currency: string;
}>();
</script>

<template>
  <div
    id="header"
    class="flex h-16 w-full items-center justify-between rounded-t-3xl bg-[#00A9FF] p-6 text-xl font-semibold text-white"
  >
    <div class="flex items-center justify-center">
      Evicon &bull;&nbsp;
      <span
        v-if="amount === -1"
        class="mt-1 h-5 w-12 animate-pulse rounded-xl bg-gray-100"
      />
      <span v-else>{{ amount }} {{ currency }}</span>
    </div>
    <span>Support</span>
  </div>
</template>
