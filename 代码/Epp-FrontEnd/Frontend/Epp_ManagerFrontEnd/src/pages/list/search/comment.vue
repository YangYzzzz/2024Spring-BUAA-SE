<template>
  <div>
    <div v-for="(item,i) in comments" :key="i" class="author-title reply-father">
      <a-Avatar class="header-img" size="default" :src="item.headImg"></a-Avatar>
      <div class="author-info">
        <span class="author-name">{{item.name}}</span>
        <span class="author-time">{{item.time}}</span>
      </div>
      <div class="icon-btn">
        
        <a-popconfirm confirm title="确定要删除吗?删除后将不可恢复。" @confirm="deleteItem(i,reply)">
          <a-Button>
            <a-Icon type="delete" />删除
          </a-Button>
        </a-popconfirm>

        <a-Button @click="likeReply(item)" v-if="false">
          <a-Icon type="md-arrow-dropup" />
          点赞{{item.like}}
        </a-Button>
      </div>
      <div class="talk-box">
        <p>
          <span class="reply"><editor v-html="item.comment"></editor></span>
        </p>
      </div>
      <div class="reply-box">
        <div v-for="(reply,j) in item.reply" :key="j" class="author-title">
          <a-Avatar class="header-img" size="default" :src="reply.headImg"></a-Avatar>
          <div class="author-info">
            <span class="author-name">{{reply.name}}</span>
            <span class="author-time">{{reply.time}}</span>
          </div>
          <div class="icon-btn">
            <a-popconfirm confirm title="确定要删除吗?删除后将不可恢复。" @confirm="deleteReply(i,j)">
              <a-Button>
                
                <a-icon type="delete" />删除
              </a-Button>
            </a-popconfirm>
          </div>
          <div class="reply-box"></div>
        </div>
      </div> 
    </div>
  </div>
</template>
<script>
import editor from '@/pages/components/editor/editor.vue'
import {
  createDiscussionComment, 
  deleteDiscussionComment,
  addComment, 
  deleteComment,
} from "@/services/dataSource";

