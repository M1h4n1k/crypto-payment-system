<script setup lang="ts">
import { Order } from "../types.ts";

defineProps<{
  order: Order;
}>();

const toggleMode = () => {
  if (localStorage.getItem("color-theme") === "dark") {
    localStorage.setItem("color-theme", "light");
    document.documentElement.classList.remove("dark");
  } else {
    localStorage.setItem("color-theme", "dark");
    document.documentElement.classList.add("dark");
  }
};
</script>

<template>
  <div
    id="header"
    class="flex h-16 w-full items-center justify-between rounded-t-3xl bg-[#00A9FF] p-6 text-xl font-semibold text-white transition-colors duration-75 dark:bg-[#004fd6] dark:text-gray-100"
  >
    <div class="flex items-center justify-center">
      Evicon &bull;&nbsp;
      <span
        v-if="order.amountFiat === -1"
        class="mt-1 h-5 w-12 animate-pulse rounded-xl bg-gray-100"
      />
      <span v-else>{{ order.amountFiat }} {{ order.currency }}</span>
    </div>
    <div class="flex items-center justify-center space-x-3">
      <button
        id="theme-toggle"
        type="button"
        class="text-slate rounded-lg p-2.5 text-blue-900 transition-all hover:bg-[#1385ff] active:scale-75 dark:text-white dark:hover:bg-[#166afa]"
        @click="toggleMode"
      >
        <svg
          id="theme-toggle-dark-icon"
          class="h-5 w-5 dark:hidden"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"
          ></path>
        </svg>
        <svg
          id="theme-toggle-light-icon"
          class="hidden h-5 w-5 dark:block"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
          ></path>
        </svg>
      </button>
      <a href="https://t.me/M1h4n1k">Support</a>
    </div>
  </div>
</template>
