<template>
  <div class="navi-bar">
    <el-menu class="menu" active-text-color="#ffd04b" background-color="black" default-active="2" text-color="#fff"
      @open="handleOpen" @close="handleClose">
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
        <span>QA Managemnent</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>


<script lang="ts" setup>
import { Document } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';


  const router = useRouter()

  const handleOpen = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
    router.push(key)
  }
  const handleClose = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
  }

</script>

<style>
.navi-bar {
  height: 100%;
  /* 占满父组件 */
  width: 100%;
}

.menu {
  height: 100%;
}
</style>
