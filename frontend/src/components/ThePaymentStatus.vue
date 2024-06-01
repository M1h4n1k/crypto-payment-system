<script setup lang="ts">
import { Currency, Order } from "../types.ts";

const props = defineProps<{
  chosenCurrency: Currency;
  order: Order;
}>();

const emit = defineEmits<{
  (e: "cancel"): void;
}>();

let intervalId: ReturnType<typeof setInterval>;

const refreshOrder = async () => {
  fetch(`${import.meta.env.VITE_API_URL}/order/${props.order._id}`)
    .then((response) => response.json())
    .then((data: Order) => {
      props.order.status = data.status;
      if (data.status === 1) clearInterval(intervalId);
    });
};

if (props.order.status === 0) {
  intervalId = setInterval(refreshOrder, 5000);
}
</script>

<template>
  <div
    class="flex h-full w-full flex-col items-center justify-center px-12 sm:px-24"
  >
    <div class="flex w-full items-center justify-between">
      <div class="relative mb-2 flex items-center space-x-2">
        <img
          :src="chosenCurrency['link']"
          alt=""
          class="h-12 w-12 rounded-full"
          :style="{
            'background-color': chosenCurrency.color,
          }"
        />
        <img
          class="absolute -left-[36px] h-[30px] w-[17px] cursor-pointer dark:invert-[70%]"
          src="/backArrow.svg"
          alt="back"
          @click="emit('cancel')"
        />
      </div>
      <span class="text-xl font-semibold dark:text-gray-100">
        {{ order["amountCrypto"] }} {{ chosenCurrency["name"].toUpperCase() }}
      </span>
    </div>

    <div class="mt-2 w-full">
      <span class="block text-base font-semibold text-gray-400"> Address </span>
      <span
        type="text"
        class="block w-full break-words border-b-2 border-[#00A9FF] py-1 font-semibold outline-none dark:border-[#004fd6] dark:text-gray-100"
      >
        {{ order["address"] }}
      </span>
    </div>
    <div class="mt-4 w-full">
      <span class="block text-base font-semibold text-gray-400"> Status </span>
      <span
        type="text"
        class="block w-full font-semibold outline-none"
        :style="{
          color: order['status'] === 0 ? '#FF9B9B' : '#32cb00',
        }"
      >
        {{ order["status"] === 0 ? "Waiting for payment" : "Payment received" }}
      </span>
    </div>

    <p class="mt-2 block text-sm font-semibold text-gray-400 sm:mt-7">
      You have to transfer the exact amount in one transaction. Multiple
      transactions are not supported
    </p>

    <div class="mt-3 grid h-12 w-full grid-cols-5 gap-4">
      <button
        class="col-span-2 flex items-center justify-center rounded-xl border-[3px] border-[#FF9B9B] text-2xl font-medium text-[#FF9B9B] transition-colors duration-200 hover:border-[#FF6B6B] hover:text-[#FF6B6B]"
        @click="emit('cancel')"
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
