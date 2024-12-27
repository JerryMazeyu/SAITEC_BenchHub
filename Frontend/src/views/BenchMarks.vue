<template>
    <div>
        <main>
            <div class="benchmark-title">
                <h1>
                    Benchmark Hub
                </h1>
                <h3>
                    Here, we offer a wide range of comprehensive evaluation benchmarks.
                </h3>
            </div>
            <div class="benchmark-intro">
                <n-flex justify="center" size="large" align="center">
                    <!-- Progress Bar on the Left -->
                    <div class="process-bar">
                        <n-space vertical>
                            <n-steps vertical :current="currentCardIndex">
                                <n-step title="Number of evaluation data" description="" />
                                <n-step title="Evaluation Dimensions" description="" />
                                <n-step title="Evaluation Features" description="" />
                                <n-step title="Evaluation advantages" description="" />
                            </n-steps>
                        </n-space>
                    </div>
                    <!-- Cards on the Right -->
                    <div class="intro-play">
                        <n-card class="intro-card" v-if="currentCardIndex === 1" title="Number of evaluation data"
                            size="large" hoverable>
                            <n-ul>
                                <n-li>Unimodal data: a total of <n-text type="success">
                                        <n-number-animation :from="0" :to="29819" />
                                    </n-text> entries</n-li>
                                <n-li>Multimoda data: a total of <n-text type="success">
                                        <n-number-animation :from="0" :to="8189" />
                                    </n-text> entries</n-li>
                                <n-li>Nearly <n-text type="success">
                                        <n-number-animation :from="0" :to="40000" />
                                    </n-text> entries of comprehensive international standard dimension test
                                    datasets</n-li>
                            </n-ul>
                        </n-card>
                        <n-card class="intro-card" v-if="currentCardIndex === 2" title="Evaluation Dimensions"
                            size="large" hoverable>
                            <n-ul>
                                <n-li>Unimodal tasks: Text classification, math reasoning, and information
                                    extraction, etc.</n-li>
                                <n-li>Multimodal tasks: Image, text, and audio understanding.</n-li>
                                <n-li><n-text type="success">
                                        Safety tasks:
                                    </n-text>Fairness, compliance, and robustness.</n-li>
                                <n-li><n-text type="success">
                                        Domain-specific tasks:
                                    </n-text>Evaluate knowledge and reasoning in fields like
                                    healthcare,
                                    law, education, and finance.</n-li>
                            </n-ul>
                        </n-card>
                        <n-card class="intro-card" v-if="currentCardIndex === 3" title="Evaluation Features"
                            size="large" hoverable>
                            <n-ul>
                                <n-li><n-text type="success">
                                        Aligns with National Standards:
                                    </n-text>Adheres to “AI Pre-trained Model Part 2: Evaluation Indicators and
                                    Methods”.</n-li>
                                <n-li><n-text type="success">
                                        Covers Safety Capabilities:
                                    </n-text>Evaluates fairness, hallucination, and compliance.</n-li>
                                <n-li><n-text type="success">
                                        Assesses Multimodal Capabilities:
                                    </n-text>Fills gaps in image-text task coverage.</n-li>
                                <n-li><n-text type="success">
                                        Assesses Domain Capabilities:
                                    </n-text>Improves fine-grained domain-specific coverage lacking in traditional
                                    datasets.</n-li>
                            </n-ul>
                        </n-card>
                        <n-card class="intro-card" v-if="currentCardIndex === 4" title="Evaluation advantages"
                            size="large" hoverable>
                            <n-ul>
                                <n-li><n-text type="success">
                                        Comprehensive Evaluation of Basic, Safety, and Domain Capabilities:
                                    </n-text>Covers basic (unimodal- and multimodal), safety (hallucination,
                                    fairness, legality,
                                    robustness), and domain-specific (law, education, medicine, finance)
                                    capabilities to ensure broad
                                    and precise evaluation.</n-li>
                                <n-li><n-text type="success">
                                        Fully Automated Evaluation and Reporting:
                                    </n-text>Automates task execution and result analysis, generating structured
                                    reports to present
                                    model performance and evaluation outcomes.</n-li>
                            </n-ul>
                        </n-card>
                    </div>
                    <div class="statistics">
                        <n-carousel autoplay show-arrow>
                            <img class="carousel-img" src="../assets/单模态能力.png">
                            <img class="carousel-img" src="../assets/多模态能力.png">
                        </n-carousel>
                    </div>
                </n-flex>
            </div>
            <div class="filter-control">
                <n-flex justify="center" direction="row" wrap="wrap">
                    <div>
                        <n-button class="filter-buttons" size="large" @click="categoryFilter(0)" round>All</n-button>
                        <n-button class="filter-buttons" size="large" @click="categoryFilter(1)" round>Unimodal
                        </n-button>
                        <n-button class="filter-buttons" size="large" @click="categoryFilter(2)"
                            round>Multimodal</n-button>
                        <n-button class="filter-buttons" size="large" @click="categoryFilter(3)"
                            round>Security</n-button>
                    </div>
                    <div class="filter-search">
                        <n-input v-model:value="searchQuery" />
                        <n-button type="primary" ghost @click="searchFilter()">
                            <template #icon>
                                <n-icon>
                                    <Search48Regular />
                                </n-icon>
                            </template>
                            Search
                        </n-button>
                    </div>
                </n-flex>
            </div>
            <div class="filtered-cards">
                <n-flex justify="center">
                    <n-skeleton v-if="loadingCards" v-for="index in filteredDatasets.length" :width="400" :height="100"  :sharp="false" size="medium" />
                    <n-card class="filtered-card" v-else v-for="(row, index) in filteredDatasets" :key="index" hoverable
                        @click="toQA(row)" title="">
                        <div><n-h3><n-text type="success">{{ row.name }}</n-text></n-h3></div>
                        <div>{{ row.description }}</div>
                        <div> <n-tag class="filtered-card-tag" round v-for="(tag, index) in row.tag" :bordered="false">
                                {{ tag }}
                            </n-tag></div>
                    </n-card>
                </n-flex>
            </div>
        </main>
    </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { Search48Regular } from '@vicons/fluent';
