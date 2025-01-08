<template>
    <n-grid :x-gap="8" :y-gap="8" cols="12">
        <!-- 上半部分 -->
        <n-grid-item :span="12">
            <div class="top-section">
                <div class="benchmark-intro" v-if="thisBenchMark.name">
                    <h1>Test Cases Hub</h1>
                    <h3>Here we provide test cases from <n-text type="success">{{ thisBenchMark.name }}</n-text></h3>
                </div>
            </div>
        </n-grid-item>

        <!-- 下半部分左侧 -->
        <n-grid-item :span="9">
            <div class="content-section bottom-left-section">
                <div class="show-qa">
                    <n-skeleton v-if="loadingQA" v-for="n in 10" class="skeleton" :height="150" :sharp="false" />
                    <n-list v-else>
                        <n-list-item v-for="(row, index) in currentQA" :key="index">
                            <!-- 左侧内容 -->
                            <n-thing>
                                <div class="qa-content">
                                    <div class="qa">
                                        <n-text type="success"><b>Question <n-icon>
                                                    <QuestionCircle16Regular />
                                                </n-icon></b></n-text>
                                        <n-blockquote v-if="row.question.text">{{ row.question.text }}</n-blockquote>
                                        <n-blockquote v-else>{{ row.question }}</n-blockquote>
                                    </div>
                                    <div class="qa">
                                        <n-text type="success"><b>Answer <n-icon>
                                                    <QuestionAnswerOutlined />
                                                </n-icon></b></n-text>
                                        <n-blockquote>{{ row.answer }}</n-blockquote>
                                    </div>
                                    <div class="qa">
                                        <n-text type="success"><b>Check Metadata <n-icon>
                                                    <Info20Regular />
                                                </n-icon></b></n-text>
                                        <n-switch class="switchMeta" v-model:value="showMetaData[index]"></n-switch>
                                        <n-collapse-transition :show="showMetaData[index]">
                                            <div class="meta-data">
                                                <n-h5><n-text type="success">Uploader
                                                        <n-icon>
                                                            <Accessibility16Regular />
                                                        </n-icon></n-text>
                                                </n-h5>
                                                <div v-if="row.uploader">{{ row.uploader }}</div>
                                                <div v-else><n-tag type="info">
                                                        No Uploader
                                                    </n-tag></div>
                                                <n-h5><n-text type="success">Date Note
                                                        <n-icon>
                                                            <CalendarRtl28Regular />
                                                        </n-icon>
                                                    </n-text></n-h5>
                                                {{ row.created_at }}
                                                <n-h5><n-text type="success">Date Resource
                                                        <n-icon>
                                                            <CloudDataOps />
                                                        </n-icon>
                                                    </n-text></n-h5>
                                                {{ row.data_resource }}
                                                <n-h5><n-text type="success">Answer Mode
                                                        <n-icon>
                                                            <Apps20Regular />
                                                        </n-icon>
                                                    </n-text></n-h5>
                                                <div v-if="row.answer_mode === 'level1'"><n-tag type="info">Open-ended
                                                        Answer</n-tag></div>
                                                <div v-if="row.answer_mode === 'level2'"><n-tag
                                                        type="info">Propositional
                                                        Answer</n-tag></div>
                                            </div>
                                        </n-collapse-transition>
                                    </div>
                                    <div class="qa">
                                        <n-text type="success"><b>Check Variants <n-icon>
                                                    <Version />
                                                </n-icon></b></n-text>
                                        <n-switch class="switchVariants" v-model:value="showOtherVersions[index]">
                                        </n-switch>
                                        <n-collapse-transition :show="showOtherVersions[index]">
                                            <div class="variants" v-if="row.other_version.length > 0"
                                                v-for="(version, index) in row.other_version">
                                                <div><n-text type="success">Version:</n-text>{{ version.version }}</div>
                                                <div><n-text type="success">Question:</n-text>{{ version.answer }}</div>
                                                <div><n-text type="success">Answer:</n-text>{{ version.question }}</div>
                                            </div>
                                            <div class="no-variants" v-else>
                                                <n-alert title="No other version" type="warning">
                                                    There are no other versions of this test case
                                                </n-alert>
                                            </div>
                                        </n-collapse-transition>
                                    </div>
                                    <div class="qa-buttons">
                                        <n-flex>
                                            <n-button v-if="row.question.file_url" strong secondary type="primary"
                                                @click="checkMedia(row.question.file_url)"><template #icon>
                                                    <MediaLibrary />
                                                </template>
                                                Check Meida File
                                            </n-button>
                                            <!-- 还可以继续添加其他按钮 -->
                                        </n-flex>
                                    </div>
                                </div>
                            </n-thing>

                            <!-- 右侧媒体 -->
                            <template #suffix>
                                <div class="qa-media">
                                    <div v-if="row.question.file_url">
                                        <template v-if="isImage(row.question.file_url)">
                                            <img :src="row.question.file_url" alt="Image Preview" />
                                        </template>
                                        <template v-else-if="isVideo(row.question.file_url)">
                                            <video :key="row.question.file_url" controls>
                                                <source :src="row.question.file_url" type="video/mp4" />
                                                Your browser does not support the video tag.
                                            </video>
                                        </template>
                                    </div>
                                </div>
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

        <!-- 下半部分右侧 -->
        <n-grid-item :span="3">
            <div class="content-section bottom-right-section">
                <n-card :bordered="false" class="benchmark-meta-card">
                    <n-spin :show="loadingBenchmarkCard">
                        <n-h3>Benchmark Information</n-h3>
                        <n-h5><n-text type="success">Benchmark Name
                                <n-icon>
                                    <DriveFileRenameOutlineOutlined />
                                </n-icon>
                            </n-text></n-h5>
                        <n-h3><b>{{ thisBenchMark.name }}</b></n-h3>
                        <n-h5><n-text type="success">Benchmark Class
                                <n-icon>
                                    <ClassOutlined />
                                </n-icon>
                            </n-text></n-h5>
                        <n-tag size="large" type="info">{{ thisBenchMark.class }}</n-tag>
                        <n-h5><n-text type="success">Benchmark Description
                                <n-icon>
                                    <DescriptionOutlined />
                                </n-icon>
                            </n-text></n-h5>
                        {{ thisBenchMark.description }}
                        <n-h5><n-text type="success">Total Number
                                <n-icon>
                                    <NumberRow16Regular />
                                </n-icon>
                            </n-text></n-h5>
                        <n-text type="info"><n-number-animation :from="0" :to="totalCount" /></n-text>
                    </n-spin>
                </n-card>
            </div>
        </n-grid-item>
    </n-grid>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue';
