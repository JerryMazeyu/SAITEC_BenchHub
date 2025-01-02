<template>
    <div class="common-layout">
      <el-container class="layout-container">
        <el-aside class="asider">
          <div class="logo">
            <img class="logo1" src="../assets/logo.png" alt="">
            <img class="logo2" src="../assets/logo-2.png" alt="">
          </div>
          <div class="naviBar">
            <NaviBar />
          </div>
          <div class="login-out">
            <el-button class="login-out-button" size="large" type="warning" plain>Login Out</el-button>
          </div>
        </el-aside>
  
        <el-main class="content-container">
            <router-view />
        </el-main>
  
      </el-container>
    </div>
  </template>
  
  <script>
  import NaviBar from './NaviBar.vue'
  export default {
    name: "Layout",
    components: {
      NaviBar,
    }
  };
  </script>
  
  <style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    overflow: hidden;
  }
  
  
  .common-layout {
    margin: 0;
    padding: 0;
    height: 100vh;
  }
  
  /* 整体容器 */
  .layout-container {
    height: auto;
    /* 占满整个视口高度 */
  }
  
  .logo {
    display: flex;
    padding-left: 20px;
    align-items: center;
    height: 20vh;
    background-color: black;
  }
  
  .logo1 {
    height: 60px;
    width: 60px;
    margin: 5px;
  }
  
  .logo2{
    height: 30px;
    width: 120px;
  }
  
  .naviBar {
    background-color: black;
    height: 70vh;
  }
  
  .login-out{
    height: 10vh;
    background-color: black;
  }
  
  .login-out-button {
    width: 90%;
  }
  
  /* 主容器 */
  .main-container {
    height: 100vh;
  }
  
  /* Aside 样式 */
  .asider {
    width: 200px;
    /* 固定宽度 */
    text-align: center;
    /* 水平居中 */
    height: 100vh;
  }
  
  /* Content 容器 */
  .content-container {
    flex: 1;
    /* 占据剩余空间 */
    text-align: center;
    /* 水平居中 */
    height: 100%
  }
  </style>
  