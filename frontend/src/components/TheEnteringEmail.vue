<script setup lang="ts">
import { ref } from "vue";
import { Currency, Order } from "../types.ts";

const props = defineProps<{
  chosenCurrency: Currency;
  order: Order;
}>();

const emit = defineEmits<{
  (e: "cancel"): void;
  (e: "proceed", em: string): void;
}>();

const validateEmail = (email: string) => {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    );
};

const email = ref(props.order.email);
const emailError = ref(false);

const passEmail = () => {
  if (!validateEmail(email.value)) {
    emailError.value = true;
    return;
  }
  emit("proceed", email.value);
};
</script>

<template>
  <div class="flex h-full flex-col items-center justify-center px-24">
    <div class="flex w-full items-center justify-between">
      <div class="relative mb-2 flex items-center space-x-2">
        <img
          :src="chosenCurrency['link']"
          alt=""
          class="h-12 w-12 rounded-full"
          :style="{
            'background-color': chosenCurrency['color'],
          }"
        />
        <img
          class="absolute -left-[36px] h-[30px] w-[17px] cursor-pointer dark:invert-[70%]"
          src="/backArrow.svg"
          alt="back"
          height="30"
          width="17"
          @click="() => $emit('cancel')"
        />
      </div>
      <span
        v-if="order.amountCrypto === -1"
        class="h-8 w-1/3 animate-pulse rounded-xl bg-gray-100"
      />
      <span v-else class="text-xl font-semibold dark:text-gray-100">
        {{ order.amountCrypto }} {{ chosenCurrency["name"].toUpperCase() }}
      </span>
    </div>

    <input
      placeholder="Email address"
      type="email"
      class="mt-8 w-full border-b-2 border-gray-200 bg-transparent py-1 outline-none transition-colors duration-200 focus:border-[#00A9FF] dark:border-gray-600 dark:text-gray-100 dark:focus:border-[#004fd6]"
      :style="{
        'border-color': emailError ? '#FF9B9B' : '',
      }"
      v-model="email"
      @input="emailError = false"
      @keyup.enter="passEmail"
    />

    <div class="mt-8 grid h-12 w-full grid-cols-5 gap-4">
      <button
        class="col-span-2 flex items-center justify-center rounded-xl border-[3px] border-[#FF9B9B] text-2xl font-medium text-[#FF9B9B] transition-colors duration-200 hover:border-[#FF6B6B] hover:text-[#FF6B6B]"
        @click="() => $emit('cancel')"
      >
        Back
      </button>
      <button
        class="col-span-3 flex items-center justify-center rounded-xl bg-[#00A9FF] text-2xl font-medium text-white transition-colors duration-200 hover:bg-[#0098e6] dark:bg-[#004fd6] dark:hover:bg-[#0040b2]"
        @click="passEmail"
      >
        Pay
      </button>
    </div>
  </div>
</template>
