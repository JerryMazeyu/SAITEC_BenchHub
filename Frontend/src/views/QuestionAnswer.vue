<template>
    <n-grid :x-gap="8" :y-gap="8" cols="12">
        <!-- 上半部分 -->
        <n-grid-item :span="12">
            <div class="top-section">
                <div class="benchmark-intro" v-if="thisBenchMark.name">
                    <n-h2>{{ thisBenchMark.name }}</n-h2>
                    <n-h4>{{ thisBenchMark.description }}</n-h4>
                    <n-flex justify="center">
                        <n-tag size="large" type="success" v-for="row in thisBenchMark.tag" :key="row">{{ row }}</n-tag>
                    </n-flex>
                </div>
            </div>
        </n-grid-item>

        <!-- 下半部分左侧 -->
        <n-grid-item :span="9">
            <div class="content-section bottom-left-section">
                <div class="show-qa">
                    <n-skeleton v-if="loadingQA" v-for="n in 10" class="skeleton" :sharp="false" size="large" />
                    <n-list hoverable clickable v-else>
                        <n-list-item v-for="(row, index) in currentQA" :key="index">
                            <!-- 左侧内容 -->
                            <n-thing>
                                <div class="qa-content">
                                    <div class="qa">
                                        <n-text type="success">Question:</n-text>{{ row.question }}
                                    </div>
                                    <div class="qa">
                                        <n-text type="success">Answer:</n-text>{{ row.answer }}
                                    </div>
                                    <div class="qa">
                                        <n-text type="success">Check Variants:</n-text>
                                        <n-switch class="checkVariants" v-model:value="showVariantsArray[index]">
                                        </n-switch>
                                        <span></span>
                                        <n-collapse-transition :show="showVariantsArray[index]">
                                            <div class="variants" v-for="(variant, index) in row.variants">
                                                <div><n-text type="success">Question:</n-text>{{ variant.answer }}</div>
                                                <div><n-text type="success">Answer:</n-text>{{ variant.question }}</div>
                                            </div>
                                        </n-collapse-transition>
                                    </div>
                                    <div class="qa-buttons">
                                        <n-flex>
                                            <n-button strong secondary type="primary" @click="download(row.file_url)">
                                                Download File
                                            </n-button>
                                            <!-- 还可以继续添加其他按钮 -->
                                        </n-flex>
                                    </div>
                                </div>
                            </n-thing>

                            <!-- 右侧媒体 -->
                            <template #suffix>
                                <div class="qa-media">
                                    <template v-if="isImage(row.file_url)">
                                        <img :src="row.file_url" alt="Image Preview" />
                                    </template>
                                    <template v-else-if="isVideo(row.file_url)">
                                        <video :key="scope.row.file_url" controls>
                                            <source :src="row.file_url" type="video/mp4" />
                                            Your browser does not support the video tag.
                                        </video>
                                    </template>
                                    <template v-else>
                                        <n-alert type="default">
                                            <template #icon>
                                                <n-icon>
                                                    <MdFolderOpen />
                                                </n-icon>
                                            </template>
                                            No Media File
                                        </n-alert>
                                    </template>
                                </div>
                            </template>
                        </n-list-item>
                    </n-list>
                    <n-pagination class="pagination" v-model:page="page" :page-count="totalPage" size="large"
                        show-quick-jumper />
                </div>
            </div>
        </n-grid-item>

        <!-- 下半部分右侧 -->
        <n-grid-item :span="3">
            <div class="content-section bottom-right-section">
                <n-card :bordered="false" class="benchmark-meta-card">
                    <n-spin :show="loadingBenchmarkCard">
                        <n-h3>Dataset Information</n-h3>
                        <n-h5><n-text type="success">Uploader
                                <n-icon>
                                    <Accessibility16Regular />
                                </n-icon></n-text>
                        </n-h5>
                        {{ datasetInfo.uploader }}
                        <n-h5><n-text type="success">Total Number
                                <n-icon>
                                    <NumberRow16Regular />
                                </n-icon>
                            </n-text></n-h5>
                        {{ datasetInfo.total_number }}
                        <n-h5><n-text type="success">Update Version
                                <n-icon>
                                    <ArrowClockwise16Regular />
                                </n-icon>
                            </n-text></n-h5>
                        <n-flex vertical>
                            <n-alert v-for="(row, index) in datasetInfo.update_version" type="info">
                                Version: {{ row.version }}
                                <br>
                                Update Time: {{ row.update_time }}
                            </n-alert>
                        </n-flex>
                        <n-h5><n-text type="success">Answer Mode
                                <n-icon>
                                    <Apps20Regular />
                                </n-icon>
                            </n-text></n-h5>
                        {{ datasetInfo.answer_mode }}
                        <n-h5><n-text type="success">Date Note
                                <n-icon>
                                    <CalendarRtl28Regular />
                                </n-icon>
                            </n-text></n-h5>
                        {{ datasetInfo.date_note }}
                    </n-spin>
                </n-card>
            </div>
        </n-grid-item>
    </n-grid>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useMessage } from 'naive-ui'
