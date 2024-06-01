<script setup lang="ts">
import { CRYPTO_CURRENCIES } from "../currencies.ts";

const emit = defineEmits<{
  (e: "methodChosen", currency: string): void;
}>();
</script>

<template>
  <div class="flex h-full w-full items-center justify-center px-10">
    <div class="-mt-12">
      <span class="text-base font-semibold text-gray-400">
        Crypto currencies
      </span>
      <div class="mt-5 flex w-full flex-wrap items-center justify-center gap-8">
        <div
          v-for="(val, currency) in CRYPTO_CURRENCIES"
          @click="emit('methodChosen', currency)"
          class="currency flex items-center justify-center hover:brightness-75"
          :style="{
            'border-color': val.color,
          }"
        >
          <img
            :src="val.link"
            :alt="currency"
            class="h-full w-full rounded-full border border-white text-center leading-[5rem] transition-colors duration-75 dark:border-gray-700"
            :style="{
              'background-color': val.color,
            }"
          />
        </div>
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
  border: 3px solid;
}
</style>
