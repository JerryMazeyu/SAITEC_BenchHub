<template>
    <div class="title">
        <h1>QA Management</h1>
    </div>
    <div class="filter-search">
        <el-select class="filter-select" v-model="classValue" placeholder="Please Select The Data Category">
            <el-option v-for="item in classOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-select class="filter-select" disabled v-if="classValue === null" placeholder="Please Select The Benchmark">
        </el-select>
        <el-select class="filter-select" v-else v-model="benchmarkValue" placeholder="Please Select The Benchmark">
            <el-option v-for="item in benchmarkOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-button type="primary" @click="handleFilter()">
            <el-icon>
                <Filter />
            </el-icon>
            Retrieve Data
        </el-button>
        <el-button type="warning" @click="reset()">
            <el-icon>
                <RefreshRight />
            </el-icon>
            Reset
        </el-button>
    </div>
    <div class="update-button">
        <el-button size="large" type="success"> <el-icon>
                <Refresh />
            </el-icon>Sync Data</el-button>
    </div>
    <div class="table-area">
        <el-card shadow="always">
            <div class="table">
                <el-table stripe :data="currentPapers" style="width: 100%">

                </el-table>
            </div>
        </el-card>
    </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { ElNotification } from 'element-plus'

export default {
    name: "QA",
    setup() {
        const classOptions = ref([
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
        ])
        const classValue = ref(0)
        const benchmarkOptions = computed(() => {
            benchmarkValue.value = null
            let filteredDatasets = [];

            // 对benchmarks按照单模态,多模态和安全性进行过滤并映射到选项中
            if (classValue.value === 0) {
                filteredDatasets = benchmarks.value;
            } else if (classValue.value === 1) {
                filteredDatasets = benchmarks.value.filter(item => item.class.includes("单模态"));
            }
            else if (classValue.value === 2) {
                filteredDatasets = benchmarks.value.filter(item => item.class.includes("多模态"));
            } else if (classValue.value === 3) {
                filteredDatasets = benchmarks.value.filter(item => item.class.includes("安全性"));
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
        })
        const benchmarkValue = ref(null)
        const benchmarks = ref(
            [
                { id: '1', name: "文本分类", description: "将文本划分为不同的类别或标签。可以应用于垃圾邮件过滤、情感分析、新闻分类等应用场景", class: "单模态" },
                { id: '2', name: "信息抽取", description: "指模型能够根据文本内容，完成内容、实体、事件、属性、关系等信息的抽取", class: "单模态" },
                { id: '3', name: "数学推理", description: "指理解和应用数学概念、原理来解决涉及数学运算问题的能力。如解析表达式、图形识别、公式推导等", class: "单模态" },
            ]
        )
        const filtreredQA = ref([])
        const handleFilter = () => {
            if (benchmarkValue.value === null) {
                ElNotification({
                    title: 'Warning',
                    message: 'Please select benchmark.',
                    type: 'warning',
                })
                return
            }
        }
        const reset = () => {
            benchmarkValue.value = null
            classValue.value = 0
            filtreredQA.value = []
            ElNotification({
                title: 'Success',
                message: 'Reset.',
                type: 'success',
            })

        }
        onMounted(() => {
            // 获取到benchmarks,在computed中执行benchmarks到benchmarkOpions的映射
        })

        return {
            classOptions,
            classValue,
            benchmarkOptions,
            benchmarkValue,
            handleFilter,
            reset,
            filtreredQA
        }
    }
}
</script>

<style>
.filter-search {
    margin-top: 40px;
    display: flex;
    justify-content: center;
}

.filter-select {
    width: 33% !important;
    margin-right: 20px;
}

.update-button {
    margin-top: 30px;
    display: flex
}

.table-area {
    margin-top: 10px;
}

.table {
    margin: 10px;
}
</style>