import { MdFolderOpen } from '@vicons/ionicons4'
import { Accessibility16Regular, NumberRow16Regular, ArrowClockwise16Regular, Apps20Regular, CalendarRtl28Regular } from '@vicons/fluent'
import { download } from 'naive-ui/es/_utils';
// import {getQAs,getMeta} from '@/api/questionAnswer'

export default {
    name: 'QuestionAnswer',
    components: {
        Accessibility16Regular,
        NumberRow16Regular,
        ArrowClockwise16Regular,
        Apps20Regular,
        CalendarRtl28Regular,
        MdFolderOpen
    },
    setup() {
        const totalQA = ref([
            {
                answer: '古代“十八般武艺”中的“白打”是指徒手搏击的技艺，也可以理解为空手格斗或者自由搏击。这个词语体现了古代武艺中对身体技巧和力量的重视，即使不使用任何武器，也能凭借自身的武艺进行有效的自卫和攻击。在古代，这种技能是非常受尊敬的，因为它体现了武者的身体素质和实战能力。',
                question: '我国古代“十八般武艺”中第十八是“白打”意思是什么？',
                file_url: 'https://pic.superbed.cc/item/67580169fa9f77b4dc007d03.jpg',
                variants: [
                    { question: '我国古代“十八般武艺”中第十八是“白打”意思是什么？', answer: '古代“十八般武艺”中的“白打”是指徒手搏击的技艺，也可以理解为空手格斗或者自由搏击。这个词语体现了古代武艺中对身体技巧和力量的重视，即使不使用任何武器，也能凭借自身的武艺进行有效的自卫和攻击。在古代，这种技能是非常受尊敬的，因为它体现了武者的身体素质和实战能力。' },
                    { question: '我国古代“十八般武艺”中第十八是“白打”意思是什么？', answer: '古代“十八般武艺”中的“白打”是指徒手搏击的技艺，也可以理解为空手格斗或者自由搏击。这个词语体现了古代武艺中对身体技巧和力量的重视，即使不使用任何武器，也能凭借自身的武艺进行有效的自卫和攻击。在古代，这种技能是非常受尊敬的，因为它体现了武者的身体素质和实战能力。' }
                ]
            },
            {
                answer: 'Answer 2',
                question: 'Question 2',
                file_url: 'https://pic.superbed.cc/item/67595444fa9f77b4dc12837b.jpg',
                variants: [
                    { question: '我国古代“十八般武艺”中第十八是“白打”意思是什么？', answer: '古代“十八般武艺”中的“白打”是指徒手搏击的技艺，也可以理解为空手格斗或者自由搏击。这个词语体现了古代武艺中对身体技巧和力量的重视，即使不使用任何武器，也能凭借自身的武艺进行有效的自卫和攻击。在古代，这种技能是非常受尊敬的，因为它体现了武者的身体素质和实战能力。' },
                    { question: '我国古代“十八般武艺”中第十八是“白打”意思是什么？', answer: '古代“十八般武艺”中的“白打”是指徒手搏击的技艺，也可以理解为空手格斗或者自由搏击。这个词语体现了古代武艺中对身体技巧和力量的重视，即使不使用任何武器，也能凭借自身的武艺进行有效的自卫和攻击。在古代，这种技能是非常受尊敬的，因为它体现了武者的身体素质和实战能力。' }
                ]
            },
            {
                answer: 'Answer 3',
                question: 'Question 3',
                file_url: 'https://pic.superbed.cc/item/67595444fa9f77b4dc12837b.jpg',
                variants: [
                    { question: '我国古代“十八般武艺”中第十八是“白打”意思是什么？', answer: '古代“十八般武艺”中的“白打”是指徒手搏击的技艺，也可以理解为空手格斗或者自由搏击。这个词语体现了古代武艺中对身体技巧和力量的重视，即使不使用任何武器，也能凭借自身的武艺进行有效的自卫和攻击。在古代，这种技能是非常受尊敬的，因为它体现了武者的身体素质和实战能力。' },
                    { question: '我国古代“十八般武艺”中第十八是“白打”意思是什么？', answer: '古代“十八般武艺”中的“白打”是指徒手搏击的技艺，也可以理解为空手格斗或者自由搏击。这个词语体现了古代武艺中对身体技巧和力量的重视，即使不使用任何武器，也能凭借自身的武艺进行有效的自卫和攻击。在古代，这种技能是非常受尊敬的，因为它体现了武者的身体素质和实战能力。' }
                ]
            },
        ]);

        const datasetInfo = ref({ uploader: 'Richard', total_number: 125, answer_mode: 'Open Questions', date_note: '2024-12-27', update_version: [{ version: "1.0", update_time: "2024-9-11" }, { version: "2.0", update_time: "2024-10-11" }] });

        const thisBenchMark = ref({});

        const page = ref(1)

        const loadingBenchmarkCard = ref(false)

        const loadingQA = ref(false)

        const showVariantsArray = ref(Array(10).fill(false));

        const message = useMessage()

        const download = (fileUrl) => {
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

        const currentQA = computed(() => {
            const start = (page.value - 1) * 10;
            const end = page.value * 10;
            showVariantsArray.value = Array(10).fill(false);
            return totalQA.value.slice(start, end);
        });

        const totalPage = computed(() => {
            return Math.ceil(totalQA.value.length / 10);
        });

        onMounted(() => {
            const cachedData = localStorage.getItem('thisBenchMark');
            thisBenchMark.value = cachedData ? JSON.parse(cachedData) : {};
            console.log('获取缓存', thisBenchMark.value);
            // // 同步获取数据集meta和数据集qa
            // // 获取数据集meta
            // loadingBenchmarkCard.value=true
            // getMeta(thisBenchMark.value.id).then(res=>{
            //     datasetInfo.value=res.data
                    // setTimeout(() => {
                    // loadingBenchmarkCard.value = false;
                    // }, 500);

            // })
            // // 获取数据集qa
            // loadingQA.value=true
            // getQAs(hisBenchMark.value.id).then(res=>{
            //     totalQA.value=res.data
            //     loadingQA.value=false
                    // setTimeout(() => {
                    // loadingQA.value = false;
                    // }, 500);
            // })
        });

        return {
            thisBenchMark,
            isImage,
            isVideo,
            download,
            totalQA,
            page,
            totalPage,
            currentQA,
            datasetInfo,
            loadingBenchmarkCard,
            loadingQA,
            showVariantsArray
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
    margin-top: 70px;
    height: 200px;
    align-items: stretch;
    justify-content: center;
    height: 100%;
    width: 100%;
    box-sizing: border-box;
}

.bottom-left-section {
    background: rgba(0, 0, 0, 0.1);
    height: auto;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    width: 95%;
    margin-left: 50px;
}

.skeleton {
    margin: 20px;
    height: 300px;
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

}

.qa {
    margin-bottom: 10px;
}

.checkVariants {
    margin-left: 15px;
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

.qa-buttons {
    margin-top: 20px;
}

.qa-media {
    flex-shrink: 0;
    /* 确保媒体部分不会被挤压 */
    width: 200px;
    height: 200px;
    /* 根据需要调整宽度 */
    /* background-color: white; */
    display: flex;
    justify-content: center;
    /* 水平居中 */
    align-items: center;
    /* 垂直居中 */
}

.qa-media img,
.qa-media video {
    max-width: 100%;
    max-height: 100%;
    /* 确保媒体按比例缩放 */
    border-radius: 8px;
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
