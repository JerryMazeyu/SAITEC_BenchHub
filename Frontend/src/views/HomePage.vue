<template>
  <div id="app">
    <!-- <Navbar /> -->
    <main class="homepage">
      <div class="welcome-section">
        <h2 class="welcome-text">
          <span v-for="(word, index) in words" :key="index" class="word" @mouseover="hoverEffect"
            @mouseout="removeEffect">
            {{ word }}
          </span>
        </h2>
        <div id="dynamic-background"></div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  name: "Homepage",
  setup() {
    const words = ref([
      "Shanghai ",
      "Generative ",
      "AI ",
      "Testing ",
      "and ",
      "Evaluation ",
      "Center ",
      "Benchhub",
    ]);

    const addDynamicBackground = () => {
      const canvas = document.createElement("canvas");
      canvas.id = "dynamic-background";
      document.querySelector(".welcome-section").appendChild(canvas);

      const ctx = canvas.getContext("2d");
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;

      const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
      const particles = [];

      for (let i = 0; i < 100; i++) {
        const charCount = Math.floor(Math.random() * 10) + 1;
        let charGroup = "";
        for (let j = 0; j < charCount; j++) {
          charGroup += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          char: charGroup,
          fontSize: Math.random() * 2 + 10,
          dx: (Math.random() - 0.5) * 2,
          dy: (Math.random() - 0.5) * 2,
        });
      }

      function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach((p) => {
          ctx.font = `${p.fontSize}px Arial`;
          ctx.fillStyle = "rgba(150, 150, 150, 1)";
          ctx.fillText(p.char, p.x, p.y);

          p.x += p.dx;
          p.y += p.dy;

          if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
          if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
        });

        requestAnimationFrame(animate);
      }

      animate();
    };

    const hoverEffect = (event) => {
      event.target.classList.add("hovered");
    };

    const removeEffect = (event) => {
      event.target.classList.remove("hovered");
    };

    onMounted(() => {
      addDynamicBackground();
      const element = document.querySelector(".welcome-text");
      if (element) {
        element.classList.add("appear");
      }
    });

    return {
      words,
      hoverEffect,
      removeEffect,
    };
  },
};
</script>


<style>
body {
  overflow: hidden;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: sans-serif;
  background-color: #000;
  color: #fff;
}

.homepage {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
  text-align: center;
  padding-top: 50px;
}

.welcome-section {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  /* 确保宽度为 100% */
  height: 100%;
  /* 确保高度为 100% */
  position: relative;
  margin: 0;
  padding: 0;
}

.welcome-text {
  position: relative;
  z-index: 1;
  font-size: 5.5em;
  font-weight: bold;
  text-align: center;
  margin-left: 20%;
  margin-right: 20%;
  opacity: 0;
  transition: opacity 2s ease-in-out;
  /* 3秒缓慢过渡 */
}

.welcome-text.appear {
  opacity: 1;
}

#dynamic-background {
  position: absolute;
  top: 0;
  left: 0;
  margin: 0;
  /* width: 100%; */
  height: 100%;
  z-index: 0;
}

.word {
  margin: 0 5px;
  display: inline-block;
  transition: text-shadow 0.5s ease-in-out, color 0.5s ease-in-out;
  /* 加入缓慢的过渡效果 */
  cursor: pointer;
}

.word.hovered {
  color: #ffffff;
  /* 发光的颜色：白色 */
  text-shadow:
    0 0 2px #ffffff,
    0 0 4px #ffffff,
    0 0 8px #ffffff;
  /* 减弱发光效果 */

}
</style>