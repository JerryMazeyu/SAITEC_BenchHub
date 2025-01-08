<template>
    <div class="main-container">
        <div class="title">
            <h1>Welcome to SAITEC dashboard!{{ username }}</h1>
        </div>
        <div class="update-button">
            <el-button size="large" type="success">
                <el-icon>
                    <Refresh />
                </el-icon>
                Sync Data
            </el-button>
        </div>
    </div>
</template>

<script>
import { onMounted, ref } from 'vue';
export default {
    name: "Home",
    setup() {
        const username = ref('')

        onMounted(() => {
            if (!localStorage.getItem("username")) {
                username.value = localStorage.getItem("username")
            }
            else {
                username.value = ''
            }
        })
        return {
            username
        }
    }
}
</script>

<style>
/* 确保整个页面不显示滚动条 */
html,
body {
    overflow: hidden;
    /* 禁止滚动 */
    margin: 0;
    /* 去掉默认外边距 */
    padding: 0;
    /* 去掉默认内边距 */
}

/* 主容器样式 */
.main-container {
    overflow: hidden;
    /* 确保容器本身没有滚动条 */
    width: 100vw;
    /* 适配视口宽度 */
    height: 100vh;
    /* 适配视口高度 */
    display: flex;
    flex-direction: column;
    /* 垂直排列子元素 */
    justify-content: center;
    /* 垂直居中 */
    align-items: center;
    /* 水平居中 */
}

/* 标题样式 */
.title h1 {
    margin: 0;
    /* 去掉默认外边距 */
    font-size: 2rem;
    text-align: center;
}

/* 按钮样式 */
.update-button {
    margin-top: 20px;
    /* 增加按钮与标题之间的间距 */
}
</style>
