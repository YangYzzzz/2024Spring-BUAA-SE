<template>
  <div>
  <p style="margin: 0;background-color: lightgoldenrodyellow;font-size: 14px">相关订单：</p>
  <a-table :columns="OrderColumns" :data-source="OrderData"
           :pagination="false" style="background-color: lightgoldenrodyellow">
    <template slot="operation" slot-scope="text, record">
      <div>
        <a-popconfirm
            v-if="OrderData.length"
            title="Sure to delete?"
            @confirm="() => onDeleteOrder(record.order_id)"
        >
          <a href="javascript:0;">Delete</a>
        </a-popconfirm>
      </div>
    </template>
  </a-table>
  </div>
</template>

<script>
import {deleteNeed, deleteOrder} from "../../services/needOrder";

export default {
  name: "ChildForm",
  inject: ['reload'],
  props:{
    OrderColumns: {
      type: Array,
      default: ''
    },
    OrderData: {
      type: Array,
      default: ''
    },
    showExpandColumn: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    onDeleteOrder(id) {
      deleteOrder(id, 'delete').then((res) => {
        console.log(res)
      }).catch((error) => {
        console.log(error);
      })
      this.reload();
    },
  }
}
</script>

<style scoped>
/deep/ .ant-table-thead > tr > th{
  background-color: lightgoldenrodyellow !important;
}
</style>
