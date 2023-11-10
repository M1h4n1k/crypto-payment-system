<script setup lang="ts">
import { ref } from "vue";
import { Currency } from "../types.ts";

defineProps<{
  currency: Currency;
  amount: number;
}>();

const emit = defineEmits<{
  (e: "cancel"): void;
}>();

const address = ref("0x9C08f04E516165bFE5aDC6A2c5eBbC16EA79afDA");
const status = ref("Unpaid");
</script>

<template>
  <div class="flex h-full w-full flex-col items-center justify-center px-24">
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
          @click="() => emit('cancel')"
        />
      </div>
      <span class="text-xl font-semibold">
        {{ amount }} {{ currency["name"].toUpperCase() }}
      </span>
    </div>

    <div class="mt-2 w-full">
      <span class="block text-base font-semibold text-gray-400"> Address </span>
      <span
        type="text"
        class="block w-full border-b-2 border-[#00A9FF] py-1 font-semibold outline-none"
      >
        {{ address }}
      </span>
    </div>
    <div class="mt-4 w-full">
      <span class="block text-base font-semibold text-gray-400"> Status </span>
      <span type="text" class="block w-full font-semibold outline-none">
        {{ status }}
      </span>
    </div>

    <p class="mt-7 block text-sm font-semibold text-gray-400">
      You have to transfer the exact amount in one transaction. Multiple
      transactions are not supported
    </p>

    <div class="mt-3 grid h-12 w-full grid-cols-5 gap-4">
      <button
        class="col-span-2 flex items-center justify-center rounded-xl border-[3px] border-[#FF9B9B] text-2xl font-medium text-[#FF9B9B] hover:border-[#FF6B6B] hover:text-[#FF6B6B]"
        @click="() => $emit('cancel')"
      >
        Back
      </button>
      <!--      <button-->
      <!--        class="col-span-3 flex items-center justify-center rounded-xl bg-[#00A9FF] text-2xl font-medium text-white hover:bg-[#0098e6]"-->
      <!--        @click="() => $emit('proceed', email)"-->
      <!--      >-->
      <!--        QR-code-->
      <!--      </button>-->
    </div>
  </div>
</template>
