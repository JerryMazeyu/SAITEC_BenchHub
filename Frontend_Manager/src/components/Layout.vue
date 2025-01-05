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
          <el-button round class="login-out-button" size="large" type="primary" plain @click="signOut">Sign Out</el-button>
        </div>
      </el-aside>

      <el-main class="content-container">
        <router-view />
      </el-main>

    </el-container>
  </div>
</template>

<script>
import NaviBar from './NaviBar.vue';
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { tokenCheck } from '../api/login';
// import { ElMessage } from 'element-plus';
import { ElNotification } from 'element-plus'
import { useRouter } from 'vue-router';

export default {
  name: "Layout",
  components: {
    NaviBar,
  },
  setup() {
    const router = useRouter();
    let timer = null;

    // Token 检测逻辑
    const checkToken = () => {
      const token = localStorage.getItem('token');
      if (token) {
        tokenCheck(token)
          .then(res => {
            if (!res.success) {
              ElNotification({
                title: 'Warning',
                message: 'Your token has expired, please sign in again.',
                type: 'warning',
              })
              router.push('/login');
            }
          })
          .catch(() => {
            ElNotification({
                title: 'Error',
                message: 'Failed to check token. Please try again.',
                type: 'error',
              })
          });
      } else {
        ElNotification({
                title: 'Warning',
                message: 'Login detected as not completed. Please sign in.',
                type: 'warning',
              })

        // router.push('/login');
      }
    };

    const signOut = () => {
      localStorage.removeItem('token')
      localStorage.removeItem('usernmae')
      router.push('/login')
      ElNotification({
                title: 'Info',
                message: 'You have logged out.',
                type: 'info',
              })
      
    }

    // 页面挂载时初始化
    onMounted(() => {
      checkToken(); // 立即执行一次
      timer = setInterval(checkToken, 5 * 60 * 1000); // 每五分钟检测一次
    });

    // 页面卸载时清除定时器
    onBeforeUnmount(() => {
      if (timer) clearInterval(timer);
    });

    return {
      signOut
    }
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
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

.logo2 {
  height: 30px;
  width: 120px;
}

.naviBar {
  background-color: black;
  height: 70vh;
  width: 100%;
}

.login-out {
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