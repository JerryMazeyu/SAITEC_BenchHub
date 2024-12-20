<template>
    <header class="navbar">
        <div class="navbar-content">
            <div class="navbar-logos">
                <img src="@/assets/logo.png" alt="SAITEC Logo" class="navbar-logo" />
                <img src="@/assets/logo-2.png" alt="Secondary Logo" class="navbar-logo2" />
            </div>
            <nav class="navbar-links">
                <router-link to="/" class="nav-link">Home</router-link>
                <router-link to="/benchmarks" class="nav-link">Benchmarks</router-link>
                <router-link to="/papers" class="nav-link">Papers</router-link>
                <router-link to="/about" class="nav-link">About</router-link>
            </nav>
          <button class="login-button">Login</button>
        </div>
      </header>
</template>

<script>
export default {
  name: 'Navbar',
};
</script>

<style>
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #111;
    padding: 10px 20px;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 10;
  }
  .navbar-logos {
  display: flex; 
  align-items: center;
}

  .navbar-logo {
  height: 50px;
  width: auto;
  margin-right: 20px; 
}

.navbar-logo2 {
  height: 18px;
  width: auto;
  margin-right: 20px;
}

  .navbar-links {
  display: flex;
  align-items: center;
  gap: 15px;
}

  .navbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 70%;
  margin-left: 15%;
}
  
  .navbar-title {
    font-size: 1.5em;
    font-weight: bold;
  }
  
  .navbar-links a,
  .navbar-links .nav-link {
    text-decoration: none;
    color: white;
    font-size: 1.2em;
    padding: 15px 20px;
    border-radius: 1px;
    transition: background-color 0.4s ease, color 0.4s ease;
  }
  
  .navbar-links a:hover,
  .navbar-links .nav-link:hover {
    filter: brightness(1.2);
    background-color: #000;
  }
  
  .login-button {
    background-color: #000;
    border: none;
    color: white;
    font-size: 1.2em;
    padding: 15px 20px;
    cursor: pointer;
    border-radius: 1px;
    transition: background-color 0.4s ease, color 0.4s ease;
    margin-left: auto;
  }
  
  .login-button:hover {
    filter: brightness(1.2);
    background-color: #000;
  }

  button::after, a::after,
.navbar-links .nav-link::after {
  content: '';
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

    button:hover::after, a:hover::after,
    .navbar-links .nav-link:hover::after {
    transform: scale(1);
    opacity: 1;
    }
</style>


