<template>
  <el-col style="overflow: hidden; height: 100vh">
    <el-col :span="16" style="margin-top: 80px;" type="flex">
      <el-row>
        <el-col :span="22" :offset="1" style="display: flex; align-items: center;">
          <el-switch v-model="isDialogSearch" active-text="语义匹配" inactive-text="精确匹配">
          </el-switch>
          <div style="width: 80%;">
            <search-input :searchType="isDialogSearch ? 'dialogue' : 'string'"
            :searchContent="defaultSearchContent"/>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="4" style="margin-top: 15px;">
          <el-col :span="18" :offset="6">
            <!-- 侧边栏 -->
            <div class="filter-cond">
              <el-button type="text" @click="filterByYear(0)"
                :class="filterYear === 0 ? 'clicked-button' : 'normal-button'">时间不限</el-button>
            </div>
            <div class="filter-cond">
              <el-button type="text" @click="filterByYear(2024)"
                :class="filterYear === 2024 ? 'clicked-button' : 'normal-button'">2024年以来</el-button>
            </div>
            <div class="filter-cond">
              <el-button type="text" @click="filterByYear(2022)"
                :class="filterYear === 2022 ? 'clicked-button' : 'normal-button'">2022年以来</el-button>
            </div>
            <div class="filter-cond">
              <el-button type="text" @click="filterByYear(2020)"
                :class="filterYear === 2020 ? 'clicked-button' : 'normal-button'">2020年以来</el-button>
            </div>
            <el-divider></el-divider>
            <div class="filter-cond">
              <el-button type="text" @click="sortPapers('')"
                :class="sortOrder === '' ? 'clicked-button' : 'normal-button'">默认排序</el-button>
            </div>
            <div class="filter-cond">
              <el-button type="text" @click="sortPapers('asc')"
                :class="sortOrder === 'asc' ? 'clicked-button' : 'normal-button'">按时间升序</el-button>
            </div>
            <div class="filter-cond">
              <el-button type="text" @click="sortPapers('desc')"
                :class="sortOrder === 'desc' ? 'clicked-button' : 'normal-button'">按时间降序</el-button>
            </div>
            <el-divider></el-divider>
            <el-form label-position="top">
              <el-form-item>
                <el-select v-model="filterSubclass" placeholder="所有类别" @change="applyFilter">
                  <el-option label="所有类别" value=""></el-option>
                  <el-option label="边缘检测" value="边缘检测"></el-option>
                  <el-option label="目标检测" value="目标检测"></el-option>
                  <el-option label="图像分类" value="图像分类"></el-option>
                  <el-option label="图像去噪" value="图像去噪"></el-option>
                  <el-option label="图像分割" value="图像分割"></el-option>
                  <el-option label="人脸识别" value="人脸识别"></el-option>
                  <el-option label="姿态估计" value="姿态估计"></el-option>
                  <el-option label="动作识别" value="动作识别"></el-option>
                  <el-option label="人群计数" value="人群计数"></el-option>
                  <el-option label="医学影像" value="医学影像"></el-option>
                  <el-option label="三维重建" value="三维重建"></el-option>
                  <el-option label="对抗样本攻击" value="对抗样本攻击"></el-option>
                </el-select>
              </el-form-item>
            </el-form>
            <el-divider></el-divider>
          </el-col>
        </el-col>
        <el-col :span="20">
          <el-main>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                共检索出 {{ filteredPapers.length }} 篇论文
                <div>
                  <el-button type="success" icon="el-icon-download" @click="downloadPapers" size="small">
                    下载文献
                  </el-button>
                  <el-button type="primary" icon="el-icon-document-copy" @click="generateSummaryReport" size="small">
                    生成综述
                  </el-button>
                </div>
              </div>
              <div class="papers-container" v-if="papers && papers.length > 0">
                <div v-for="paper in filteredPapers" :key="paper.paper_id" style="margin-top: 30px;">
                  <div class="columns is-mobile">
                    <div class="column is-narrow checkbox">
                      <el-checkbox v-model="checkedPapers[paper.paper_id]"
                      @change="handleCheckboxChange(paper.paper_id)"></el-checkbox>
                    </div>
                    <paper-card :paper="paper" />
                  </div>
                </div>
              </div>
              <div v-else-if="papers && papers.length == 0">
                <img src="@/assets/userAvatar/ybw.jpg" alt="" width="30%" height="30%" style="border-radius: 50%; margin-top: 3rem;">
                <img src="@/assets/前面的区域以后再来探索吧.jpg" alt="">
              </div>
            <el-backtop :visibility-height="100"></el-backtop>
          </el-main>
        </el-col>
      </el-row>
    </el-col>
    <el-col :span="8" style="height: 100vh; position: sticky; top: 55px">
      <ai-assistant v-if="aiReply.length > 0" :aiReply="aiReply" :paperIds="paperIds" :searchRecordID="searchRecordID"
        :restoreHistory="restoreHistory" @find-paper="searchPaperByAssistant" />
    </el-col>
  </el-col>
