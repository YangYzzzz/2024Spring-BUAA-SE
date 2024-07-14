<template>
  <div class="bar">
    <h4>{{ title }}</h4>
    <div class="chart">
      <v-chart
        :force-fit="true"
        height="312"
        :data="data"
        :padding="[24, 0, 0, 0]"
      >
        <v-tooltip />
        <v-axis />
        <v-bar position="x*y" />
      </v-chart>
    </div>
  </div>
</template>

<script>
import { getvis } from "@/services/dataSource";
const data = [];

data.push({
  x: "1月",
  y: 30,
});
data.push({
  x: "2月",
  y: 71,
});

data.push({
  x: "3月",
  y: 67,
});
data.push({
  x: "4月",
  y: 130,
});
data.push({
  x: "5月",
  y: 239,
});
// for (let i = 6; i <= 12; i += 1) {
//   data.push({
//     x: `${i}月`,
//     y: 0
//   })
// }

const tooltip = [
  "x*y",
  (x, y) => ({
    name: x,
    value: y,
  }),
];

const scale = [
  {
    dataKey: "x",
    min: 2,
  },
  {
    dataKey: "y",
    title: "时间",
    min: 1,
    max: 22,
  },
];
export default {
  name: "Bar",
  props: ["title"],
  data() {
    return {
      data,
      scale,
      tooltip,
    };
  },
  created() {
    getvis().then((res) => {
      // console.log(res);

      data.push({
        x: '6月',
        y: res.data.totcount-537 < 0 ? 10 : res.data.totcount-537,
      });
    });
  },
};
</script>

<style scoped lang="less">
.bar {
  position: relative;
  .chart {
  }
}
</style>
