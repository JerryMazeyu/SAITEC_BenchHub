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
    <el-dialog v-model="showAddPaper" title="Add Paper" width="600" :before-close="handleCloseAddPaper">
        <el-form :model="addPaperData" :ref="addPaperDataRef" :rules="rules" label-width="120px">
            <el-form-item label-position="left" prop="name" label="Paper Name">
                <el-input v-model="addPaperData.name" placeholder="Enter paper name"></el-input>
            </el-form-item>
            <el-form-item label-position="left" prop="author" label="Paper Author">
                <el-input v-model="addPaperData.author" placeholder="Enter paper author"></el-input>
            </el-form-item>
            <el-form-item label-position="left" prop="journal" label="Paper Journal">
                <el-input v-model="addPaperData.journal" placeholder="Enter paper journal"></el-input>
            </el-form-item>
            <el-form-item label-position="left" prop="journal" label="Paper file url">
                <el-input v-model="addPaperData.file_url" placeholder="Enter paper file url"></el-input>
            </el-form-item>
            <el-form-item label-position="left" prop="class" label="Paper class">
                <el-select v-model="addPaperData.class" clearable placeholder="Choose paper class">
                    <el-option v-for="item in classOptions" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
            </el-form-item>
            <el-form-item label-position="left" prop="abstract" label="Paper abstract">
                <el-input :autosize="{ minRows: 3, maxRows: 7 }" type="textarea" height="300"
                    v-model="addPaperData.abstract" placeholder="Enter paper abstract"></el-input>
            </el-form-item>
        </el-form>
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
import { ref, onMounted, computed, reactive } from 'vue';
import { getAllPapers, deletePaper , addPaper, getAllBenchMarks } from '../api/paper'
import { ElNotification } from 'element-plus'
export default {
    name: "Paper",
    setup() {
        const addPaperData = reactive(
            {
                name: "",
                author: "",
                journal: "",
                abstract: "",
                class: "",
                file_url: "",
            }
        )
        const addPaperDataRef = ref(null)

        const rules = {
            name: [
                { required: true, message: "Please enter paper name", trigger: "blur" },
            ],
            author: [
                { required: true, message: "Please enter paper author", trigger: "blur" },
            ],
            journal: [
                { required: true, message: "Please enter paper journal", trigger: "blur" },
            ],
            abstract: [
                { required: true, message: "Please enter paper abstract", trigger: "blur" },
            ],
            class: [
                { required: true, message: "Please choose paper class", trigger: "blur" },
            ],
            file_url: [
                { required: true, message: "Please enter paper file url", trigger: "blur" },
            ],
        };

        const benchmarks = ref(
            [
                { id: '1', name: "文本分类", description: "将文本划分为不同的类别或标签。可以应用于垃圾邮件过滤、情感分析、新闻分类等应用场景", class: "单模态" },
                { id: '2', name: "信息抽取", description: "指模型能够根据文本内容，完成内容、实体、事件、属性、关系等信息的抽取", class: "单模态" },
                { id: '3', name: "数学推理", description: "指理解和应用数学概念、原理来解决涉及数学运算问题的能力。如解析表达式、图形识别、公式推导等", class: "单模态" },
            ]
        )
        const classOptions = ref([])

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
                class: "",
                file_url: "",
            }
            showAddPaper.value = false
        }
        const handleAddPaper = () => {
            addPaperDataRef.value.validate((valid) => {
                if (valid) {
                    const paperAddData = addPaperData.value
                    addPaper(paperAddData).then(res => {
                        if (res.success) {
                            ElNotification({
                                title: 'Success',
                                message: 'Paper added successfull.',
                                type: 'success',
                            })
                            handleCloseAddPaper()
                        }
                    })
                }
                else {
                    ElNotification({
                        title: 'Error',
                        message: 'Validation failed.',
                        type: 'error',
                    })
                }
            })
        }
        onMounted(() => {
            // 获取到paper数据paperData.value
            // getAllPapers().then(res => {
            //     if (res.success) {
            //         paperData.value = res.data
            //         filterTableData.value = paperData.value
            //         classFilterData.value = paperData.value.map(item => ({
            //             text: item.class,
            //             value: item.class,
            //         }));
            //     }
            // })

            // 获取假数据paperData
            filterTableData.value = paperData.value
            classFilterData.value = paperData.value.map(item => ({
                text: item.class,
                value: item.class,
            }));

            //获取到benchmarks,将其映射到类别选项中
            // getAllBenchMarks().then(res => {
            //     if (res.success) {
            //         benchmarks.value = res.data
            //         classOptions.value = benchmarks.value.map(item => ({
            //             label: item.name,
            //             value: item.name,
            //         }));
            //     }
            // })

            // 获取benchmarks假数据
            classOptions.value = benchmarks.value.map(item => ({
                        label: item.name,
                        value: item.name,
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
            addPaperData,
            addPaperDataRef,
            classOptions,
            rules,
            handleCloseAddPaper,
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

.el-select__placeholder.is-transparent {
    visibility: visible !important;
    opacity: 1 !important;
}
</style>