<template>
  <a-card :bordered="false">
    <a-table :data-source="data" :columns="columns">
      <template slot="operation" slot-scope="text, record">
        <div>
          <span>
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
      <template slot="action" slot-scope="text, record">
        <a-button type="primary" @click="handleProcess(record.id)">回复</a-button>
      </template>
      <template #expandedRowRender="record" class="ant-table-thead">
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
           <a-button type="danger" @click="deleteComment(record.comment.comment_id)">删除评论</a-button>
        </div>
      </template>
    </a-table>
    <a-modal
  v-model="showReplyModalVisible"
  title="举报信息回复"
  @ok="handleReplyOk"
  @cancel="handleReplyCancel"
>
  <a-textarea
    v-model="replyContent"
    placeholder="请输入回复内容"
    rows="4"
  />
</a-modal>
  </a-card>
</template>

<script>
import {getReport, replyFeedback} from "../../services/feedback";

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
  {
    title: "操作",
    dataIndex: "action",
    scopedSlots: { customRender: "action" },
    width: 150,
  }
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
  name: "handledFeedbbackList",
  inject: ['reload'],
  components: {},
  data() {
    return {
      data,
      columns,
      showDetail: false,
      reply: '',
      selectData: {},
      showReplyModalVisible: false,
      replyContent: "",
      selectedRecord: null,
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
      getReport({mode:1}).then((res)=>{
        console.log(res);
        let d = res.data.reports;
        console.log(d);
        for (let i = 0; i < d.length; i++) {
          data.push({
            id: d[i].id,
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
    handleProcess(id) {
       this.selectedRecord = id;
      this.replyContent = "";
      this.showReplyModalVisible = true;
      console.log("处理举报信息:", record);
    },
    handleReplyOk() {
      if (!this.replyContent) {
        // 可以添加提示信息
        console.log("请输入回复内容");
        return;
      }
      replyFeedback({
        id: this.selectedRecord,
        judgment: this.replyContent,
      })
        .then(() => {
          console.log("回复成功");
          this.showReplyModalVisible = false;
          this.loadNeed();
        })
        .catch((error) => {
          console.error("回复失败", error);
        });
    },
    handleReplyCancel() {
      this.showReplyModalVisible = false;
    },
    deleteComment(commentId) {
      deleteCommentApi(commentId)
        .then(() => {
          console.log("评论删除成功");
          this.loadNeed();
        })
        .catch((error) => {
          console.error("删除评论失败", error);
        });
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
