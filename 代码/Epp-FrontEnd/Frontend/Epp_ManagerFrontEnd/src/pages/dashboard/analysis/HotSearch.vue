<template>
  <div class="hot-search">
    
    <a-table
      :dataSource="searchData"
      :columns="tableColumns"
      :pagination="{style: { marginBottom: 0 }}"
      size="small"
      rowKey="index"
    >
      <a href="javascript:0" slot="keyword" slot-scope="text">{{text}}</a>
      <span slot="rang" slot-scope="text">{{text}} %<a-icon type="caret-up" /> </span>
    </a-table>
  </div>
</template>

<script>
// import MiniArea from '../../../components/chart/MiniArea'
import {getkeywords} from "@/services/dataSource";
const searchData = []

const columns = [
  {
    dataIndex: 'index',
    key: 'rank'
  },
  {
    dataIndex: 'keyword',
    key: 'keyword',
    scopedSlots: {customRender: 'keyword'}
  },
  {
    dataIndex: 'count',
    key: 'count',
  },
]

export default {
  name: 'HotSearch',
  i18n: require('./i18n-search'),
  data () {
    return {
      searchData,
      columns
    }
  },
  created() {
    this.init();
  },

  methods: {
    init: async function() {
      this.loadData();
    },

    loadData: function() {
      this.loading = true;
      searchData.length=0;
      getkeywords()
        .then((res) => {
          // console.log(res)
          for (let i = 0; i < 8; i++) {
            searchData.push({
              index: i + 1,
              keyword: res.data[i].name,
              count: res.data[i].count,
              status: Math.floor((Math.random() * 10) % 2),
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  computed: {
    tableColumns() {
      let columns = this.columns
      return columns.map(item => {
       item.title = this.$t(item.key)
        return item
      })
    }
  }
}
</script>

<style lang="less" scoped>
  .num-info{
    .title{
      color: @text-color-second;
      font-size: 14px;
      height: 22px;
      line-height: 22px;
      overflow: hidden;
      text-overflow: ellipsis;
      word-break: break-all;
      white-space: nowrap;
    }
    .value{
      .total{
        color: @title-color;
        display: inline-block;
        line-height: 32px;
        height: 32px;
        font-size: 24px;
        margin-right: 32px;
      }
      .subtotal{
        color: @text-color-second;
        font-size: 16px;
        vertical-align: top;
        margin-right: 0;
        i{
          font-size: 12px;
          color: red;
          transform: scale(.82);
          margin-left: 4px;
        }
      }
    }
  }
</style>
