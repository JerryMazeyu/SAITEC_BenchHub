<template>
  <n-config-provider :theme="darkTheme">
    <n-message-provider>
      <div id="app">
        <Navbar />
        <router-view />
      </div>
    </n-message-provider>
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
  background: linear-gradient(135deg,
      /* 渐变效果 */
      black 0%,
      #2e9475 -20%,
      black 55%,
      #109dfa 150%,
      black 100%);
}

#app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  overflow: auto;
  /* 自动出现滚动条 */
}
</style>
