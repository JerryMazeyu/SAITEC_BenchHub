import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 引入路由配置
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import * as Icons from '@element-plus/icons-vue';

const app = createApp(App);

app.use(ElementPlus); // 使用 ElementPlus
app.use(router); // 使用 Vue Router

// 全局注册所有图标组件
for (const [key, component] of Object.entries(Icons)) {
  app.component(key, component);
}

app.mount('#app'); // 挂载到 DOM