<template>
  <div style="width: 100%; height: 100%">
    <!-- ECharts container -->
    <div ref="chartContainer" style="width: 100%; height: 100%;"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";

export default {
  name: "EvaluationChart",
  mounted() {
    // Initialize ECharts instance
    const chart = echarts.init(this.$refs.chartContainer);

    // Chart configuration
    const option = {
      title: {
        text: "Model Evaluation Results",
        textStyle: {
          color: "#ffffff", // Set font color to white
        },
      },
      tooltip: {
        trigger: "axis",
      },
      grid: {
        show: false, // Hide grid lines
      },
      xAxis: {
        type: "category",
        data: [
          "Visual Language Reasoning\n\n(GPT4o)",
          "Visual Entailment\n\n(GPT4o)",
          "Video Retrieval\n\n(GLM-4V-Plus)",
          "Audio-Visual QA\n\n(GLM-4V-Plus)",
          "Chart Reasoning\n\n(GPT4o)",
          "Static Image Classification\n\n(GPT4o)",
          "Visual-Spatial Relation\n\n(GPT4o)",
          "Image QA\n\n(GPT4o)",
          "Object Detection\n\n(GPT4o)",
        ],
        axisLine: {
          show: true, // Hide x-axis line
        },
        axisTick: {
          show: true, // Hide x-axis ticks
        },
        axisLabel: {
          show: true, // Hide x-axis labels
        },
      },
      yAxis: {
        type: "value",
        name: "Accuracy (%)",
        axisLine: {
          show: true, // Hide y-axis line
        },
        axisTick: {
          show: true, // Hide y-axis ticks
        },
        axisLabel: {
          show: true, // Hide y-axis labels
        },
        splitLine: {
          show: false, // Hide grid horizontal lines
        },
      },
      series: [
        {
          name: "Evaluation Results",
          type: "bar",
          data: [
            86.74, 83.79, 77.31, 80.89, 75.27, 84.5, 75.61, 90.06, 14.6,
          ],
          label: {
            show: true,
            position: "top",
            formatter: "{c}%",
            color:"#ffffff"
          },
          itemStyle: {
            color: (params) => {
              // Set color for Object Detection (#109dfa), others as #2e9475
              return params.dataIndex === 8 ? "#109dfa" : "#2e9475";
            },
          },
        },
      ],
    };

    // Render the chart
    chart.setOption(option);

    // Add responsive support
    window.addEventListener("resize", () => chart.resize());
  },
};
</script>

<style scoped>
/* Optional style adjustments */
</style>