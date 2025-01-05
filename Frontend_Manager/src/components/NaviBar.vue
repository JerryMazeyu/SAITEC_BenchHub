<template>
  <div class="navi-bar">
    <el-menu
      class="menu"
      active-text-color="#ffd04b"
      background-color="black"
      default-active="2"
      text-color="#fff"
      @select="handleSelect"
    >
      <el-menu-item index="/paper">
        <el-icon>
          <Document />
        </el-icon>
        <span>Paper Management</span>
      </el-menu-item>
      <el-menu-item index="/qa">
        <el-icon>
          <ChatDotRound />
        </el-icon>
        <span>QA Management</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script lang="ts" setup>
import { Document, ChatDotRound } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const handleSelect = (key: string) => {
  // 跳转到对应的路由路径
  router.push(key).catch((err) => {
    console.error("Navigation Error:", err);
  });
};
</script>

<style>
.navi-bar {
  height: 100%;
  width: 100%; /* 占满父组件 */
}

.menu {
  height: 100%;
}
</style>
