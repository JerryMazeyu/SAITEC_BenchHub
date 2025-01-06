<template>
  <div class="login-container">
    <el-card class="login-card" shadow="hover">
      <div class="title-logo">
        <div class="logo">
          <img class="logo1" src="../assets/logo.png" alt="">
          <img class="logo2" src="../assets/logo-2.png" alt="">
        </div>
        <div class="title">
          <h1><el-icon>
              <Tools />
            </el-icon>Admin Dashboard</h1>
        </div>
      </div>

      <el-form :size="large" :model="loginForm" :rules="rules" ref="loginFormRef" label-width="100px">
        <!-- 用户名输入框 -->
        <el-form-item label-position="top" label="UserName" prop="username">
          <!-- <div class="form-item-lable">Username</div> -->
          <el-input v-model="loginForm.username" placeholder="Enter your username"></el-input>
        </el-form-item>

        <!-- 密码输入框 -->
        <el-form-item label-position="top" label="PassWord" prop="password">
          <!-- <div class="form-item-lable">Password</div> -->
          <el-input v-model="loginForm.password" type="password" placeholder="Enter your password"></el-input>
        </el-form-item>

        <!-- 登录按钮 -->
        <el-form-item label-position="top">
          <el-button type="primary" @click="onSubmit">Sign In</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { reactive, ref } from 'vue';
// import { ElMessage } from 'element-plus';
import { ElNotification } from 'element-plus'
import { login } from '../api/login';
import { useRouter } from 'vue-router';

export default {
  name: "LoginPage",
  setup() {

    const router = useRouter()
    const loginForm = reactive({
      username: "",
      password: "",
    });

    const rules = {
      username: [
        { required: true, message: "Please enter your username", trigger: "blur" },
      ],
      password: [
        { required: true, message: "Please enter your password", trigger: "blur" },
      ],
    };

    const loginFormRef = ref(null);

    const onSubmit = () => {
      loginFormRef.value.validate((valid) => {
        if (valid) {
          const loginData = { username: loginForm.username, password: loginForm.password }
          login(loginData).then(res => {
            if (res.success) {
              localStorage.setItem('username', res.username)
              localStorage.setItem('token', res.token)
              router.push("/")
              ElNotification({
                title: 'Success',
                message: 'Login successful with username: ${loginForm.username}.',
                type: 'success',
              })
            }
            else {
              ElNotification({
                title: 'Error',
                message: 'Validation failed, please check your username and password.',
                type: 'error',
              })
            }
          })
        } else {
          ElNotification({
                title: 'Error',
                message: 'Validation failed.',
                type: 'error',
              })
          return false;
        }
      });
    };

    return {
      loginForm,
      rules,
      loginFormRef,
      onSubmit,
    };
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  background-color: black;
  width: 700px;
  padding: 20px;
  box-shadow: 0px 2px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  display: flex;
  justify-content: left;
}

.title-logo {
  display: flex;
  justify-content: left;
}

.logo {
  height: 70px;
  background-color: black;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
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

.title {
  background: black;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70px;
  margin-left: 30px;
  color: white;
}

.form-item-lable {
  color: white;
}
</style>