import { useMessage } from 'naive-ui'
import { Accessibility16Regular, NumberRow16Regular, Apps20Regular, CalendarRtl28Regular, QuestionCircle16Regular, Info20Regular } from '@vicons/fluent'
import { DriveFileRenameOutlineOutlined, DescriptionOutlined, ClassOutlined, QuestionAnswerOutlined } from "@vicons/material"
import { MediaLibrary, CloudDataOps, Version } from "@vicons/carbon"
import { getQAs } from '@/api/questionAnswer'

export default {
    name: 'QuestionAnswer',
    components: {
        Accessibility16Regular,
        NumberRow16Regular,
        Apps20Regular,
        CalendarRtl28Regular,
        DriveFileRenameOutlineOutlined,
        DescriptionOutlined,
        ClassOutlined,
        MediaLibrary,
        CloudDataOps,
        QuestionCircle16Regular,
        QuestionAnswerOutlined,
        Info20Regular,
        Version
    },
    setup() {
        const thisBenchMark = ref({});

        const page = ref(1)

        const loadingBenchmarkCard = ref(false)

        const loadingQA = ref(false)

        const showOtherVersions = ref(Array(10).fill(false));

        const showMetaData = ref(Array(10).fill(false));

        const message = useMessage()

        const checkMedia = (fileUrl) => {
            if (!fileUrl) {
                message.error("Invalid File URL");
                return;
            }
            message.success("Downloading")
            // 创建一个隐藏的 <a> 标签
            const link = document.createElement('a');
            link.href = fileUrl; // 设置文件地址
            link.download = ''; // 设置文件名，可以设置具体名称，比如 `filename.pdf`
            link.target = '_blank'; // 兼容某些浏览器的跨域文件下载
            document.body.appendChild(link);
            link.click(); // 触发点击事件
            document.body.removeChild(link); // 下载完成后移除元素
        }

        const isImage = (fileUrl) => {
            const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'];
            const extension = fileUrl.split('.').pop().toLowerCase();
            return imageExtensions.includes(extension);
        }

        const isVideo = (fileUrl) => {
            const videoExtensions = ['mp4', 'webm', 'ogg', 'mov'];
            const extension = fileUrl.split('.').pop().toLowerCase();
            return videoExtensions.includes(extension);
        }

        const currentQA = ref([])

        const totalCount = ref(0)

        const totalPage = computed(() => {
            return Math.ceil(totalCount.value / 10);
        });

        const fetchQAs = () => {
            loadingQA.value = true;
            getQAs({ page: page.value, page_size: 10, data_dimension: thisBenchMark.value.name })
                .then((res) => {
                    totalCount.value = res.data.data.total_count;
                    if (totalCount.value > 0) {
                        currentQA.value = processRawData(res.data.data);
                        console.log("获取并处理qa", currentQA.value);
                    } else {
                        currentQA.value = [];
                        message.info("No Data Was Obtained");
                    }
                })
                .catch((error) => {
                    console.error("Failed to fetch QAs:", error);
                })
                .finally(() => {
                    setTimeout(() => {
                        loadingQA.value = false;
                    }, 500);
                });
        };

        // 用于处理获取到的原生qa数据
        const processRawData = (rawData) => {
            const processedData = [];
            const dataItems = rawData.data;

            for (const key in dataItems) {
                if (dataItems.hasOwnProperty(key)) {
                    const item = dataItems[key];

                    // 提取第一个版本（按键顺序取第一个）
                    const [firstVersionKey, firstVersionData] = Object.entries(item)[0];

                    // 构造其他版本数据
                    const otherVersions = Object.entries(item)
                        .filter(([versionKey]) => versionKey !== firstVersionKey)
                        .map(([versionKey, versionData]) => ({
                            version: versionKey,
                            question: versionData.data_content.question,
                            answer: versionData.data_content.answer,
                        }));

                    // 构造主数据对象
                    processedData.push({
                        id: key,
                        question: firstVersionData.data_content.question,
                        answer: firstVersionData.data_content.answer,
                        uploader: firstVersionData.meta.uploader,
                        answer_mode: firstVersionData.meta.answer_mode,
                        data_resource: firstVersionData.meta.data_resource,
                        created_at: firstVersionData.meta.created_at,
                        other_version: otherVersions, // 其他版本数据
                    });
                }
            }

            return processedData;
        }

        watch(page, () => {
            // 页面变化时存储当前页数，并获取对应的数据
            localStorage.setItem('qaPage', page.value);
            fetchQAs();
        });

        onMounted(() => {
            // 初始化thisBenchMark
            const cachedData = localStorage.getItem('thisBenchMark');
            thisBenchMark.value = cachedData ? JSON.parse(cachedData) : {};
            console.log('获取缓存', thisBenchMark.value);

            // 获取缓存的页数并加载数据
            const cachedPage = localStorage.getItem('qaPage');
            page.value = cachedPage ? Number(cachedPage) : 1; // 默认从第1页开始
            fetchQAs();
        });

        return {
            thisBenchMark,
            isImage,
            isVideo,
            checkMedia,
            page,
            totalPage,
            currentQA,
            loadingBenchmarkCard,
            loadingQA,
            showOtherVersions,
            showMetaData,
            totalCount,
        };
    }
};
</script>

