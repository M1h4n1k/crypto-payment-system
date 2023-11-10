<script setup lang="ts">
import { CRYPTO_CURRENCIES } from "../currencies.ts";

defineEmits<{
  (e: "methodChosen", currency: string): void;
}>();
</script>

<template>
  <div class="-mt-12 flex h-full w-full items-center justify-center px-20">
    <div>
      <span class="text-base font-semibold text-gray-400">
        Crypto currencies
      </span>
      <div class="mt-5 flex w-full flex-wrap items-center justify-start gap-8">
        <div
          v-for="(bg, currency) in CRYPTO_CURRENCIES"
          @click="() => $emit('methodChosen', currency)"
          class="currency hover:brightness-75"
          :style="{
            'background-color': bg.color,
          }"
        ></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.currency {
  height: 6rem;
  width: 6rem;
  cursor: pointer;
  border-radius: 50%;
}
</style>
