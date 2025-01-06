<template>
    <n-grid :x-gap="8" :y-gap="8" cols="12">
        <n-grid-item :span="12">
            <div class="section title-section">
                <div class="paper-title">
                    <h1>
                        Papers Hub
                    </h1>
                    <h3>
                        Here, we've got some great resources for articles that can help with model performance
                    </h3>
                </div>
            </div>
        </n-grid-item>
        <n-grid-item :span="12">
            <div class="section filter-section">
                <n-flex class="filter-control" justify="center">
                    <n-select class="selector" v-model:value="valueClass" size="large" :options="optionsClass"
                        placeholder="Please Select The Data Category" />
                    <n-select class="selector" size="large" disabled v-if="valueClass === 0 || valueClass === null"
                        placeholder="Please Select The Benchmark" />
                    <n-select class="selector" v-else v-model:value="valueBenchmark" size="large"
                        :options="optionsBenchmark" placeholder="Please Select The Benchmark" />
                    <n-button size="large" type="primary" ghost @click="optionFilter()">
                        <template #icon>
                            <n-icon>
                                <Filter />
                            </n-icon>
                        </template>
                        Filter
                    </n-button>
                    <div class="search-input">
                        <n-input size="large" v-model:value="searchQuery"
                            placeholder="Please Intput The Search Query" />
                    </div>
                    <n-button size="large" type="primary" ghost @click="searchFilter()">
                        <template #icon>
                            <n-icon>
                                <Search48Regular />
                            </n-icon>
                        </template>
                        Search
                    </n-button>
                    <n-button ghost type="info" size="large" @click="resetFilter()"><template #icon>
                            <Reset />
                        </template>Reset</n-button>
                </n-flex>
                <div class="showPapersNumber" v-if="showNumber">
                    <n-h3>In the field of <n-text type="success">{{ valueBenchmark }}</n-text>, we have collected
                        <n-text type="success"><n-number-animation :from="0" :to="filteredPapers.length" /></n-text>
                        high-quality
                        articles</n-h3>
                </div>
                <div class="showPapersNumber" v-else>
                    <n-h3>In <n-text type="success">total</n-text>, we have collected <n-text
                            type="success"><n-number-animation :from="0" :to="papers.length" /></n-text> high-quality
                        articles</n-h3>
                </div>
            </div>
        </n-grid-item>
        <n-grid-item :span="12">
            <div class="section paper-section">
                <div class="papers-list">
                    <n-skeleton class="skeleton" v-if="loadingPapers" v-for="n in 10" :sharp="false" :height="150" />
                    <n-list v-else hoverable clickable>
                        <n-list-item v-for="(row, index) in currentPapers">
                            <n-h3><n-text type="success"><b>{{ row.name }}</b></n-text></n-h3>
                            <n-tag type="info" :bordered="false">{{ row.class }}</n-tag>
                            <h4><n-text type="success"><b>Author:</b></n-text> {{ row.author }}</h4>
                            <h4><n-text type="success"><b>Journal:</b></n-text> {{ row.journal }}</h4>
                            <n-blockquote>{{ row.abstract }}</n-blockquote>
                            <template #suffix>
                                <n-button round size="large" dashed @click="readPaper(row.file_url)"> <template #icon>
                                        <n-icon>
                                            <NewspaperOutline />
                                        </n-icon>
                                    </template>Read This Paper</n-button>
                            </template>
                        </n-list-item>
                    </n-list>
                    <n-pagination class="pagination" v-model:page="page" :page-count="totalPage" size="large"
                        show-quick-jumper>
                        <template #goto>
                            Go To Page
                        </template>
                    </n-pagination>
                </div>
            </div>
        </n-grid-item>
    </n-grid>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useMessage } from 'naive-ui'
import { Search48Regular } from '@vicons/fluent';
import { Filter } from "@vicons/carbon"
import { NewspaperOutline } from "@vicons/ionicons5"
import { Reset } from "@vicons/carbon"
// import {getAllPapers} from "@/api/papers"

