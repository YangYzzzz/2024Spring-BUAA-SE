<template>
  <a-card :bordered="false">
    <a-table :data-source="data" :columns="columns" :showExpandColumn="true">
      <template
          #customFilterDropdown="{ setSelectedKeys, selectedKeys, confirm, clearFilters, column }"
      >
      </template>
      <template slot="operation" slot-scope="text, record">
        <div>
          <a-popconfirm
              v-if="data.length"
              title="Sure to delete?"
              @confirm="() => onDeleteNeed(record.need_id)"
          >
            <a href="javascript:0;">Delete</a>
          </a-popconfirm>
        </div>
      </template>
      <template #expandedRowRender="record,index" class="ant-table-thead">
        <ChildForm :OrderColumns="OrderColumns" :OrderData="OrderData[index] "></ChildForm>
      </template>
    </a-table>
  </a-card>
</template>

<script>
import {getNeedAll, getOrder, deleteOrder, deleteNeed} from "../../services/needOrder";
import ChildForm from "./ChildForm";
const columns = [
  {
    title: "需求ID",
    dataIndex: "need_id",
    scopedSlots: { customRender: "need_id" },
    width: 80,
  },
  {
    title: "发布用户",
    dataIndex: "enterprise_name",
    scopedSlots: { customRender: "enterprise_name" },
    width: 150,
    customFilterDropdown: true,
    onFilter: (value, record) =>
        record.enterprise_name.toString().toLowerCase().includes(value.toLowerCase()),

  },
  {
    title: "需求名称",
    dataIndex: "title",
    scopedSlots: { customRender: "title" },
    width: 230
  },
  {
    title: "开始时间",
    dataIndex: "start_time",
    scopedSlots: { customRender: "start_time" },
    width: 150
  },
  {
    title: "结束时间",
    dataIndex: "end_time",
    scopedSlots: { customRender: "end_time" },
    width: 150
  },
  {
    title: "关键词",
    dataIndex: "key_word",
    scopedSlots: { customRender: "key_word" },
    width: 120
  },
  {
    title: "领域",
    dataIndex: "field",
    scopedSlots: { customRender: "field" },
    width: 100
  },
  {
    title: "需求状态",
    dataIndex: "state",
    scopedSlots: { customRender: "state" },
    width: 100
  },
  {
    title: "操作",
    dataIndex: "operation",
    width: 80,
    scopedSlots: { customRender: "operation" },
  },
];

const data = [];

const OrderColumns =  [
  { title: '订单ID', dataIndex: 'order_id', key: 'order_id', width: 100, className:'ant-table-thead'},
  { title: '专家ID', dataIndex: 'expert_id', key: 'expert_id', width: 100},
  { title: '专家姓名', dataIndex: 'expert_name', key: 'expert_name', width: 100},
  { title: '专家电话', dataIndex: 'phone', key: 'phone', width: 140},
  { title: '创建时间', dataIndex: 'create_time', key: 'create_time', width: 200},
  { title: '结束时间', dataIndex: 'end_time', key: 'end_time', width: 200},
  { title: '进行状态', dataIndex: 'state', key:'state', width: 100},
  {
    title: '操作',
    dataIndex: 'operation',
    key: 'operation',
    width: 80,
    scopedSlots: { customRender: "operation" },
  },
];

const OrderData = [];

export default {
  name: "NeedForm",
  inject: ['reload'],
  components: {
    ChildForm
  },
  data() {
    this.cacheData = data.map((item) => ({ ...item }));
    return {
      type:"",
      type1:0,
      data,
      columns,
      editingKey: "",
      OrderData,
      OrderColumns,
    };
  },

  mounted() {
    this.init();
  },

  methods: {
    init: async function() {
      this.loadNeed();
    },

    loadNeed: function() {
      this.loading = true;
      data.length = 0;
      OrderData.length = 0;
      getNeedAll().then((res) => {
        console.log(res);
        for (let i = 0; i < res.data.data.length; i++) {
          getOrder(res.data.data[i].need_id, "get").then((res2) => {
            data.push({
              need_id: res.data.data[i].need_id,
              enterprise_name: res.data.data[i].enterprise_name,
              title: res.data.data[i].title,
              description: res.data.data[i].description,
              start_time: res.data.data[i].start_time,
              money: res.data.data[i].money,
              key_word: res.data.data[i].key_word,
              end_time: res.data.data[i].end_time,
              field: res.data.data[i].field,
              state: res.data.data[i].state,
              emergency: res.data.data[i].emergency,
              predict: res.data.data[i].predict,
              real: res.data.data[i].real,
              order: res2.data.data
            });
            OrderData.push(res2.data.data);
          })
        }
        console.log(data);
        this.loading = false;
      }).catch((error) => {
        console.log(error);
      })
    },
    handleChange() {
      this.loadNeed();
    },
    rowClassName(record, index) {
      console.log("!!!!!!!!!!!!")
      return "test";
    },
    onDeleteNeed(id) {
      deleteNeed(id, 'delete').then((res) => {
        console.log(res)
      }).catch((error) => {
        console.log(error);
      })
      this.reload();
    },

  },
};
</script>

<style scoped>
.highlight {
  background-color: rgb(255, 192, 105);
  padding: 0px;
}
.editable-row-operations a {
  margin-right: 8px;
}




</style>
