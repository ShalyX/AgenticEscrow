<template>
  <Suspense>
    <template #default>
      <EscrowScreen />
    </template>
    <template #fallback>
      <div class="flex items-center justify-center h-screen bg-[#030712]">
        <div class="spinner"></div>
      </div>
    </template>
  </Suspense>
</template>

<script setup>
import EscrowScreen from "./components/EscrowScreen.vue";
</script>
