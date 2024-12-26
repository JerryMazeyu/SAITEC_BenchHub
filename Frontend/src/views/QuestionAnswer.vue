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
                <n-data-table :bordered="false" :columns="columns" :data="tableData" :pagination="pagination" />
            </div>
        </n-grid-item>

        <!-- 下半部分右侧 -->
        <n-grid-item :span="3">
            <div class="content-section bottom-right-section">
                <n-card :bordered="false" class="benchmark-meta-card">
                    <n-h3>Dataset Information</n-h3>
                    <n-h5><n-text type="success">Uploader
                            <n-icon>
                                <Accessibility16Regular />
                            </n-icon></n-text>
                    </n-h5>
                    <n-h5><n-text type="success">Total Number
                            <n-icon>
                                <NumberRow16Regular />
                            </n-icon>
                        </n-text></n-h5>
                    <n-h5><n-text type="success">Update Version
                            <n-icon>
                                <ArrowClockwise16Regular />
                            </n-icon>
                        </n-text></n-h5>
                    <n-h5><n-text type="success">Answer Mode
                            <n-icon>
                                <Apps20Regular />
                            </n-icon>
                        </n-text></n-h5>
                    <n-h5><n-text type="success">Date Note
                            <n-icon>
                                <CalendarRtl28Regular />
                            </n-icon>
                        </n-text></n-h5>
                </n-card>
            </div>
        </n-grid-item>
    </n-grid>
</template>

<script>
import { ref, onMounted, h } from 'vue';
import { NButton, useMessage } from 'naive-ui'
import { useRouter } from 'vue-router';
import { Accessibility16Regular, NumberRow16Regular, ArrowClockwise16Regular, Apps20Regular, CalendarRtl28Regular } from '@vicons/fluent'
function createColumns() {
    return [
        {
            title: 'Answer',
            key: 'answer'
        },
        {
            title: 'Question',
            key: 'question'
        },
        {
            title: 'File',
            key: 'file_url'
        },
        {
            title: 'Action',
            key: 'action',
            render(row) {
                return h(
                    NButton,
                    {
                        size: 'small',
                        onClick: () => download(row.file_url)
                    },
                    { default: () => 'Download' }
                )
            }
        }
    ]
}


export default {
    name: 'QuestionAnswer',
    components: {
        Accessibility16Regular,
        NumberRow16Regular,
        ArrowClockwise16Regular,
        Apps20Regular,
        CalendarRtl28Regular
    },
    setup() {
        const router = useRouter();
        const thisBenchMark = ref({});
        const tableData = ref([
            { answer: 'Answer 1', question: 'Question 1', file_url: 'file1.pdf' },
            { answer: 'Answer 2', question: 'Question 2', file_url: 'file2.pdf' },
            { answer: 'Answer 3', question: 'Question 3', file_url: 'file3.pdf' }
        ])
        const columns = createColumns()
        const pagination = ref(10)

        const download = () => {
            console.log("click download")
        }

        const rowClassName = () => {
            return 'custom-table'
        }
        onMounted(() => {
            const cachedData = localStorage.getItem('thisBenchMark');
            thisBenchMark.value = cachedData ? JSON.parse(cachedData) : {};
            console.log('获取缓存', thisBenchMark.value);
        });

        return {
            thisBenchMark,
            tableData,
            columns,
            pagination,
            download,
            rowClassName
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

.n-data-table {
    margin: 20px;
    margin-bottom: 50px;
    opacity: 0.9;
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
