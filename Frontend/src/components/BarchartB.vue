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
            "Information Extraction",
            "Causal Reasoning",
            "Knowledge & Common Sense",
            "Long Text Comprehension",
            "Professional Knowledge",
            "Common Sense Reasoning",
            "Mathematical Reasoning",
            "Text QA",
            "Logical Reasoning",
            "Text Classification",
            "Compliance",
            "Fairness",
            "Hallucination",
            "Robustness",
          ],
          axisLine: {
            show: true, // Show x-axis line
          },
          axisTick: {
            show: true, // Show x-axis ticks
          },
          axisLabel: {
            show: true, // Show x-axis labels
          },
        },
        yAxis: {
          type: "value",
          name: "Accuracy (%)",
          axisLine: {
            show: true, // Show y-axis line
          },
          axisTick: {
            show: true, // Hide y-axis ticks
          },
          axisLabel: {
            show: true, // Show y-axis labels
          },
          splitLine: {
            show: false, // Hide grid horizontal lines
          },
        },
        series: [
          {
            name: "Llama3.1-70b",
            type: "bar",
            data: [
              60.32, 72.00, 79.13, 68.62, 68.22, 74.43, 66.28, 67.45, 66.94, 75.46, 82.42, 82.00, 42.89, 80.00,
            ],
            itemStyle: {
              color: "#2e9475",
            },
          },
          {
            name: "GPT-4o",
            type: "bar",
            data: [
              73.46, 82.67, 83.04, 78.19, 78.85, 81.76, 65.08, 77.14, 76.46, 81.43, 79.12, 78.00, 78.89, 79.44,
            ],
            itemStyle: {
              color: "#5271ff",
            },
          },
          {
            name: "Llama3.1-8b",
            type: "bar",
            data: [
              50.94, 50.67, 51.30, 47.34, 46.38, 50.93, 37.74, 47.19, 46.50, 61.39, 69.23, 64.00, 38.67, 70.00,
            ],
            itemStyle: {
              color: "#109dfa",
            },
          },
          {
            name: "Qwen-Max-Latest",
            type: "bar",
            data: [
              80.97, 82.67, 88.70, 88.30, 86.89, 87.77, 76.69, 84.97, 84.47, 82.86, 82.42, 92.00, 76.89, 80.00,
            ],
            itemStyle: {
              color: "#8194e2",
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
  