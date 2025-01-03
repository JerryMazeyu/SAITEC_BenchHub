<template>
    <div class="title">
        <h1>Paper Management</h1>
    </div>
    <div class="search-add">
        <div class="add-button">
            <el-button type="primary" @click="showAddPaper = true"><el-icon>
                    <Plus />
                </el-icon> Add Paper </el-button>
        </div>
        <div class="search">
            <el-input v-model="search" size="large" placeholder="Type to search name and author" />
        </div>
    </div>
    <div class="tableArea">
        <el-card shadow="always">
            <div class="table">
                <el-table stripe :data="filterTableData" style="width: 100%">
                    <el-table-column show-overflow-tooltip prop="name" label="Name" />
                    <el-table-column show-overflow-tooltip prop="author" label="Author" />
                    <el-table-column show-overflow-tooltip label="Class" :filters="classFilterData"
                        filter-placement="bottom-end" :filter-method="filterClass">
                        <template #default="props">
                            <el-tag>{{ props.row.class }}</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Detail" type="expand" width="80">
                        <template #default="props">
                            <h4>File Url</h4>
                            <div>{{ props.row.file_url }}}</div>
                            <h4>Journal</h4>
                            <div>{{ props.row.journal }}}</div>
                            <h4>Abstract</h4>
                            <div>{{ props.row.abstract }}}</div>
                        </template>
                    </el-table-column>
                    <el-table-column fixed="right" label="Operations" min-width="50">
                        <template #default="props">
                            <el-button link type="primary" size="small"
                                @click="readPaper(props.row.file_url)">Read</el-button>
                            <el-popconfirm title="Are you sure to delete this?">
                                <template #reference>
                                    <el-button link type="danger" size="small"
                                        @click="hanleDelete(props.row.id)">Delete</el-button>
                                </template>
                            </el-popconfirm>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </el-card>
    </div>
    <el-dialog v-model="showAddPaper" title="Add Paper" width="500" :before-close="handleClose">
        <span>This is a message</span>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="handleCloseAddPaper()">Cancel</el-button>
                <el-button type="primary" @click="handleAddPaper()">
                    Confirm
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { getAllPapers, deletePaper } from '../api/paper'
import { ElNotification } from 'element-plus'
export default {
    name: "Paper",
    setup() {
        const addPaperData = ref(
            {
                name: "",
                author: "",
                journal: "",
                abstract: "",
                class: null,
                file_url: "",
            }
        )
        const paperData = ref(
            [
                {
                    id: '123',
                    name: "探索语言模型在文本分类中的应用",
                    author: "fyf2007",
                    journal: "CSDN博客",
                    abstract: "论文首先分析了语言模型中幻觉问题的来源，即模型可能生成与现实不符或误导性的文本内容。这种现象源于语言模型在无监督学习中对大规模训练语料的统计模式进行建模，却缺乏事实校验和语义理解能力。随后，作者提出了一系列减少幻觉问题的技术与非技术手段",
                    class: "文本分类",
                    file_url: "https://arxiv.org/pdf/2305.16291",
                },
                {
                    id: '123',
                    name: "利用LLMs解决信息抽取任务｜综述",
                    author: "养生的控制人",
                    journal: "知乎专栏",
                    abstract: "论文首先分析了语言模型中幻觉问题的来源，即模型可能生成与现实不符或误导性的文本内容。这种现象源于语言模型在无监督学习中对大规模训练语料的统计模式进行建模，却缺乏事实校验和语义理解能力。随后，作者提出了一系列减少幻觉问题的技术与非技术手段",
                    class: "信息抽取",
                    file_url: "https://arxiv.org/pdf/2305.16291",
                },
                {
                    id: '123',
                    name: "大模型推理最新论文及源码合集，涵盖多模态推理、逻辑推理",
                    author: "weixin_42645636",
                    journal: "CSDN博客",
                    abstract: '论文首先分析了语言模型中幻觉问题的来源，即模型可能生成与现实不符或误导性的文本内容。这种现象源于语言模型在无监督学习中对大规模训练语料的统计模式进行建模，却缺乏事实校验和语义理解能力。随后，作者提出了一系列减少幻觉问题的技术与非技术手段',
                    class: "数学推理",
                    file_url: "https://arxiv.org/pdf/2305.16291",
                }
            ]
        );
        const search = ref('')
        const showAddPaper = ref(false)
        const classFilterData = ref([])
        const filterClass = (value, row) => {
            return row.class === value
        }

        const filterTableData = computed(() =>
            paperData.value.filter((data) =>
                !search.value ||
                data.name.toLowerCase().includes(search.value.toLowerCase()) ||
                data.author.toLowerCase().includes(search.value.toLowerCase())
            )
        );
        const readPaper = (fileUrl) => {
            // 创建一个隐藏的 <a> 标签
            const link = document.createElement('a');
            link.href = fileUrl; // 设置文件地址
            link.download = ''; // 设置文件名，可以设置具体名称，比如 `filename.pdf`
            link.target = '_blank'; // 兼容某些浏览器的跨域文件下载
            document.body.appendChild(link);
            link.click(); // 触发点击事件
            document.body.removeChild(link); // 下载完成后移除元素
        }
        const hanleDelete = (id) => {
            deletePaper(id).then(res => {
                ElNotification({
                    title: 'Success',
                    message: 'Delete successfully.',
                    type: 'success',
                })
            })
        }
        const handleCloseAddPaper = () => {
            addPaperData.value = {
                name: "",
                author: "",
                journal: "",
                abstract: "",
                class: null,
                file_url: "",
            }
            showAddPaper.value=false
        }
        const handleAddPaper=()=>{
            
        }
        onMounted(() => {
            // 获取到paper数据paperData.value

            filterTableData.value = paperData.value
            classFilterData.value = paperData.value.map(item => ({
                text: item.class,
                value: item.class,
            }));
        });
        return {
            paperData,
            filterClass,
            classFilterData,
            search,
            filterTableData,
            readPaper,
            hanleDelete,
            showAddPaper,
            addPaperData
        }
    }
};
</script>

<style>
.search-add {
    margin-top: 40px;
    display: flex;
    justify-content: space-between;
    /* 子组件一左一右 */
}

.search {
    width: 30%;
}

.tableArea {
    margin-top: 10px;
}

.table {
    margin: 10px;
}
</style>