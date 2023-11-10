<script setup lang="ts">
import { ref } from "vue";
import { Currency, Order } from "../types.ts";

const props = defineProps<{
  chosenCurrency: Currency;
  order: Order;
}>();

defineEmits<{
  (e: "cancel"): void;
  (e: "proceed", em: string): void;
}>();

const email = ref(props.order.email);
</script>

<template>
  <div class="flex h-full flex-col items-center justify-center px-24">
    <div class="flex w-full items-center justify-between">
      <div class="relative mb-2 flex items-center space-x-2">
        <div
          class="h-12 w-12 rounded-full"
          :style="{
            'background-color': chosenCurrency['color'],
          }"
        ></div>
        <img
          class="absolute -left-[36px] h-[30px] w-[17px] cursor-pointer"
          src="/backArrow.png"
          alt="back"
          height="202"
          width="118"
          @click="() => $emit('cancel')"
        />
      </div>
      <span
        v-if="order.amountCrypto === -1"
        class="h-8 w-1/3 animate-pulse rounded-xl bg-gray-100"
      />
      <span v-else class="text-xl font-semibold">
        {{ order.amountCrypto }} {{ chosenCurrency["name"].toUpperCase() }}
      </span>
    </div>

    <input
      placeholder="Email address"
      type="email"
      class="mt-8 w-full border-b-2 border-gray-200 py-1 outline-none transition-colors duration-200 focus:border-[#00A9FF]"
      v-model="email"
      @keyup.enter="() => $emit('proceed', email)"
    />

    <div class="mt-8 grid h-12 w-full grid-cols-5 gap-4">
      <button
        class="col-span-2 flex items-center justify-center rounded-xl border-[3px] border-[#FF9B9B] text-2xl font-medium text-[#FF9B9B] hover:border-[#FF6B6B] hover:text-[#FF6B6B]"
        @click="() => $emit('cancel')"
      >
        Back
      </button>
      <button
        class="col-span-3 flex items-center justify-center rounded-xl bg-[#00A9FF] text-2xl font-medium text-white hover:bg-[#0098e6]"
        @click="() => $emit('proceed', email)"
      >
        Pay
      </button>
    </div>
  </div>
</template>