import { useMessage } from 'naive-ui'
import { useRouter } from 'vue-router';
// import {getAllBenchMarks} from '@/api/benchMarks'

export default {
    name: 'BenchMarks',
    components: {
        Search48Regular
    },
    setup() {
        const router = useRouter();
        const currentCardIndex = ref(1);
        const intervalId = ref(null);
        const loadingCards = ref(false);
        const searchQuery = ref('');
        const message = useMessage()

        const datasets = [
            { id:'1',name: "文本分类", description: "将文本划分为不同的类别或标签。可以应用于垃圾邮件过滤、情感分析、新闻分类等应用场景", tag: ["单模态", "文本理解"] },
            { id:'2',name: "信息抽取", description: "指模型能够根据文本内容，完成内容、实体、事件、属性、关系等信息的抽取", tag: ["单模态", "文本理解"] },
            { id:'3',name: "数学推理", description: "指理解和应用数学概念、原理来解决涉及数学运算问题的能力。如解析表达式、图形识别、公式推导等", tag: ["单模态", "文本理解"] },
            { id:'4',name: "文本分类", description: "将文本划分为不同的类别或标签。可以应用于垃圾邮件过滤、情感分析、新闻分类等应用场景", tag: ["单模态", "文本理解"] },
            { id:'5',name: "信息抽取", description: "指模型能够根据文本内容，完成内容、实体、事件、属性、关系等信息的抽取", tag: ["单模态", "文本理解"] },
            { id:'6',name: "数学推理", description: "指理解和应用数学概念、原理来解决涉及数学运算问题的能力。如解析表达式、图形识别、公式推导等", tag: ["单模态", "文本理解"] },
            { id:'7',name: "文本分类", description: "将文本划分为不同的类别或标签。可以应用于垃圾邮件过滤、情感分析、新闻分类等应用场景", tag: ["单模态", "文本理解"] },
            { id:'8',name: "信息抽取", description: "指模型能够根据文本内容，完成内容、实体、事件、属性、关系等信息的抽取", tag: ["单模态", "文本理解"] },
            { id:'9',name: "数学推理", description: "指理解和应用数学概念、原理来解决涉及数学运算问题的能力。如解析表达式、图形识别、公式推导等", tag: ["单模态", "文本理解"] },
        ];

        const filteredDatasets = ref([]);

        const updateCardIndex = () => {
            currentCardIndex.value = currentCardIndex.value < 4 ? currentCardIndex.value + 1 : 1;
        };

        const categoryFilter = (option) => {
            if (option === 0) {
                loadingCards.value = true
                filteredDatasets.value = datasets;
                setTimeout(() => {
                    loadingCards.value = false;
                }, 500);
            } else if (option === 1) {
                loadingCards.value = true
                filteredDatasets.value = datasets.filter(item => item.tag.includes("单模态"));
                setTimeout(() => {
                    loadingCards.value = false;
                }, 500);
            } else if (option === 2) {
                loadingCards.value = true
                filteredDatasets.value = datasets.filter(item => item.tag.includes("多模态"));
                setTimeout(() => {
                    loadingCards.value = false;
                }, 500);
            } else if (option === 3) {
                loadingCards.value = true
                filteredDatasets.value = datasets.filter(item => item.tag.includes("安全性"));
                setTimeout(() => {
                    loadingCards.value = false;
                }, 500);
            }
        };

        const searchFilter = () => {
            if (searchQuery.value !== '') {
                loadingCards.value = true
                filteredDatasets.value = filteredDatasets.value.filter((item) => item.name.includes(searchQuery.value));
                setTimeout(() => {
                    loadingCards.value = false;
                }, 500);
            }
            else {
                message.warning("Search keyword cannot be empty")
            }
        };

        const toQA = (benchmark) => {
            localStorage.setItem('thisBenchMark', JSON.stringify(benchmark));
            router.push("/questionAnswer")
        };

        onMounted(() => {
            intervalId.value = setInterval(updateCardIndex, 8000);
            
            // 获取到所有的benchmarks
            // loadingCards.value=true
            // getAllBenchMarks().then(res=>{
            //     datasets.value=res.data
            //     filteredDatasets.value=this.datasets
            // loadingCards.value=false
            // })
        });

        onBeforeUnmount(() => {
            clearInterval(intervalId.value);
        });

        return {
            currentCardIndex,
            loadingCards,
            searchQuery,
            filteredDatasets,
            categoryFilter,
            searchFilter,
            toQA
        };
    }
};
</script>


