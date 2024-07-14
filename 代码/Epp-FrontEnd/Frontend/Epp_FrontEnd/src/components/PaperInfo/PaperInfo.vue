<template>
    <div>
        <el-row type="flex" justify="center">
            <el-col :span="20">
                <!-- 论文部分 -->
                <el-container class="box" style="margin-top: 60px;">
                    <el-row class="header">
                        {{ paper.title }}
                    </el-row>
                    <el-row>
                        <p><strong>作者:</strong> {{ paper.authors }}</p>
                    </el-row>
                    <el-row style="margin-top: 10px;">
                        <el-col :span="24">
                            <div style="width: 90%; margin: auto; text-align: left;">
                                <p><strong>摘要:</strong> {{ paper.abstract }}</p>
                            </div>
                        </el-col>
                    </el-row>
                    <el-row class="buttons">
                        <el-button type="text" @click="likePaper">
                            <i :class="liked ? 'fas' : 'far'" class="fa-thumbs-up"></i>
                            {{ paper.like_count }}
                        </el-button>
                        <el-button type="text" @click="collectPaper"
                            :icon="collected ? 'el-icon-star-on' : 'el-icon-star-off'">
                            {{ paper.collect_count }}
                        </el-button>
                        <el-button type="text" icon="el-icon-chat-dot-round" @click="showCommentModal = true">{{
                comments.length }}</el-button>
                        <el-button type="text" icon="el-icon-download" @click="downloadPaper">下载</el-button>
                        <router-link :to="{name: 'paper-reader', params: { paper_id: paper.paper_id }}" tag="button" class="el-button el-button--text">
                            <i class="el-icon-view"></i> 在线研读
                        </router-link>
                        <el-link type="primary" :href="paper.original_url" icon="el-icon-link"
                            style="margin-left: 10px;">原文链接</el-link>
                    </el-row>
                </el-container>

                <!-- 评分部分 -->
                <el-container class="box">
                    <el-row>
                        <el-col :span="8" style="justify-content: center; text-align: center">
                            <el-rate v-model="paper.score" disabled show-score text-color="#ff9900">
                            </el-rate>
                            <p>{{ paper.score_count }}个评分</p>
                        </el-col>
                        <el-col :span="8">
                            <el-button type="text" icon="el-icon-edit-outline"
                                @click="showScoreModal = true">我要评分</el-button>
                        </el-col>
                        <el-dialog title="我要评分" :visible.sync="showScoreModal" width="50%" @close="showScoreModal = false">
                            <el-form>
                                <el-form-item>
                                    <el-rate v-model="newScore"></el-rate>
                                </el-form-item>
                            </el-form>
                            <span slot="footer">
                                <el-button @click="showScoreModal = false">取 消</el-button>
                                <el-button type="primary" @click="submitScore">发 送</el-button>
                            </span>
                        </el-dialog>
                    </el-row>
                </el-container>

                <!-- 评论区 -->
                <el-container class="box" style="margin-top: 20px">
                    <!-- 评论弹窗 -->
                    <el-dialog title="发表评论" :visible.sync="showCommentModal" width="50%" @close="closeCommentModal">
                        <el-form>
                            <el-form-item>
                                <el-input type="textarea" placeholder="添加评论..." v-model="newComment" autosize>
                                </el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer">
                            <el-button @click="showCommentModal = false">取 消</el-button>
                            <el-button type="primary" @click="submitComment1(1)">发 送</el-button>
                        </span>
                    </el-dialog>
                    <el-divider>评论区</el-divider>
                    <div class="comments">
                        <div v-if="comments.length > 0">
                            <!-- 一级评论 -->
                            <div v-for="comment in comments" :key="comment.comment_id" class="comment-item">
                                <el-row>
                                    <el-col :span="2">
                                        <img :src="fullURL(comment.user_image)" alt="user avatar" class="avatar">
                                    </el-col>
                                    <el-col :span="22">
                                        <div class="comment-content">
                                            <div style="font-weight: bold;">{{ comment.username }}</div>
                                            <div class="text">{{ comment.text }}</div>
                                            <div class="my-footer">
                                                <span class="date">{{ comment.date }}</span>
                                                <span class="actions">
                                                    <el-button type="text" @click="likeComment(comment.comment_id, 1)">
                                                        <i :class="comment.user_liked ? 'fas' : 'far'" class="fa-thumbs-up"></i>
                                                        {{ comment.like_count }}
                                                    </el-button>
                                                    <el-button type="text" icon="el-icon-chat-dot-round"
                                                        @click="toggleReplyInput(comment.comment_id)">回复</el-button>
                                                    <el-button type="text" icon="el-icon-warning-outline"
                                                        @click="reportComment(comment.comment_id, 1)">举报</el-button>
                                                    <el-button type="text" :icon="showRepliesCommentId === comment.comment_id ? 'el-icon-arrow-up' : 'el-icon-arrow-down'" v-show="comment.second_len > 0"
                                                        @click="fetchComments2(comment.comment_id)">共 {{ comment.second_len }} 条回复</el-button>
                                                </span>
                                            </div>
                                        </div>
                                        <!-- 回复评论的框 -->
                                        <div style="display: flex; margin-bottom: 5px;">
                                            <el-input v-if="showReplyInput == comment.comment_id" type="textarea" v-model="newComment" placeholder="请输入回复内容..." rows="1"></el-input>
                                            <el-button v-if="showReplyInput == comment.comment_id" type="primary" size="small" @click="submitComment2(comment.comment_id)">发送</el-button>
                                        </div>
                                    </el-col>
                                </el-row>

                                <!-- 二级评论部分 -->
                                <div v-show="showRepliesCommentId === comment.comment_id">
                                    <div v-if="secondLevelComments.length > 0">
                                        <div v-for="comment2 in secondLevelComments" :key="comment2.comment_id"
                                            class="comment-item">
                                            <el-row>
                                                <el-col :span="2" :offset="2">
                                                    <img :src="fullURL(comment2.user_image)" alt="user avatar"
                                                        class="avatar">
                                                </el-col>
                                                <el-col :span="20">
                                                    <div class="comment-content">
                                                        <div style="font-weight: bold;">{{ comment2.username }}</div>
                                                        <div class="text">
                                                            <!-- 后续加上跳转到用户个人中心的功能 -->
                                                            <router-link v-if="comment2.to_username"
                                                                :to="{ name: '', params: { username: comment2.to_username } }">
                                                                @{{ comment2.to_username }}
                                                            </router-link>
                                                            {{ comment2.text }}
                                                        </div>
                                                        <div class="my-footer">
                                                            <span class="date">{{ comment2.date }}</span>
                                                            <span class="actions">
                                                                <el-button type="text" @click="likeComment">
                                                                    <i :class="comment2.user_liked ? 'fas' : 'far'" class="fa-thumbs-up"></i>
                                                                    {{ comment2.like_count }}
                                                                </el-button>
                                                                <el-button type="text" icon="el-icon-chat-dot-round"
                                                                    @click="toggleReplyInput(comment2.comment_id)">回复</el-button>
                                                                <el-button type="text" icon="el-icon-warning-outline"
                                                                    @click="reportComment(comment2.comment_id, 2)">举报</el-button>
                                                            </span>
                                                        </div>
                                                    </div>
                                                    <!-- 回复评论的框 -->
                                                    <div style="display: flex; margin-bottom: 5px;">
                                                        <el-input v-if="showReplyInput == comment2.comment_id" type="textarea" v-model="newComment" placeholder="请输入回复内容..." rows="1"></el-input>
                                                        <el-button v-if="showReplyInput == comment2.comment_id" type="primary" size="small" @click="submitComment3(comment.comment_id, comment2.comment_id)">发送</el-button>
                                                    </div>
                                                </el-col>
                                            </el-row>
                                        </div>
                                    </div>
                                    <p v-else>暂无评论</p>
                                </div>
                            </div>
                        </div>
                        <p v-else>暂无评论</p>
                    </div>
                </el-container>
            </el-col>
        </el-row>
        <report-modal :showReportModal="showReportModal" :commentId="reportedCommentId"
        :commentLevel="reportedCommentLevel" @close-report-modal="showReportModal = false"></report-modal>
    </div>
