<script setup lang="ts">
import TheHeader from "./TheHeader.vue";
import TheChoosingCurrency from "./TheChoosingCurrency.vue";
import TheEnteringEmail from "./TheEnteringEmail.vue";
import ThePaymentStatus from "./ThePaymentStatus.vue";
import TheSkeleton from "./TheSkeleton.vue";

import { nextTick, onMounted, ref, watch } from "vue";
import { CRYPTO_CURRENCIES } from "../currencies";
import { Currency, Order } from "../types.ts";

const email = ref("");
const amount = ref(1000);
const amountCrypto = ref(0);
const currency = ref("EUR");
const chosenCurrency = ref(new Currency());
let dataLoaded = false;

const stage = ref(-1);

let oid = new URL(location.href).searchParams.get("oid");

onMounted(() => {
  fetch(`http://127.0.0.1:8000/order/${oid}`)
    .then((response) => response.json())
    .then((data) => {
      if (data["currencyCrypto"] !== "") {
        chosenCurrency.value.name = data["currencyCrypto"];
        chosenCurrency.value.color =
          CRYPTO_CURRENCIES[data["currencyCrypto"]]["color"];
      }
      email.value = data["email"];
      amount.value = data["amountEUR"];
      amountCrypto.value = data["amountCrypto"];
      currency.value = data["currency"];
      stage.value = data["stage"];
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
    const orderUpd = await updateOrder({
      currencyCrypto: newCurrency,
    });
    amountCrypto.value = orderUpd["amountCrypto"];
  },
);

watch(email, (newEmail) => {
  if (!dataLoaded) return;
  updateOrder({
    email: newEmail,
  });
});

watch(stage, (newStage) => {
  if (!dataLoaded) return;
  updateOrder({
    stage: newStage,
  });
});
</script>

<template>
  <div class="h-[440px] w-1/2 min-w-[300px] max-w-[650px] rounded-3xl bg-white">
    <TheHeader :amount="amount" :currency="currency" />

    <TheSkeleton v-if="stage === -1" />
    <TheChoosingCurrency
      v-else-if="stage === 0"
      @methodChosen="
        (m: string) => {
          chosenCurrency = new Currency(m, CRYPTO_CURRENCIES[m]['color']);
          stage = 1;
        }
      "
    />
    <TheEnteringEmail
      v-else-if="stage === 1"
      @cancel="
        () => {
          chosenCurrency = new Currency();
          stage = 0;
        }
      "
      @proceed="
        (e: string) => {
          email = e;
          stage = 2;
        }
      "
      :amount="amountCrypto"
      :currency="chosenCurrency"
      :email="email"
    />
    <ThePaymentStatus
      v-else-if="stage === 2"
      :amount="amountCrypto"
      :currency="chosenCurrency"
      @cancel="() => (stage = 1)"
    />
  </div>
</template>
