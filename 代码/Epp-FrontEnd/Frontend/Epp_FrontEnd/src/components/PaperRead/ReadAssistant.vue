<template>
  <el-container style="height: calc(100vh - 60px);" class="read-assistant">
    <el-header class="my-header">
      <h3>调研助手</h3>
      <div>
        <el-tooltip class="item" effect="dark" content="一键总结" placement="top">
          <el-button type="success" plain size="small" @click="renderMarkdown()" icon="fas fa-file-text"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="清除历史对话" placement="top">
          <el-button type="primary" plain size="small" @click="clearHistory()" icon="fas fa-eraser"
            style="margin-right: 10px;"></el-button>
        </el-tooltip>
        <el-dialog :visible.sync="showSummaryModal" width="70%">
            <div v-html="markdownFile" style=""></div>
        </el-dialog>
      </div>
    </el-header>

    <el-main class="chat-content">
      <div v-for="(message, index) in chatMessages" :key="index">
        <div v-if="message.sender === 'ai'" class="message-bubble left">
          <div v-if="message.loading" v-loading="message.loading" element-loading-text="拼命加载中"
            element-loading-spinner="el-icon-loading" style="width: 100px; height: 40px;">
          </div>
          <div v-else>
            <p style="white-space: pre-wrap;" v-html="message.text"></p>
            <el-button type="text" @click="regenerateAnswer"
              v-show="index == chatMessages.length - 1 && answerFinished">
              <i class="fas fa-refresh"></i>
              重新生成
            </el-button>
            <el-button type="text" @click="findReplySource" v-show="index == chatMessages.length - 1 && answerFinished">
              <i class="fas fa-quote-right"></i>
              查询出处
            </el-button>
          </div>
        </div>
        <div v-else class="message-bubble right">
          <p style="white-space: pre-wrap;">{{ message.text }}</p>
        </div>
      </div>
      <div style="margin-top: 10px;">
        <div v-show="answerFinished" v-for="(question, index) in probQuestions" :key="index" class="prob-question"
          @click="sendProbQuestion(question)">
          {{ question }}
        </div>
      </div>
    </el-main>

    <el-footer>
      <el-input v-model="chatInput" placeholder="输入你的消息..." @keyup.enter.native="chatToAI"></el-input>
      <el-button type="primary" @click="chatToAI">发送</el-button>
    </el-footer>
  </el-container>
</template>

<script>
import axios from 'axios'
import markdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css' // 选择你喜欢的样式

