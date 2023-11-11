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
  fetch(`http://127.0.0.1:8000/order/${oid}`)
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
  let response = await fetch(`http://127.0.0.1:8000/order/${oid}`, {
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
</script>

<template>
  <div
    class="flex h-[440px] w-11/12 min-w-[300px] max-w-[650px] flex-col overflow-hidden rounded-3xl bg-white shadow-xl duration-75 dark:bg-gray-700"
  >
    <TheHeader :order="order" />

    <TheSkeleton v-if="order.stage === -1" />
    <TheChoosingCurrency
      v-else-if="order.stage === 0"
      @methodChosen="
        (m: string) => {
          chosenCurrency = new Currency(
            m,
            CRYPTO_CURRENCIES[m as keyof CryptoCurrencyType]['color'],
            CRYPTO_CURRENCIES[m as keyof CryptoCurrencyType]['link'],
          );
          order.stage = 1;
        }
      "
    />
    <TheEnteringEmail
      v-else-if="order.stage === 1"
      @cancel="
        () => {
          chosenCurrency = new Currency();
          order.stage = 0;
        }
      "
      @proceed="
        (e: string) => {
          order.email = e;
          order.stage = 2;
        }
      "
      :chosenCurrency="chosenCurrency"
      :order="order"
    />
    <ThePaymentStatus
      v-else-if="order.stage === 2"
      :chosenCurrency="chosenCurrency"
      @cancel="() => (order.stage = 1)"
      :order="order"
    />
  </div>
</template>
