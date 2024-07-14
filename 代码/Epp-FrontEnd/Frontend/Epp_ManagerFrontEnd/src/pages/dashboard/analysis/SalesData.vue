<template>
  <div style="">
    <v-chart :forceFit="true" :height="height" :data="data" :scale="scale">
      <v-tooltip :showTitle="false" dataKey="item*percent" />
      <v-axis />
      <v-legend dataKey="item" position="right" :offsetX="-80" />
      <v-pie
        position="percent"
        color="item"
        :vStyle="pieStyle"
        :label="labelConfig"
      />
      <v-coord type="theta" :radius="0.75" :innerRadius="0.6" />
    </v-chart>
  </div>
</template>

<script>
import { gettags } from "@/services/dataSource";

const DataSet = require("@antv/data-set");

const sourceData = [];

const scale = [
  {
    dataKey: "percent",
    min: 0,
    formatter: ".0%",
  },
];

const dv = new DataSet.View().source(sourceData);
dv.transform({
  type: "percent",
  field: "count",
  dimension: "item",
  as: "percent",
});
const data = dv.rows;
export default {
  name: "SalesData",
  data() {
    return {
      data,
      scale,
      height: 375,
      pieStyle: {
        stroke: "#fff",
        lineWidth: 1,
      },
      labelConfig: [
        "percent",
        {
          formatter: (val, item) => {
            return item.point.item + ": " + val;
          },
        },
      ],
    };
  },
  created() {
    gettags().then((res) => {
      // console.log(res);
      for (let i = 0; i < 8; i++) {
        // console.log(res.data[i].name);
        // console.log(res.data[i].count);
        sourceData.push({
          item: res.data[i].name,
          count: res.data[i].count,
        });
      }
      const dv = new DataSet.View().source(sourceData);
      dv.transform({
        type: "percent",
        field: "count",
        dimension: "item",
        as: "percent",
      });
      this.data = dv.rows;
    });
  },
  methods: {
    init: async function() {
      this.gettags();
    },
  },
};
</script>

<style scoped></style>
