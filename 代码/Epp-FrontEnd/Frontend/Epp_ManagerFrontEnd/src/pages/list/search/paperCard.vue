<template>
  <div>
    <a-card :bordered="false" dis-hover>
      <div slot="title">
        发布者:
        <a href="javascript:0" :id="id">{{
          creator["username"] === "" ? "未知用户" : creator["username"]
        }}</a>
      </div>
      <p slot="extra">
        {{ kind === 1 ? "论文解读" : "批注" }}发布于: {{ createAt }}
      </p>
      <a-Row>
        解读对象: <a :href="source"> {{ citation }} </a>-------{{
          publishedYear
        }}年
      </a-Row>
      <a-Row> 标题: {{ title }} </a-Row>
      <br />
      <br />
      <br />
      <editor v-html="content"></editor>
      <br />
      <a-Row>
        <a-Tag v-for="(tag, index) in tags" :key="index" class="sysTopics">{{
          tag.name
        }}</a-Tag>
      </a-Row>
      <br />
      <template v-if="displayType === 0">
        <a-space>
          <a-button href="javascript:0" style="font-size: 14px">
            <a-Icon type="star-o" />收藏{{ totalFavor }}
          </a-button>
          <a-button href="javascript:0" style="font-size: 14px">
            <a-Icon type="like-o" />点赞 {{ totalLike }}
          </a-button>
          <a-button @click="onComment" style="font-size: 14px">
            <a-Icon type="message" />评论 {{totalcomment}}
          </a-button>
        </a-space>

        <a-Card v-if="showComment" style="margin-top: 10px;">
          <comment v-bind="comments"></comment>
        </a-Card>
      </template>
    </a-card>
  </div>
</template>
<script>
import comment from "./comment.vue";
import Editor from "@/pages/components/editor/editor.vue";
import editor from "@/pages/components/editor/editor.vue";

import {
  getInterpretationComments,
  getUserInfo,
  InterpretationIdReq,
  getLocalTime,
} from "@/services/dataSource";
export default {
  name: "PaperCard",
  components: {
    comment,
    Editor,
    editor,
  },
  props: {
    id: {
      type: Number,
      default: 0,
    },

    creator: {
      type: Object,
      default: () => {
        return {
          username: "xx",
          id: "0",
        };
      },
    },

    title: {
      type: String,
      default: "引用",
    },

    kind: {
      type: Number,
      default: 1,
    },

    citeMessageInit: {
      type: String,
      default: "引用",
    },

    createAt: {
      type: String,
      default: "年/月/日",
    },

    content: {
      type: String,
      default: "这是一个展示示例",
    },

    tags: {
      type: Array,
      default: () => {
        return [];
      },
    },

    isLike: {
      type: Boolean,
      default: false,
    },

    isCollect: {
      type: Boolean,
      default: false,
    },

    likeNumber: {
      type: Number,
      default: 0,
    },

    favorNumber: {
      type: Number,
      default: 0,
    },

    commentNum: {
      type: Number,
      default: 0,
    },

    displayType: {
      type: Number,
      default: 0,
    },

    source: {
      type: String,
      default: "qq",
    },

    citation: {
      type: String,
      default: "ss",
    },

    publishedYear: {
      type: Number,
      default: 0,
    },

    interpretations: {
      type: Array,
      default: () => {
        return [];
      },
    },

    userpic:{
      type: String,
      // default: 'http://122.9.14.73:8000/api/images/default_user_icon.jpg'
      // default: 'http://127.0.0.1:8000/api/images/default_user_icon.jpg'
      default: 'http://116.63.14.146:8000/api/images/default_user_icon.jpg'
    }
  },
  data() {
    return {
      like: this.$props.isLike,
      totalLike: this.$props.likeNumber,
      totalcomment: this.$props.commentNum,
      totalFavor: this.$props.favorNumber,
      collect: this.$props.isCollect,
      cited: false,
      showComment: false,
      comments: [],
      detailController: false,
      showUserControl: false,
      userInfo: {},
      htmlTitle: this.title,
      followText: "",
      paperid: "1",
    };
  },
  computed: {
    likeColor: function() {
      return this.like ? "#0084ff" : "#747b8b";
    },

    paperId: function() {
      return this.paperid;
    },

    collectType: function() {
      return this.collect ? "ios-heart" : "ios-heart-outline";
    },

    collectColor: function() {
      return this.collect ? "#fb7299" : "default";
    },

    citeStyle: function() {
      return this.cite ? "margin-left:100px;" : "";
    },

    citeMessage: function() {
      return this.cited ? "取消" : this.citeMessageInit;
    },

    popId: function() {
      return "pop" + this.$props.id;
    },
  },
  methods: {
    onLike: function() {
      this.like = false;
    },

    onCollect: function() {
      this.collect = false;
    },

    onComment: async function() {
      await this.getComments()
      this.showComment = !this.showComment
    },
    showDetail: function() {
      if (this.evidences.length === 0) {
        InterpretationIdReq(this.id, this.kind, "get")
          .then((res) => {
            this.evidences = res.data.evidences;
            this.detailController = true;
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        this.detailController = true;
      }
    },

    convertComments: function(comments) {
      comments = comments.map((x) => ({
        commentId: x.id,
        name: x.username,

        time: getLocalTime(x.created_at),
        id: x.user_id,
        comment: x.text,
        to: x.to_user ? x.to_user.username : 0,
        toId: x.to_user ? x.to_user.id : "",
        inputShow: false,
        // headImg: 'http://122.9.14.73:8000/api/'+x.userpic,
        // headImg: 'http://127.0.0.1:8000/api/'+x.userpic,
        headImg: 'http://116.63.14.146:8000/api/'+x.userpic,
        parent_comment_id: x.parent_comment_id,
        reply: [],
      }));
      let father_comments_map = {};
      comments
        .filter((x) => x.parent_comment_id === undefined)
        .forEach((x) => {
          father_comments_map[x.commentId] = x;
        });
      comments.forEach((x) => {
        if (x.parent_comment_id !== undefined) {
          father_comments_map[x.parent_comment_id].reply.push(x);
        }
      });
      return Object.values(father_comments_map);
    },

    getComments: async function () {
      let username = ''
      let userid = ''
      let userpic=''
      await getUserInfo().then(res => {
        userid = res.data.id
        username = res.data.username
        // userpic ='http://122.9.14.73:8000/api/'+res.data.userpic
        // userpic ='http://127.0.0.1:8000/api/'+res.data.userpic
        userpic ='http://116.63.14.146:8000/api/'+res.data.userpic
      }).catch(error => {
        console.log(error)
      })

      let header = {
        myName: username,
        interpretation_id: this.id,
        myHeader: userpic,
        myId: userid
      }
      await getInterpretationComments('get', {
        interpretation_id: this.id,
        pindex: 1,
        psize: 20
      }).then(res => {
        this.comments = { ...header, comments_init: this.convertComments(res.data.comment_list) }
        console.log(this.comments)
      }).catch(err => {
        console.log(err)
        this.comments = header
      })
    },
  },

  
};
</script>