<style>
.content-section {
    color: white;
    display: flex;
    align-items: stretch;
    justify-content: center;
    border-radius: 8px;
    height: 100%;
    width: 100%;
    box-sizing: border-box;
    margin-top: 50px;
}

.benchmark-intro {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
}

.benchmark-intro h4 {
    margin-top: 0px;
}

.benchmark-intro h2 {
    margin-top: 0px;
    font-weight: bold;
}

.top-section {
    color: white;
    margin-top: 50px;
    height: 200px;
    align-items: stretch;
    justify-content: center;
    height: 100%;
    width: 100%;
    box-sizing: border-box;
}

.bottom-left-section {
    background: rgba(0, 0, 0, 0.1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    height: auto;
    width: 95%;
    margin-left: 50px;
}

.skeleton {
    margin: 20px;
    width: 95%;
}

.show-qa {
    margin: 20px;
    margin-bottom: 50px;
    width: 95%;
}

.qa-content {
    flex: 1;
    /* 左侧内容占满剩余空间 */
    margin-right: 16px;
    padding: 15px;
}

.qa {
    margin-bottom: 15px;
}

.switchMeta {
    margin-left: 15px;
}

.switchVariants {
    margin-left: 25px;
}

.meta-data {
    margin: 10px;
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10px);
    padding: 5px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.variants {
    margin: 10px;
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10px);
    padding: 5px;
    transition: box-shadow 0.5s ease-in-out;
}

.variants:hover {
    box-shadow: 0 0 5px 2px rgba(99, 226, 183, 0.8);
}

.no-variants {
    margin: 10px;
}

.qa-buttons {
    margin-top: 20px;
    margin-left: 10px;
}

.qa-media {
    flex-shrink: 0;
    /* 确保媒体部分不会被挤压 */
    width: 250px;
    height: 250px;
    /* 根据需要调整宽度 */
    /* background-color: white; */
    display: flex;
    justify-content: center;
    /* 水平居中 */
    align-items: center;
    /* 垂直居中 */
    margin-right: 25px;

}

.qa-media img,
.qa-media video {
    max-width: 250px;
    max-height: 250px;
    /* 确保媒体按比例缩放 */
    border-radius: 10px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    /* 添加动画过渡效果 */
}

.qa-media img:hover,
.qa-media video:hover {
    transform: scale(1.1);
    /* 悬浮时放大 */
    box-shadow: 0 0 5px 2px rgba(0, 0, 0, 0.8);
}

.pagination {
    margin-top: 20px;
    float: right;
}

.bottom-right-section {
    height: auto;
    display: flex;
    /* align-items: stretch; */
}

.benchmark-meta-card {
    display: flex;
    flex-direction: column;
    height: 90%;
    width: 90%;
    box-sizing: border-box;
    margin: 0;
    padding: 16px;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    border-radius: 10px;
    transition: box-shadow 0.5s ease-in-out;
    box-shadow: 0 0 0 rgba(99, 226, 183, 0);
    border: 1px solid rgba(255, 255, 255, 0.3);
    margin-bottom: 10px;
    /* 留出底部间隙 */
}

.benchmark-meta-card h3 {
    font-weight: bold;
}

.benchmark-meta-card:hover {
    box-shadow: 0 0 5px 2px rgba(99, 226, 183, 0.8);
}
</style>
