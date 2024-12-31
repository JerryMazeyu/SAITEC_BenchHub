<template>
  <div id="app">
    <main class="homepage">
      <div class="welcome-section">
        <div class="welcome-text">
          <h1>Shanghai Generative AI Testing and Evaluation Center Benchhub</h1>
          <div class="typing-area"><span class="currentText" v-html="currentText"></span><span class="cursor"></span>
          </div>
          <div class="button-group">
            <n-flex>
              <router-link to="/benchmarks"> <n-button ghost type="primary" size="large"><template #icon>
                    <ClipboardDataBar24Regular />
                  </template>Benchmarks</n-button></router-link>
              <router-link to="/papers"><n-button size="large" type="primary" ghost>
                  <template #icon>
                    <NewspaperOutline />
                  </template>
                  Papers
                </n-button></router-link>
            </n-flex>
          </div>
        </div>
        <div id="dynamic-background"></div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { ClipboardDataBar24Regular } from '@vicons/fluent';
import { NewspaperOutline } from "@vicons/ionicons5"

export default {
  name: "Homepage",
  components: {
    ClipboardDataBar24Regular,
    NewspaperOutline
  },
  setup() {
    const messages = [
      "Here, we provide evaluation benchmarks covering a wide range of dimensions, along with the display of all use cases included.",
      "We have also carefully curated articles spanning various evaluation dimensions, which can be helpful for enhancing the model's performance.",
      "Let's click the button below to start..."
    ];

    const currentText = ref("");
    const messageIndex = ref(0);
    const charIndex = ref(0);
    const typingSpeed = 50; // Typing speed in ms
    const deletingSpeed = 10; // Deleting speed in ms
    const delayBeforeDelete = 2000; // Delay between messages in ms
    const delayBetweenMessages = 1000;

    const typeText = () => {
      if (charIndex.value < messages[messageIndex.value].length) {
        currentText.value += messages[messageIndex.value][charIndex.value];
        charIndex.value++;
        setTimeout(typeText, typingSpeed);
      } else {
        setTimeout(deleteText, delayBeforeDelete);
      }
    };

    const nextMessage = () => {
      charIndex.value = 0;
      messageIndex.value = (messageIndex.value + 1) % messages.length;
      currentText.value = "";
      typeText();
    };

    const deleteText = () => {
      if (charIndex.value > 0) {
        // Deleting characters one by one
        charIndex.value--;
        currentText.value = currentText.value.slice(0, charIndex.value);
        setTimeout(deleteText, deletingSpeed);
      } else {
        // Move to the next message after deleting
        setTimeout(nextMessage, delayBetweenMessages);
      }
    };

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

    onMounted(() => {
      addDynamicBackground();
      typeText();
    });

    return {
      currentText,
    };
  },
};
</script>

<style>
html {
  overflow: hidden;
  /* 确保 html 元素也隐藏滚动条 */
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

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
  /* padding-top: 50px; */
}

.welcome-section {
  display: flex;
  justify-content: center;
  width: 100%;
  height: 100%;
  position: relative;
  margin: 0;
  padding: 0;
}

.welcome-text {
  position: relative;
  z-index: 1;
  font-weight: bold;
  text-align: left;
  /* background-color: blue; */
  width: 90%;
  height: 15%;
  margin-top: 20%;
}

.welcome-text h1 {
  font-size: 5ch;
}

.currentText {
  font-size: x-large;
  font-family:'Courier New', Courier, monospace
}

.typing-area {
  height: 100px;
}

#dynamic-background {
  position: absolute;
  top: 0;
  left: 0;
  margin: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.cursor {
  display: inline-block;
  width: 10px;
  height: 1em;
  background-color: #fff;
  animation: blink 0.6s steps(1) infinite;
  margin-left: 5px;
  /* 与文本保持一定距离 */
}

@keyframes blink {
  50% {
    opacity: 0;
  }
}

.button-group {
  position: fixed;
}
</style>