const clickoutside = {
  // 初始化指令
  bind (el, binding,) {
    function documentHandler (e) {
      // 这里判断点击的元素是否是本身，是本身，则返回
      if (el.contains(e.target)) {
        return false
      }
      // 判断指令中是否绑定了函数
      if (binding.expression) {
        // 如果绑定了函数 则调用那个函数，此处binding.value就是handleClose方法
        binding.value(e)
      }
    }
    // 给当前元素绑定个私有变量，方便在unbind中可以解除事件监听
    el.vueClickOutside = documentHandler
    document.addEventListener('click', documentHandler)
  },
  update () { },
  unbind (el, ) {
    // 解除事件监听
    document.removeEventListener('click', el.vueClickOutside)
    delete el.vueClickOutside
  }
}
export default {
  name: 'ArticleComment',
  components: {
   editor
 },
  props: {
    myHeader: {
      type: String,
      default:
        'https://ae01.alicdn.com/kf/Hd60a3f7c06fd47ae85624badd32ce54dv.jpg'
    },
    myId: {
      type: Number,
      default: 19870621
    },
    comments_init: {
      type: Array,
      default: function () {
        return []
      }
    },
    interpretation_id: {
      type: Number,
      default: 0
    },
    commentType: {
      type: Number,
      default: 0
    }
  },
  data () {
    return {
      btnShow: false,
      index: '0',
      replyComment: '',
      myName: "SUPERMANAGER",
      to: '',
      toId: -1,
      comments: this.comments_init
    }
  },
  directives: { clickoutside },
  methods: {
    inputFocus () {
      var replyInput = document.getElementById('replyInput')
      replyInput.style.padding = '8px 8px'
      replyInput.style.border = '2px solid blue'
      replyInput.focus()
    },
    showReplyBtn () {
      this.btnShow = true
    },
    hideReplyBtn () {
      this.btnShow = false
      // replyInput.style.padding = '10px'
      // replyInput.style.border = 'none'
    },
    showReplyInput (i, name, id) {
      console.log(i, name, id)
      this.comments[this.index].inputShow = false
      this.index = i
      this.comments[i].inputShow = true
      this.to = name
      this.toId = id
    },
    _inputShow (i) {
      return this.comments[i].inputShow
    },
    deleteItem (i) {
      const delete_function = this.commentType === 0 ? deleteComment : deleteDiscussionComment
      delete_function('post', {
        id: this.comments[i].commentId
      })
        .then(res => {
          console.log(res)
          this.comments.splice(i, 1)
          this.$message.success('删除成功！')
        })
        .catch(err => {
          console.log(err)
          this.$message.success('删除失败!')
        })
    },
    deleteReply (i, j) {
      const delete_function = this.commentType === 0 ? deleteComment : deleteDiscussionComment
      delete_function('post', {
        id: this.comments[i].reply[j].commentId
      })
        .then(res => {
          console.log(res)
          this.comments[i].reply.splice(j, 1)
          this.$message.success('删除成功！')
        })
        .catch(err => {
          console.log(err)
          this.$message.success('删除失败!')
        })
    },
    sendComment () {
      if (!this.replyComment) {
        this.$message({
          showClose: true,
          type: 'warning',
          message: '评论不能为空'
        })
      } else {
        let a = {}
        let input = document.getElementById('replyInput')
        let timeNow = new Date().getTime()
        let time = this.dateStr(timeNow)
        a.name = this.myName
        a.id = this.myId
        a.comment = this.replyComment
        a.headImg = this.myHeader
        a.time = time
        a.reply = []
        a.commentNum = 0
        a.like = 0
        if (this.commentType === 0) {
          addComment('post', {
            interpretation_id: this.interpretation_id,
            content: a.comment
          })
            .then(res => {
              this.$message.success('评论成功!')
              console.log(res)
              a.commentId = res.data.id
              this.comments.push(a)
              this.replyComment = ''
              input.innerHTML = ''
            })
            .catch(err => {
              console.log(err)
              this.$Message.error('评论失败!')
            })
        } else {
          createDiscussionComment({
            topic_id: this.interpretation_id,
            content: a.comment
          }).then(res => {
            this.$Message.success('评论成功!')
            console.log(res)
            a.commentId = res.data.id
            this.comments.push(a)
            this.replyComment = ''
            input.innerHTML = ''
          }).catch(err => {
            console.log(err)
            this.$Message.error('评论失败!')
          })
        }
      }
    },
    sendCommentReply (i) {
      if (!this.replyComment) {
        this.$message({
          showClose: true,
          type: 'warning',
          message: '评论不能为空'
        })
      } else {
        let a = {}
        let timeNow = new Date().getTime()
        let time = this.dateStr(timeNow)
        a.name = this.myName
        a.to = this.to
        a.id = this.myId
        a.headImg = this.myHeader
        a.comment = this.replyComment
        a.time = time
        a.commentNum = 0
        a.like = 0
        if (this.commentType === 0) {
          addComment('post', {
            interpretation_id: this.interpretation_id,
            content: a.comment,
            parent_comment_id: this.comments[i].commentId,
            to_user_id: this.toId
          })
            .then(res => {
              this.$Message.success('评论成功!')
              console.log(res)
              a.commentId = res.data.id
              this.comments[i].reply.push(a)
              this.replyComment = ''
              document.getElementsByClassName('reply-comment-input')[i].innerHTML = ''
            })
            .catch(err => {
              console.log(err)
              this.$Message.error('评论失败!')
            })
        } else {
          createDiscussionComment({
            topic_id: this.interpretation_id,
            content: a.comment,
            parent_discussion_id: this.comments[i].commentId,
            to_user_id: this.toId
          }).then(res => {
            this.$Message.success('评论成功!')
            console.log(res)
            a.commentId = res.data.id
            this.comments[i].reply.push(a)
            this.replyComment = ''
            document.getElementsByClassName('reply-comment-input')[i].innerHTML = ''
          }).catch(err => {
            console.log(err)
            this.$Message.error('评论失败!')
          })
        }
      }
    },
    onDivInput: function (e) {
      this.replyComment = e.target.innerHTML
    },
    dateStr (date) {
      // 获取js 时间戳
      var time = new Date().getTime()
      // 去掉 js 时间戳后三位，与php 时间戳保持一致
      time = parseInt((time - date) / 1000)
      // 存储转换值
      var s
      if (time < 60 * 10) {
        // 十分钟内
        return '刚刚'
      } else if (time < 60 * 60 && time >= 60 * 10) {
        // 超过十分钟少于1小时
        s = Math.floor(time / 60)
        return s + '分钟前'
      } else if (time < 60 * 60 * 24 && time >= 60 * 60) {
        // 超过1小时少于24小时
        s = Math.floor(time / 60 / 60)
        return s + '小时前'
      } else if (time < 60 * 60 * 24 * 30 && time >= 60 * 60 * 24) {
        // 超过1天少于30天内
        s = Math.floor(time / 60 / 60 / 24)
        return s + '天前'
      } else {
        // 超过30天ddd
        date = new Date(parseInt(date))
        return (
          date.getFullYear() +
          '/' +
          (date.getMonth() + 1) +
          '/' +
          date.getDate()
        )
      }
    }
  
  }
}
</script>