<style>
.benchmark-title {
    display: flex;
    flex-direction: column;
    /* 垂直排列 */
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    position: relative;
    margin: 0;
    padding: 0;
    margin-top: 100px;
}

.benchmark-title h1 {
    margin: 0 0 20px;
    /* 与 h3 保持一定的间距 */
    font-size: 2.5em;
}

.benchmark-title h3 {
    margin: 0;
    margin-bottom: 40px;
    font-size: 1.2em;
}

.benchmark-intro {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
}

.process-bar {
    margin-right: 0px;
}

.intro-control {
    margin-top: 20px;
}

.intro-play {
    transition: box-shadow 0.5s ease-in-out;
    /* 控制发光效果的平滑过渡 */
    box-shadow: 0 0 0 rgba(99, 226, 183, 0);
    /* 初始无发光 */
}

.intro-play:hover {
    box-shadow: 0 0 5px 2px rgba(99, 226, 183, 0.8);
    /* 鼠标悬浮时的发光效果 */
}

.intro-card {
    width: 500px;
    flex-shrink: 0;
    /* 防止卡片因容器宽度不足被压缩 */
    height: 280px;
    background-color: black;
    border-radius: 20px
}

.statistics {
    width: 600px;
    height: 280px;
    transition: box-shadow 0.5s ease-in-out;
}

.statistics:hover {
    box-shadow: 0 0 5px 2px rgba(99, 226, 183, 0.8);
    /* 鼠标悬浮时的发光效果 */
}

.carousel-img {
    width: 100%;
    /* 图片宽度自适应轮播框 */
    height: 100%;
    /* 图片高度自适应轮播框 */
    object-fit: fill;
    /* 填充轮播框，可能裁剪部分图片 */
}

.filter-control {
    margin-top: 100px
}

.filter-buttons {
    margin-left: 10px
}

.filter-search {
    margin-left: 100px;
    display: flex;
    /* 使用Flexbox布局 */
    align-items: center;
    /* 垂直居中对齐 */
    gap: 10px;
    /* 设置输入框和按钮之间的间距 */
    width: 400px;
}

.filter-search n-input {
    flex: 1;
    /* 输入框可以根据需要伸缩 */
}

.filtered-cards {
    margin-top: 20px;
}

.filtered-cards .filtered-card {
    width: 400px;
    margin: 20px;
    transition: box-shadow 0.5s ease-in-out;
    box-shadow: 0 0 0 rgba(99, 226, 183, 0);
    cursor: pointer
}

.filtered-cards .filtered-card:hover {
    box-shadow: 0 0 5px 2px rgba(99, 226, 183, 0.8);
}

.filtered-card-tag {
    margin: 5px;
    margin-top: 10px;
}
</style>