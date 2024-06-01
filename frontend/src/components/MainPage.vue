<script setup lang="ts">
import TheHeader from "./TheHeader.vue";
import TheChoosingCurrency from "./TheChoosingCurrency.vue";
import TheEnteringEmail from "./TheEnteringEmail.vue";
import ThePaymentStatus from "./ThePaymentStatus.vue";
import TheSkeleton from "./TheSkeleton.vue";

import { nextTick, onMounted, ref, watch } from "vue";
import { CRYPTO_CURRENCIES } from "../currencies";
import { CryptoCurrencyType, Currency, Order } from "../types.ts";

const chosenCurrency = ref(new Currency());
let order = ref(new Order());
let dataLoaded = false;

let oid = new URL(location.href).searchParams.get("oid");

onMounted(() => {
  fetch(`${import.meta.env.VITE_API_URL}/order/${oid}`)
    .then((response) => response.json())
    .then((data: Order) => {
      order.value = data;
      if (data.currencyCrypto !== "") {
        chosenCurrency.value.name = data.currencyCrypto;
        chosenCurrency.value.color =
          CRYPTO_CURRENCIES[data.currencyCrypto as keyof CryptoCurrencyType][
            "color"
          ];
        chosenCurrency.value.link =
          CRYPTO_CURRENCIES[data.currencyCrypto as keyof CryptoCurrencyType][
            "link"
          ];
      }
      nextTick(() => {
        dataLoaded = true;
      });
    });
});

const updateOrder = async (body: {}): Promise<Order> => {
  let response = await fetch(`${import.meta.env.VITE_API_URL}/order/${oid}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return await response.json();
};

watch(
  () => chosenCurrency.value.name,
  async (newCurrency) => {
    if (!dataLoaded) return;
    order.value.amountCrypto = -1;
    const orderUpd = await updateOrder({
      currencyCrypto: newCurrency,
    });
    order.value.amountCrypto = orderUpd["amountCrypto"];
    order.value.address = orderUpd["address"];
  },
);

watch(
  () => order.value.email,
  async (newEmail) => {
    if (!dataLoaded) return;
    await updateOrder({
      email: newEmail,
    });
  },
);

watch(
  () => order.value.stage,
  (newStage) => {
    if (!dataLoaded) return;
    updateOrder({
      stage: newStage,
    });
  },
);

const chooseCurrency = (m: string) => {
  chosenCurrency.value = new Currency(
    m,
    CRYPTO_CURRENCIES[m as keyof CryptoCurrencyType]["color"],
    CRYPTO_CURRENCIES[m as keyof CryptoCurrencyType]["link"],
  );
  order.value.stage = 1;
};

const cancelEmail = () => {
  chosenCurrency.value = new Currency();
  order.value.stage = 0;
};

const proceedEmail = (email: string) => {
  order.value.email = email;
  order.value.stage = 2;
};

const cancelPayment = () => {
  order.value.stage = 1;
};
</script>

<template>
  <div
    class="flex h-[440px] w-11/12 min-w-[300px] max-w-[650px] flex-col overflow-hidden rounded-3xl bg-white shadow-xl duration-75 dark:bg-gray-700"
  >
    <TheHeader :order="order" />

    <TheSkeleton v-if="order.stage === -1" />
    <TheChoosingCurrency
      v-else-if="order.stage === 0"
      @methodChosen="chooseCurrency"
    />
    <TheEnteringEmail
      v-else-if="order.stage === 1"
      @cancel="cancelEmail"
      @proceed="proceedEmail"
      :chosenCurrency="chosenCurrency"
      :order="order"
    />
    <ThePaymentStatus
      v-else-if="order.stage === 2"
      :chosenCurrency="chosenCurrency"
      @cancel="cancelPayment"
      :order="order"
    />
  </div>
</template>