<style>
.my-reply {
  padding: 10px;
  background-color: #fafbfc;
}

.my-reply .header-img {
  display: inline-block;
  vertical-align: top;
}

.my-reply .reply-info {
  display: inline-block;
  margin-left: 5px;
  width: 90%;
}

@media screen and (max-width: 1200px) {
  .my-reply .reply-info {
    width: 80%;
  }
}

.my-reply .reply-info .reply-input {
  min-height: 20px;
  line-height: 22px;
  padding: 10px 10px;
  color: #ccc;
  background-color: #fff;
  border-radius: 5px;
}

.my-reply .reply-info .reply-input:empty:before {
  content: attr(placeholder);
}

.my-reply .reply-info .reply-input:focus:before {
  content: none;
}

.my-reply .reply-info .reply-input:focus {
  padding: 8px 8px;
  border: 2px solid #00f;
  box-shadow: none;
  outline: none;
}

.my-reply .reply-btn-box {
  height: 25px;
  margin: 10px 0;
}

.my-reply .reply-btn-box .reply-btn {
  position: relative;
  float: right;
  margin-right: 15px;
}
.my-reply .text-div {
    word-break: break-all;
}
.my-comment-reply {
  margin-left: 50px;
}

.my-comment-reply .reply-input {
  width: flex;
}

.author-title:not(:last-child) {
  border-bottom: 1px solid rgba(178, 186, 194, 0.3);
}

.author-title {
  padding: 10px;
}

.author-title .header-img {
  display: inline-block;
  vertical-align: top;
}

.author-title .author-info {
  display: inline-block;
  margin-left: 5px;
  width: 60%;
  height: 40px;
  line-height: 20px;
}

.author-title .author-info > span {
  display: block;
  cursor: pointer;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.author-title .author-info .author-name {
  color: #000;
  font-size: 18px;
  font-weight: bold;
}

.author-title .author-info .author-time {
  font-size: 14px;
}

.author-title .icon-btn {
  width: 30%;
  padding: 0 !important;
  float: right;
}

@media screen and (max-width: 1200px) {
  .author-title .icon-btn {
    width: 15%;
    padding: 7px;
  }
}

.author-title .icon-btn > span {
  cursor: pointer;
}

.author-title .icon-btn .iconfont {
  margin: 0 5px;
}

.author-title .talk-box {
  margin: 0 50px;
}

.author-title .talk-box > p {
  margin: 0;
}

.author-title .talk-box .reply {
  font-size: 16px;
  color: #000;
}

.author-title .reply-box {
  margin: 10px 0 0 50px;
  background-color: #efefef;
}
</style>