export default {
    name: "Papers",
    components: {
        Search48Regular,
        Filter,
        NewspaperOutline,
        Reset
    },
    setup() {
        const loadingPapers = ref(false)
        const message = useMessage()
        const papers = ref(
            [
                {
                    name: "探索语言模型在文本分类中的应用",
                    author: "fyf2007",
                    journal: "CSDN博客",
                    abstract: "论文首先分析了语言模型中幻觉问题的来源，即模型可能生成与现实不符或误导性的文本内容。这种现象源于语言模型在无监督学习中对大规模训练语料的统计模式进行建模，却缺乏事实校验和语义理解能力。随后，作者提出了一系列减少幻觉问题的技术与非技术手段",
                    class: "文本分类",
                    file_url: "https://arxiv.org/pdf/2305.16291",
                },
                {
                    name: "利用LLMs解决信息抽取任务｜综述",
                    author: "养生的控制人",
                    journal: "知乎专栏",
                    abstract: "论文首先分析了语言模型中幻觉问题的来源，即模型可能生成与现实不符或误导性的文本内容。这种现象源于语言模型在无监督学习中对大规模训练语料的统计模式进行建模，却缺乏事实校验和语义理解能力。随后，作者提出了一系列减少幻觉问题的技术与非技术手段",
                    class: "信息抽取",
                    file_url: "https://arxiv.org/pdf/2305.16291",
                },
                {
                    name: "大模型推理最新论文及源码合集，涵盖多模态推理、逻辑推理",
                    author: "weixin_42645636",
                    journal: "CSDN博客",
                    abstract: '论文首先分析了语言模型中幻觉问题的来源，即模型可能生成与现实不符或误导性的文本内容。这种现象源于语言模型在无监督学习中对大规模训练语料的统计模式进行建模，却缺乏事实校验和语义理解能力。随后，作者提出了一系列减少幻觉问题的技术与非技术手段',
                    class: "数学推理",
                    file_url: "https://arxiv.org/pdf/2305.16291",
                }
            ]
        );
        const filteredPapers = ref([]);
        const datasets = ref(
            [
                { id: '1', name: "文本分类", description: "将文本划分为不同的类别或标签。可以应用于垃圾邮件过滤、情感分析、新闻分类等应用场景", class: "单模态" },
                { id: '2', name: "信息抽取", description: "指模型能够根据文本内容，完成内容、实体、事件、属性、关系等信息的抽取", class: "单模态" },
                { id: '3', name: "数学推理", description: "指理解和应用数学概念、原理来解决涉及数学运算问题的能力。如解析表达式、图形识别、公式推导等", class: "单模态" }
            ]
        )
        const optionsClass = ref(
            [
                {
                    label: 'All',
                    value: 0
                },
                {
                    label: 'Unimodal',
                    value: 1
                },
                {
                    label: 'Multimodal',
                    value: 2
                },
                {
                    label: 'Security',
                    value: 3,
                },
            ]
        );
        const optionsBenchmark = computed(() => {
            valueBenchmark.value = null
            // filteredDatasets 直接初始化为普通数组
            let filteredDatasets = [];

            // 确保 datasets.value 是一个数组，并根据 valueClass 进行过滤
            if (valueClass.value === 1) {
                filteredDatasets = datasets.value.filter(item => item.class.includes("单模态"));
            } else if (valueClass.value === 2) {
                filteredDatasets = datasets.value.filter(item => item.class.includes("多模态"));
            } else if (valueClass.value === 3) {
                filteredDatasets = datasets.value.filter(item => item.class.includes("安全性"));
            }
            if (filteredDatasets.length !== 0) {
                let filteredOptions = []
                filteredOptions = filteredDatasets.map(item => ({
                    label: item.name,
                    value: item.name,
                }));
                return filteredOptions
            }
            else {
                return []
            }
        });
        const valueBenchmark = ref(null);
        const valueClass = ref(null);
        const showNumber = ref(false)
        const searchQuery = ref('')
        const page = ref(1)
        const totalPage = computed(() => {
            return Math.ceil(filteredPapers.value.length / 10);
        });

        const currentPapers = computed(() => {
            const start = (page.value - 1) * 10;
            const end = page.value * 10;
            return filteredPapers.value.slice(start, end);
        });

        const optionFilter = () => {
            if (valueClass.value === null) {
                message.warning("Please Select The Data Category")
                return
            }
            if (valueBenchmark.value === null && valueClass.value !== 0) {
                message.warning("Please Select The Benchmark")
                return
            }
            if (valueClass.value === 0) {
                loadingPapers.value = true
                filteredPapers.value = papers.value
                showNumber.value = false
                setTimeout(() => {
                    loadingPapers.value = false;
                }, 500);
            }
            else {
                loadingPapers.value = true
                filteredPapers.value = papers.value.filter(item => item.class.includes(valueBenchmark.value))
                showNumber.value = true
                setTimeout(() => {
                    loadingPapers.value = false;
                }, 500);
            }
        }
        const searchFilter = () => {
            loadingPapers.value = true
            filteredPapers.value = filteredPapers.value.filter(item =>
                item.name.includes(searchQuery.value) || item.author.includes(searchQuery.value)
            );

            setTimeout(() => {
                loadingPapers.value = false;
            }, 500);
        }
        const resetFilter = () => {
            loadingPapers.value = true
            searchQuery.value = '',
                valueClass.value = null,
                valueBenchmark.value = null,
                filteredPapers.value = papers.value
            setTimeout(() => {
                loadingPapers.value = false;
            }, 500)
        }
        const readPaper = (fileUrl) => {
            if (!fileUrl) {
                message.error("Invalid file URL");
                return;
            }
            // 创建一个隐藏的 <a> 标签
            const link = document.createElement('a');
            link.href = fileUrl; // 设置文件地址
            link.download = ''; // 设置文件名，可以设置具体名称，比如 `filename.pdf`
            link.target = '_blank'; // 兼容某些浏览器的跨域文件下载
            document.body.appendChild(link);
            link.click(); // 触发点击事件
            document.body.removeChild(link); // 下载完成后移除元素
        }
        onMounted(() => {
            loadingPapers.value = true
            // 获取所有paper
            // getAllPapers.then(res=>{
            //     papers.value=res.data;
            //     filteredPapers=papers.value
            // })

            // 这是假数据
            filteredPapers.value = papers.value

            setTimeout(() => {
                loadingPapers.value = false;
            }, 500)
        });
        return {
            optionsClass,
            valueClass,
            datasets,
            valueBenchmark,
            optionsBenchmark,
            showNumber,
            loadingPapers,
            searchQuery,
            filteredPapers,
            papers,
            page,
            totalPage,
            currentPapers,
            optionFilter,
            searchFilter,
            resetFilter,
            readPaper
        }
    }
}
</script>

<style>
.section {
    width: 90%;
    margin-left: 5%;
}

.title-section {
    margin-top: 70px;
    height: 150px;
}

.paper-title {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0px;
}

.filter-section {
    height: auto;
    margin-top: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    /* display: flex;
    align-items: center;
    justify-content: center; */
}

.filter-control {
    margin: 20px;
    width: 100%;
    height: 100%;
}

.selector {
    width: 23%;
}

.search-input {
    width: 23%;
}

.showPapersNumber {
    /* background-color: rgb(206, 15, 15); */
    width: 100%;
    display: flex;
    justify-content: center;
    font-family: 'Times New Roman', Times, serif;
    font-weight: bold;
}

.paper-section {
    height: auto;
    margin-top: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 8px;
}

.papers-list {
    margin: 20px;
    margin-bottom: 100px;
}

.pagination {
    margin-top: 20px;
}

.skeleton {
    margin: 20px;
    height: 300px;
    width: 95%;
}
</style>