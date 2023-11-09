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
    <span>Evicon &bull; {{ amount }} {{ currency }}</span>
    <span>Support</span>
  </div>
</template>
