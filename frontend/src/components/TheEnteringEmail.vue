<script setup lang="ts">
import { ref } from "vue";
import { Currency } from "../types.ts";

const props = defineProps<{
  currency: Currency;
  amount: number;
  email: string;
}>();

defineEmits<{
  (e: "cancel"): void;
  (e: "proceed", em: string): void;
}>();

const email = ref(props.email);
</script>

<template>
  <div class="flex flex-col items-center justify-center px-24 py-16">
    <div class="flex w-full items-center justify-between">
      <div class="relative mb-2 flex items-center space-x-2">
        <div
          class="h-12 w-12 rounded-full"
          :style="{
            'background-color': currency['color'],
          }"
        ></div>
        <img
          class="absolute -left-7 cursor-pointer"
          src="https://static-00.iconduck.com/assets.00/arrow-ios-back-icon-257x512-np6b911r.png"
          alt="back"
          height="10"
          width="15"
          @click="() => $emit('cancel')"
        />
      </div>
      <span class="text-xl font-semibold">
        {{ amount }} {{ currency["name"].toUpperCase() }}
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