</template>

<script>
import axios from 'axios'
import SearchAssistant from './SearchAssistant.vue'
import PaperCard from './PaperCard.vue'
import SearchInput from './SearchInput.vue'
export default {
  components: {
    'ai-assistant': SearchAssistant,
    'paper-card': PaperCard,
    'search-input': SearchInput
  },
  props: ['searchForm'],
  watch: {
    async '$route' (to, from) {
      console.log('to query\'s search record id...', to.query.searchRecordID)
      console.log('to query\'s search content...', to.query.search_content)
      this.papers = []
      window.location.reload()
    }
  },
  data () {
    return {
      papers: null,
      filterYear: 0,
      sortOrder: '',
      filterSubclass: '',
      filteredPapers: [],
      aiReply: [],
      paperIds: [],
      searchRecordID: '',
      restoreHistory: false,
      selectedPapers: [],
      checkedPapers: {},
      isDialogSearch: true,
      defaultSearchContent: ''
    }
  },
  methods: {
    filterByYear (year) {
      this.filterYear = year
      this.applyFilter()
    },
    sortPapers (sortOrder) {
      this.sortOrder = sortOrder
      this.applyFilter()
    },
    applyFilter () {
      let results = this.papers.slice()
      if (this.sortOrder === 'asc') {
        results.sort((a, b) => {
          const dateA = new Date(a.publication_date)
          const dateB = new Date(b.publication_date)
          return dateA - dateB // 升序排序
        })
      } else if (this.sortOrder === 'desc') {
        results.sort((a, b) => {
          const dateA = new Date(a.publication_date)
          const dateB = new Date(b.publication_date)
          return dateB - dateA // 降序排序
        })
      } else {
        console.log('default order:', this.papers)
        results = this.papers
      }
      results = results.filter(paper => {
        const year = new Date(paper.publication_date).getFullYear()
        console.log(year)
        return year >= this.filterYear
      })
      if (this.filterSubclass.length > 0) {
        results = results.filter(paper => {
          return paper.sub_classes.includes(this.filterSubclass)
        })
      }
      this.filteredPapers = results
      console.log('filter papers: ', this.filteredPapers)
    },
    async fetchPapers () {
      console.log('Fetching papers...')
      const loadingInstance = this.$loading({
        lock: true,
        text: 'Loading...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      await axios.post(this.$BASE_API_URL + '/search/vectorQuery', { 'search_content': this.$route.query.search_content, 'search_type': this.$route.query.searchType })
        .then((response) => {
          console.log('response is ...')
          this.papers = response.data.paper_infos
          // 添加ai回答的逻辑
          this.aiReply.push({ sender: 'ai', text: response.data.ai_reply, loading: false, type: 'dialog' })
          // console.log('ai的回复: ', this.aiReply)
          this.paperIds = this.papers.map(paper => paper.paper_id)
          this.searchRecordID = response.data.search_record_id
          this.defaultSearchContent = this.$route.query.search_content
          loadingInstance.close()
        })
        .catch((error) => {
          console.error('语义检索失败:', error)
        })
    },
    async fetchPapersFromHistory () {
      console.log('search record ID: ', this.$route.query.searchRecordID)
      await axios.get(this.$BASE_API_URL + '/search/restoreSearchRecord?search_record_id=' + this.$route.query.searchRecordID)
        .then((response) => {
          this.papers = response.data.paper_infos
          console.log('历史记录的论文', this.papers)
          this.defaultSearchContent = response.data.conversation[0].content
          console.log('first message is ', this.defaultSearchContent)
          for (const message of response.data.conversation) {
            const sender = message.role === 'user' ? 'user' : 'ai'
            this.aiReply.push({ sender: sender, text: message.content, loading: false, type: 'dialog' })
          }
          // console.log('历史记录对话信息 ', this.aiReply)
          this.paperIds = this.papers.map(paper => paper.paper_id)
          this.restoreHistory = true
        })
        .catch((error) => {
          console.error('恢复历史记录失败: ', error)
        })
    },
    handleCheckboxChange (paperId) {
      const index = this.selectedPapers.indexOf(paperId)
      if (index > -1) {
        // 如果已存在，则移除
        this.selectedPapers.splice(index, 1)
      } else {
        // 如果不存在，则添加
        this.selectedPapers.push(paperId)
      }
    },
    resetCheckboxes () {
      Object.keys(this.checkedPapers).forEach(key => {
        this.checkedPapers[key] = false
      })
    },
    initializeCheckboxes () {
      this.papers.forEach(paper => {
        this.$set(this.checkedPapers, paper.paper_id, false)
      })
    },
    generateSummaryReport () {
      if (this.selectedPapers.length === 0) {
        this.$message({
          message: '请选择论文',
          type: 'warning'
        })
        return
      }
      console.log('选中的论文:', this.selectedPapers)
      axios.post(this.$BASE_API_URL + '/summary/generateSummaryReport', { 'paper_id_list': this.selectedPapers }, { timeout: 300000 })
        .then((response) => {
          if (response.status === 200) {
            this.$message({
              message: '正在生成综述报告',
              type: 'success'
            })
            this.getSummaryReportStatus(response.data.report_id)
          }
        })
        .catch((error) => {
          console.error('综述报告生成失败:', error)
          this.$message({
            message: '综述报告生成失败',
            type: 'error'
          })
        })
      this.selectedPapers = []
      this.resetCheckboxes()
    },
    getSummaryReportStatus (reportID) {
      console.log('报告ID是', reportID)
      let intervalID = setInterval(() => {
        axios.get(this.$BASE_API_URL + '/summary/getSummaryStatus?report_id=' + reportID)
          .then(response => {
            if (response.data.status === '生成成功') {
              this.$message({
                message: '综述报告已生成，请在个人中心查看',
                type: 'success'
              })
              clearInterval(intervalID) // 停止轮询
            }
          })
          .catch(error => {
            console.error('查询状态失败:', error)
            clearInterval(this.intervalID) // 错误时停止轮询
          })
      }, 1000) // 每秒查询一次
    },
    downloadPapers () {
      if (this.selectedPapers.length === 0) {
        this.$message({
          message: '请选择论文',
          type: 'warning'
        })
      }
      axios.post(this.$BASE_API_URL + '/batchDownload', { 'paper_id_list': this.selectedPapers })
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
      this.selectedPapers = []
      this.resetCheckboxes()
    },
    searchPaperByAssistant (papers) {
      console.log('循征之后的论文', papers)
      this.papers = papers
      this.applyFilter()
      const paperIDs = papers.map(paper => paper.paper_id)
      axios.post(this.$BASE_API_URL + '/search/changeRecordPapers', { search_record_id: this.searchRecordID, paper_id_list: paperIDs })
        .then((response) => {
          console.log(response.status)
          if (response.status === 200) {
            console.log('论文循征成功, ', response.data.msg)
          }
        })
        .catch((error) => {
          console.error('论文循征失败, ', error)
        })
    }
  },
  async mounted () {
    if (this.$route.query.searchRecordID) {
      this.searchRecordID = this.$route.query.searchRecordID
      await this.fetchPapersFromHistory()
    } else {
      await this.fetchPapers()
    }
    this.applyFilter()
    this.initializeCheckboxes()
  }
}
</script>

<style scoped>
.filter-cond {
  display: flex;
  justify-content: flex-start;
}

.normal-button {
  color: black;
  font-weight: normal !important;
}

.clicked-button {
  color: #409EFE;
  font-weight: normal !important;
  font-size: 16px;
}

.checkbox {
  margin-left: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.papers-container {
  height: 100vh;
}

/* 对话式检索部分 */
.el-header {
  text-align: center;
  padding: 20px;
}

.chat-content {
  background: rgb(233, 242, 251);
}

.el-footer {
  background: rgb(233, 242, 251);
  display: flex;
  align-items: center;
  height: 100%;
  margin: 0;
}

.my-message {
  background-color: #acd1f7;
  color: white;
  text-align: right;
}

.other-message {
  background-color: white;
  color: black;
  text-align: left;
}
</style>
