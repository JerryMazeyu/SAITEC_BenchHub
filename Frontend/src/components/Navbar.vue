<template>
  <header class="navbar">
    <div class="navbar-content">
      <!-- Logo 区域 -->
      <div class="navbar-logos">
        <img src="@/assets/logo.png" alt="SAITEC Logo" class="navbar-logo" />
        <img src="@/assets/logo-2.png" alt="Secondary Logo" class="navbar-logo2" />
      </div>
      <!-- 导航链接区域 -->
      <nav class="navbar-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/benchmarks" class="nav-link">Benchmarks</router-link>
        <router-link to="/papers" class="nav-link">Papers</router-link>
        <router-link to="/about" class="nav-link">About</router-link>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: "Navbar",
};
</script>

<style>
.navbar {
  display: flex;
  justify-content: flex-start; /* 确保内容从左开始对齐 */
  align-items: center;
  background-color: #111;
  padding: 10px 20px;
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 10;
}

.navbar-content {
  display: flex;
  align-items: center;
  width: 100%; /* 使导航栏内容填满整个横向 */
}

.navbar-logos {
  display: flex;
  align-items: center;
  margin-right: 20px; /* Logo 和导航链接之间的间距 */
}

.navbar-logo {
  height: 50px;
  width: auto;
  margin-right: 20px;
}

.navbar-logo2 {
  height: 18px;
  width: auto;
  margin-right: 100px;
}

.navbar-links {
  display: flex;
  gap: 40px; /* 控制导航链接之间的间距 */
  align-items: center;
}

.navbar-links .nav-link {
  text-decoration: none;
  color: white;
  font-size: 1.2em;
  padding: 10px 15px;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.navbar-links .nav-link:hover {
  background-color: #000;
  filter: brightness(1.2);
}

button::after,
a::after,
.navbar-links .nav-link::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: -5px;
  width: 8px;
  height: 8px;
  background-color: #f6f8fa;
  border-radius: 50%;
  transform: scale(0);
  transition: transform 0.3s ease;
  opacity: 0;
}

button:hover::after,
a:hover::after,
.navbar-links .nav-link:hover::after {
  transform: scale(1);
  opacity: 1;
}
</style>
