<template>
  <n-config-provider :theme="darkTheme">
    <div id="app">
      <Navbar />
      <router-view />
    </div>
  </n-config-provider>
</template>

<script setup lang="ts">
import Navbar from "@/components/Navbar.vue";
import { darkTheme } from "naive-ui";
</script>

<style>
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.homepage {
  flex: 1; /* 占据剩余空间 */
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
}
</style>
