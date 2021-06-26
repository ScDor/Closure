
<script>
import { defineComponent } from 'vue';
import { Pie } from 'vue3-chart-v2';

export default defineComponent({
  name: 'MonthlyChart',
  extends: Pie,
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart({
      labels: ['Must', 'Choose from list', 'Choice'],
      datasets: [
        {
          backgroundColor: ['#bc87d0','#fbaf5d','#f06eaa'],
          data: [70, 20, 40]
        }
      ]
    })
  }
})
</script>