</template>

<script>
import axios from 'axios'
import ReportModal from './ReportModal.vue'
export default {
  props: {
    paper_id: {
      type: String,
      required: true
    }
  },
  components: {
    'report-modal': ReportModal
  },
  computed: {
  },
  data () {
    return {
      paper: {},
      liked: false,
      collected: false,
      scored: false,
      newComment: '',
      comments: [],
      showCommentModal: false,
      newScore: 0,
      showScoreModal: false,
      showRepliesCommentId: null,
      showReplyInput: null, // 显示回复二级评论的输入框
      secondLevelComments: [],
      showReportModal: false,
      reportedCommentId: '',
      reportedCommentLevel: 0
    }
  },
  created () {
    this.paper_id = this.$route.params.paper_id
    this.fetchPaperInfo()
    this.fetchComments1()
    this.fetchUserPaperInfo()
  },
  methods: {
    fullURL (url) {
      return this.$BASE_URL + url
    },
    fetchUserPaperInfo () {
      axios.get(this.$BASE_API_URL + '/getUserPaperInfo?paper_id=' + this.paper_id)
        .then((response) => {
          this.liked = response.data.liked
          this.collected = response.data.collected
          this.scored = response.data.score !== 0
          this.newScore = response.data.score
        })
        .catch((error) => {
          console.error('Error', error)
        })
    },
    fetchPaperInfo () {
      console.log('传递过来的paper id:', this.paper_id)
      // 向后端传送id，返回论文结果
      //   console.log('url is...' + this.$BASE_API_URL + '/getPaperInfo?paper_id=' + this.paper_id)
      axios.get(this.$BASE_API_URL + '/getPaperInfo?paper_id=' + this.paper_id)
        .then((response) => {
          console.log('paper info is ...')
          this.paper = response.data
          console.log(this.paper)
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
    fetchComments1 () {
      // 向后端传送id，返回论文结果
      axios.get(this.$BASE_API_URL + '/getComment1?paper_id=' + this.paper_id)
        .then((response) => {
          console.log('一级评论 ...')
          this.comments = response.data.comments
          console.log(this.comments)
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
    likePaper () {
      axios.post(this.$BASE_API_URL + '/userLikePaper', { 'paper_id': this.paper_id })
        .then(() => {
          this.liked = !this.liked
          this.liked ? this.paper.like_count++ : this.paper.like_count--
        })
        .catch((error) => {
          console.error('点赞操作失败:', error)
          this.$message({
            message: '点赞操作失败',
            type: 'error'
          })
        })
    },
    collectPaper () {
      axios.post(this.$BASE_API_URL + '/collectPaper', { 'paper_id': this.paper_id })
        .then(() => {
          this.collected = !this.collected
          this.collected ? this.paper.collect_count++ : this.paper.collect_count--
        })
        .catch((error) => {
          console.error('收藏操作失败:', error)
          this.$message({
            message: '收藏操作失败',
            type: 'error'
          })
        })
    },
    downloadPaper () {
      // 实现下载功能
      axios.post(this.$BASE_API_URL + '/batchDownload', {'paper_id_list': [this.paper_id]})
        .then((response) => {
          if (response.data.is_success === true) {
            this.$message({
              message: '开始下载！',
              type: 'success'
            })
            const zipUrl = this.$BASE_URL + response.data.zip_url
            const link = document.createElement('a')
            link.href = zipUrl
            link.download = 'papers.zip'
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            this.selectedPapers = []
          }
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
    likeComment (commentId, commentLevel) {
      axios.post(this.$BASE_API_URL + '/likeComment', { 'comment_level': commentLevel, 'comment_id': commentId })
        .then((response) => {
          const comment = this.comments.find(c => c.comment_id === commentId)
          comment.user_liked = !comment.user_liked
          comment.user_liked ? comment.like_count++ : comment.like_count--
        })
        .catch((error) => {
          console.error('点赞操作失败:', error)
          this.$message({
            message: '点赞操作失败',
            type: 'error'
          })
        })
    },
    reportComment (commentId, commentLevel) {
      this.reportedCommentId = commentId
      this.reportedCommentLevel = commentLevel
      this.showReportModal = true
    },
    closeCommentModal () {
      this.showCommentModal = false // 关闭对话框
      this.newComment = ''
    },
    submitComment1 () {
      console.log('评论级别', 1)
      console.log('提交的评论内容：', this.newComment)
      let isSuccessful = false
      axios.post(this.$BASE_API_URL + '/commentPaper', {'paper_id': this.paper_id, 'comment_level': 1, 'comment': this.newComment})
        .then((response) => {
          isSuccessful = true
        })
        .catch((error) => {
          console.error('Error : ', error)
          isSuccessful = false
        })
        .finally(() => {
          this.newComment = ''
          this.showCommentModal = false
          window.location.reload()
          if (isSuccessful) {
            this.$message({
              message: '评论成功',
              type: 'success'
            })
          } else {
            this.$message({
              message: '评论失败',
              type: 'error'
            })
          }
        })
    },
    submitComment2 (level1CommentId) {
      console.log('1级评论', this.level1CommentId)
      console.log('提交的评论内容：', this.newComment)
      axios.post(this.$BASE_API_URL + '/commentPaper', {
        'paper_id': this.paper_id,
        'comment_level': 2,
        'level1_comment_id': level1CommentId,
        'comment': this.newComment
      })
        .then((response) => {
          if (response.data.is_success) {
            this.$message({
              message: '评论成功',
              type: 'success'
            })
          }
        })
        .catch((error) => {
          console.error('Error : ', error)
          this.$message({
            message: '评论失败',
            type: 'error'
          })
        })
        .finally(() => {
          this.newComment = ''
          // window.location.reload()
        })
    },
    submitComment3 (level1CommentId, level2CommentId) {
      console.log('评论级别', 3)
      console.log('提交的评论内容：', this.newComment)
      axios.post(this.$BASE_API_URL + '/commentPaper', {
        'paper_id': this.paper_id,
        'comment_level': 2,
        'level1_comment_id': level1CommentId,
        'reply_comment_id': level2CommentId,
        'comment': this.newComment
      })
        .then((response) => {
          if (response.data.is_success) {
            this.$message({
              message: '评论成功',
              type: 'success'
            })
          }
        })
        .catch((error) => {
          console.error('Error : ', error)
          this.$message({
            message: '评论失败',
            type: 'error'
          })
        })
        .finally(() => {
          this.newComment = ''
          // window.location.reload()
        })
    },
    submitScore () {
      console.log('提交的评分内容：', this.newScore)
      if (this.scored) {
        this.$message({
          message: '暂不支持修改评分哦～',
          type: 'error'
        })
        return
      }
      // 这里可以添加评论提交的逻辑
      axios.post(this.$BASE_API_URL + '/userScoring', {'paper_id': this.paper_id, 'score': this.newScore})
        .then((response) => {
          if (response.status === 200) {
            this.$message({
              message: '评分成功',
              type: 'success'
            })
          }
        })
        .catch((error) => {
          console.error('评分失败', error)
          this.$message({
            message: '评分失败',
            type: 'error'
          })
        })
        .finally(() => {
          this.showScoreModal = false // 关闭对话框
          window.location.reload()
        })
    },
    fetchComments2 (commentId) {
      if (this.showRepliesCommentId === commentId) {
        this.showRepliesCommentId = null
        return
      }
      console.log('second level comment id is ' + commentId)
      const url = this.$BASE_API_URL + '/getComment2?paper_id=' + this.paper_id + '&comment1_id=' + commentId
      console.log(url)
      axios.get(url)
        .then((response) => {
          this.secondLevelComments = response.data.comments
          console.log(response.data.message)
          console.log('二级评论：', response.data.comments)
          this.showRepliesCommentId = commentId
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
    toggleReplyInput (commentId) {
      if (this.showReplyInput === commentId) {
        this.showReplyInput = null
      } else {
        this.showReplyInput = commentId
      }
    }
  }
}
</script>

<style scoped>
.header {
    font-size: 40px;
    text-align: center;
}

.buttons {
    margin-left: 20px;
    justify-content: flex-start;
}

p {
    word-wrap: break-word;
    /* 允许单词在必要时断行 */
}

.avatar {
    width: 50%;
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    overflow: hidden;   /* 超出容器的图片部分会被隐藏 */
    object-fit: cover;  /* 图片会覆盖整个容器，且内容会被裁剪以适应 */
}

.comment-content {
    text-align: left;
}

.text {
    margin-top: 5px;
}

.my-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.date {
    font-size: 0.85rem;
    color: #666;
}

.actions {
    display: flex;
    align-items: center;
}
</style>
