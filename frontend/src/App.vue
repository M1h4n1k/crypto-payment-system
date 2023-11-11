<script setup lang="ts">
import MainPage from "./components/MainPage.vue";

if (localStorage.getItem("color-theme") === "dark") {
  document.documentElement.classList.add("dark");
}
</script>

<template>
  <div
    class="flex h-[100vh] w-full items-center justify-center bg-gray-50 transition-colors duration-75 dark:bg-gray-900"
  >
    <MainPage />
  </div>
</template>

<style scoped></style>
