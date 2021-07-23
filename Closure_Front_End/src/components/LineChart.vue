

<script>
import { defineComponent } from "vue";
import { Line } from "vue3-chart-v2";

export default defineComponent({
  name: "MonthlyChart",
  extends: Line,
  // props: {
  //   chartData: {
  //     type: Object,
  //     required: true
  //   },
  //   chartOptions: {
  //     type: Object,
  //     required: false
  //   },
  // },
  mounted() {
    this.renderChart({
      labels: [0,1, 2, 3, 4, 5, 6, 7, 8],
      datasets: [
        {
          label: "total points",
          backgroundColor: "#999999",
          fill: false,
          data: [0,25, 56, 70, 80, 90, 105, 125, 134],
          xAxisId: "semester",
          options: {
            scales: {
              title:
              {
                display: true,
                text : 'semester',
              },
            },
          },
        },
      ],
    });
  },
});
</script>