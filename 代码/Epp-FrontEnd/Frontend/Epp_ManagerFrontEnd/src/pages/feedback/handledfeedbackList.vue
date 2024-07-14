<template>
  <a-card :bordered="false">
    <a-table :data-source="data" :columns="columns">
      <template slot="operation">
        <div>
          <span>
            <!-- <a @click="checkFeedback(record)" v-if="record.flag==0">回复</a>
            <a  v-else>已成功回复</a> -->
            <a-modal v-model="showDetail" title="举报审核" @ok="handleOk()" width="750px" :mask-closable="false"
            :mask="true" :maskStyle="{'opacity':'0.08','background':'#000000','animation':'none'}">
              <a-card :bordered="false" dis-hover>
                <a-row>内容：{{selectData.content}}</a-row>
                <br/>
                <a-row>举报人：{{selectData.user}}</a-row>
                <br/>
                <a-row>日期：{{selectData.date}}</a-row>
                <br/>
                <!-- <a-textarea v-model="reply"></a-textarea> -->
              </a-card>
            </a-modal>
          </span>
        </div>
      </template>
      <template #expandedRowRender="record">
        <p style="margin: 0">
          举报内容：{{ record.content }}
        </p>
        <br/>
        <div class="detail">
          <p style="margin: 0">
            评论人：{{record.comment.user.user_name}}
          </p>
          <p style="margin: 0">
            评论文章：{{record.comment.paper.title}}
          </p>
          <p style="margin: 0">
             评论内容：{{record.comment.content}}
          </p>
        </div>
      </template>
    </a-table>
  </a-card>
</template>

<script>
import {getReport,getFeedbackAll, replyFeedback} from "../../services/feedback";

const columns = [
  {
    title: "内容",
    dataIndex: "content",
    scopedSlots: { customRender: "content" },
    width: 100,

  },
  {
    title: "举报人",
    dataIndex: "user",
    scopedSlots: { customRender: "user" },
    width: 100
  },
  {
    title: "日期",
    dataIndex: "date",
    scopedSlots: { customRender: "date" },
    width: 100
  },
  // {
  //   title: "问题类型",
  //   dataIndex: "qtype",
  //   scopedSlots: { customRender: "qtype" },
  //   width: 150
  // },
  // {
  //   title: "发布时间",
  //   dataIndex: "datatime",
  //   scopedSlots: { customRender: "datatime" },
  //   width: 150
  // },
  // {
  //   title: "回复状态",
  //   dataIndex: "state",
  //   scopedSlots: { customRender: "state" },
  //   width: 150
  // },
  // {
  //   title: "操作",
  //   dataIndex: "operation",
  //   scopedSlots: { customRender: "operation" },
  //   width: 150,
  //   render: () => <a>反馈</a>,
  // }
];
const data = [];

export default {
  name: "feedbackList",
  inject: ['reload'],
  components: {},
  data() {
    return {
      data,
      columns,
      showDetail: false,
      reply: '',
      selectData: {},
    }
  },
  mounted() {
    this.init();
  },

  methods: {
    init: async function() {
      this.loadNeed();
    },
    loadNeed: function () {
      data.length = 0;
      getReport({mode:2}).then((res)=>{
        console.log(res);
        let d = res.data.reports;
        console.log(d);
        for (let i = 0; i < d.length; i++) {
          data.push({
            content: d[i].content,
            user: d[i].user.user_name,
            date: d[i].date,
            comment:d[i].comment
            // email: d[i].email,
            // sex: d[i].sex,
            // qtype: str,
            // description: d[i].description,
            // datatime: d[i].datatime,
            // flag: d[i].flag,
            // message: d[i].message,
            // state: s
          })
        }
      }).catch((error) => {
        console.log(error);
      })
    },
    handleOk() {
      console.log(this.selectData)
      this.showDetail = false;
      let params = {
        feedback_id: this.selectData.feedback_id,
        message: this.reply
      }
      console.log(params)
      replyFeedback(params, 'post').then((res) => {
        console.log("答复成功！")
      }).catch((error) => {
        console.log(error)
      })
      this.reload();
    },
    checkFeedback(record) {
      console.log(record)
      console.log(record.name)
      this.showDetail = true;
      this.selectData = record;
    },
  }
}
</script>

<style scoped>
.highlight {
  background-color: rgb(255, 192, 105);
  padding: 0px;
}
.editable-row-operations a {
  margin-right: 8px;
}
.a-modal-mask {
  background-color: rgba(0,0,0,0.5); /* 将遮罩层的背景色修改为半透明的黑色 */
}
</style>