export default {
  props: {
    paperID: {
      type: String,
      default: ''
    },
    fileReadingId: {
      type: Number,
      defaults: 0
    }
  },
  data () {
    return {
      chatInput: '',
      chatMessages: [],
      answerFinished: false,
      probQuestions: [],
      showSummaryModal: false,
      markdownFile: '',
      summaryFinished: false
    }
  },
  mounted () {
    this.md = markdownIt({
      highlight: function (str, lang) {
        if (lang && hljs.getLanguage(lang)) {
          try {
            return '<pre class="hljs"><code class="code-block">' +
                    hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
                    '</code></pre>'
          } catch (__) {}
        }
        return '<pre class="hljs"><code class="code-block">' + this.md.utils.escapeHtml(str) + '</code></pre>'
      }
    })
    this.fileReadingID = this.fileReadingId
    if (this.fileReadingID > 0) {
      this.restorePaperStudy()
    } else {
      this.initialize()
    }
  },
  methods: {
    initialize () {
      const existingPaperId = localStorage.getItem('paperID')
      if (existingPaperId === this.paperID) {
        this.fileReadingID = localStorage.getItem('fileReadingID')
        console.log('existing file reading id is...', localStorage.getItem('fileReadingID'))
        console.log('my file reading id is...', this.fileReadingID)
        this.restorePaperStudy()
      } else {
        this.createPaperStudy()
      }
    },
    createPaperStudy () {
      const loadingInstance = this.$loading({
        lock: true,
        text: '正在创建知识库...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)',
        target: '.read-assistant' // 指定加载动画的目标
      })
      axios.post(this.$BASE_API_URL + '/study/createPaperStudy', { 'paper_id': this.paperID, 'file_type': 2 })
        .then((response) => {
          if (response.status === 200) {
            this.fileReadingID = response.data.file_reading_id
            localStorage.setItem('fileReadingID', this.fileReadingID)
            localStorage.setItem('paperID', this.paperID)
            console.log('研读对话的id, ', response.data.file_reading_id)
            this.$message({
              message: '论文研读知识库创建成功！',
              type: 'success'
            })
            loadingInstance.close()
          }
        })
        .catch((error) => {
          console.log('Error: ', error)
          loadingInstance.close()
        })
    },
    restorePaperStudy () {
      const loadingInstance = this.$loading({
        lock: true,
        text: '正在恢复研读对话...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)',
        target: '.read-assistant' // 指定加载动画的目标
      })
      console.log('恢复研读对话的id, ', this.fileReadingID)
      axios.post(this.$BASE_API_URL + '/study/restorePaperStudy', { 'file_reading_id': this.fileReadingID })
        .then((response) => {
          const history = response.data.conversation_history.conversation
          for (const message of history) {
            const sender = message.role === 'user' ? 'user' : 'ai'
            const text = message.role === 'user' ? message.content : this.md.render(message.content)
            this.chatMessages.push({ sender: sender, text: text, loading: false })
          }
          this.$message({
            message: '已恢复研读对话',
            type: 'success'
          })
          loadingInstance.close()
        })
        .catch((error) => {
          console.error('恢复论文研读失败: ', error)
          loadingInstance.close()
        })
    },
    async chatToAI () {
      const chatMessage = this.chatInput.trim()
      if (!chatMessage) {
        this.$message({
          message: '请输入你的问题',
          type: 'warning'
        })
        return
      }
      this.chatInput = ''
      this.answerFinished = false
      this.chatMessages.push({ sender: 'user', text: chatMessage, loading: false })

      let loadingMessage = { sender: 'ai', text: 'AI正在思考...', loading: true }
      this.chatMessages.push(loadingMessage)
      let answer = ''
      //   Add user message to chat
      // 有一些很奇怪的bug
      if (!this.fileReadingID) {
        if (localStorage.getItem('fileReadingID')) {
          console.log('遇到了一些bug')
          this.fileReadingID = localStorage.getItem('fileReadingID')
        } else {
          this.$message({
            message: '找不到对话ID',
            type: 'error'
          })
        }
      }
      console.log('file reading id is...', this.fileReadingID)
      try {
        await this.$axios.post(this.$BASE_API_URL + '/study/doPaperStudy', { 'query': chatMessage, 'file_reading_id': this.fileReadingID })
          .then(response => {
            answer = response.data.ai_reply
            this.docs = response.data.docs
            this.probQuestions = response.data.prob_question
            loadingMessage.loading = false
            loadingMessage.text = ''
          })
      } catch (error) {
        console.error('Error:', error)
        loadingMessage.text = ''
        answer = '抱歉, 无法从AI获取回应。'
        loadingMessage.loading = false
      } finally {
        this.answerFinished = false
        let cur = 0
        while (cur < answer.length) {
          loadingMessage.text += answer.charAt(cur)
          cur++
          await this.delay(10)
        }
        loadingMessage.text = this.md.render(loadingMessage.text)
        this.answerFinished = true
      }
    },
    delay (ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
    async regenerateAnswer () {
      console.log('regenerating...')
      const lastMessage = this.chatMessages[this.chatMessages.length - 1]
      lastMessage.text = 'AI正在思考...'
      lastMessage.loading = true
      this.answerFinished = false
      let answer = ''
      console.log('file_reading_id', this.fileReadingID)
      await axios.post(this.$BASE_API_URL + '/study/reDoPaperStudy', { 'file_reading_id': this.fileReadingID })
        .then((response) => {
          answer = response.data.ai_reply
          this.probQuestions = response.data.prob_question
          lastMessage.text = ''
          lastMessage.loading = false
        })
        .catch((error) => {
          console.error('Error:', error)
          lastMessage.text = ''
          answer = '抱歉, 无法从AI获取回应。'
          lastMessage.loading = false
        })
      let cur = 0
      while (cur < answer.length) {
        lastMessage.text += answer.charAt(cur)
        cur++
        await this.delay(50)
      }
      this.answerFinished = true
    },
    findReplySource () {
      if (this.docs.length === 0) {
        return
      }
      console.log('finding source...')
      this.answerFinished = false
      const sources = this.docs
      console.log('answer\'s source is...', this.docs)
      const lastMessage = this.chatMessages[this.chatMessages.length - 1]
      lastMessage.text += '\n来源: \n'
      let cnt = 1
      for (const source of sources) {
        const index1 = source.indexOf(']')
        const index2 = source.indexOf(']', index1 + 1)
        lastMessage.text += '[' + cnt + ']'
        lastMessage.text += source.substring(index2 + 1)
        lastMessage.text += '\n'
        cnt++
      }
      this.docs = []
      this.answerFinished = true
    },
    sendProbQuestion (question) {
      this.chatInput = question
    },
    renderMarkdown () {
      axios.post(this.$BASE_API_URL + '/study/generateAbstractReport', { document_id: '', paper_id: this.paperID })
        .then((response) => {
          if (response.data.summary) {
            const summary = response.data.summary
            this.markdownFile = this.md.render(summary)
            this.showSummaryModal = true
          } else {
            this.$message({
              message: '正在为您生成摘要，请稍等...',
              type: 'warning'
            })
            this.summaryFinished = false
          }
        })
        .catch(() => {
          this.$message({
            message: '生成摘要失败！',
            type: 'error'
          })
          this.summaryFinished = true
        })
    },
    clearHistory () {
      axios.post(this.$BASE_API_URL + '/study/clearConversation', {file_reading_id: this.fileReadingID})
        .then((response) => {
          if (response.status === 200) {
            this.$message({
              message: '清除历史对话成功！',
              type: 'success'
            })
            this.chatMessages = []
            this.probQuestions = []
            this.answerFinished = false
          }
        })
        .catch((error) => {
          console.error('清除对话失败', error)
        })
    }
  }

}
</script>

<style scoped>
.my-header {
  display: flex;
  justify-content: space-between;
  /* padding: 20px; */
  align-items: center;
}

.chat-content {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  /* 确保元素可以根据需要对齐到左边或右边 */
  background: rgb(233, 242, 251);
  width: 100%;
  /* 可以调整宽度以适应不同屏幕大小 */
}

.el-footer {
  background: rgb(233, 242, 251);
  display: flex;
  align-items: center;
  height: 100%;
  margin: 0;
}

.message-bubble {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  border: 1px solid #ccc;
  margin: 5px 0;
  overflow-y: auto;
  text-align: left;
}

.message-bubble p {
  margin: 0;
}

.right {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
  float: right;
  border-radius: 15px 0 15px 15px;
  clear: both;
  word-break: break-all;
}

.left {
  background-color: white;
  color: black;
  float: left;
  clear: both;
  border-radius: 0 15px 15px 15px;
}

.prob-question {
  background-color: white;
  color: black;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 5px 20px;
  text-align: left;
  margin-bottom: 5px;
  font-size: small;
  max-width: 90%;
  cursor: pointer
}

.code-block {
  width: 20px;
  white-space: pre-wrap !important; /* 允许内容在必要时自动换行 */
  word-wrap: break-word !important; /* 在长单词或 URL 内部进行换行 */
  overflow-wrap: break-word !important; /* 确保在必要时可以断开单词 */
  overflow-x: auto !important; /* 允许横向滚动，如果需要的话 */
}

.hljs {
    white-space: pre-wrap; /* 允许代码换行 */
    word-break: break-word; /* 在长单词或 URL 地址内部进行换行 */
}

.read-assistant pre code hljs {
    word-break: break-word !important;
    white-space: pre-wrap;
}
</style>
