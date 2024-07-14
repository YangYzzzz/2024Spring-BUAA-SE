<template>
  <div class="searchPage">
    <el-row style="margin-top: 30px;">
      <!-- 打字机效果的文字 -->
      <div class="typewriter">
        <h2>搜索更简单，啦啦啦啦啦</h2>
      </div>

      <!-- 搜索框 -->
      <el-col :span="20" :offset="2" style="display: block;">
        <el-row class="switch-row">
          <el-switch v-model="isDialogSearch" active-text="语义匹配" inactive-text="精确匹配">
          </el-switch>
        </el-row>
        <el-row>
          <search-input :searchType="isDialogSearch ? 'dialogue' : 'string'"/>
        </el-row>
      </el-col>
      <div class="hot_title">
        <img src="../../assets/hotpaper.png" alt="热门文献推荐" />
      </div>
      <!-- 推荐文献表格 -->
      <el-row>
        <el-col :span="24">
          <el-card class="table-card">
            <el-table :data="displayRecommendations" v-loading="loading" style="width: 100%;">
              <el-table-column prop="title" label="文献标题" align="center" class-name="title-column">
                <template slot-scope="scope">
                  <router-link :to="{ name: 'paper-info', params: { paper_id: scope.row.paper_id } }" class="title">
                    {{ truncateTitle(scope.row.title, 28) }}
                  </router-link>
                </template>
              </el-table-column>
              <el-table-column prop="subfield" label="分类" align="center" class-name="subfield-column">
                <template slot-scope="scope">
                  <span class="subfield">{{ scope.row.sub_classes[0] }}</span>
                </template>
              </el-table-column>
              <el-table-column label="引用数" align="center" class-name="citation-column">
                <template slot-scope="scope">
                  <div class="info-item1">
                    <img src="../../assets/icon/citate.svg" alt="citate" class="info-icon">
                    {{ scope.row.citation_count }}
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="阅读量" align="center" class-name="read-column">
                <template slot-scope="scope">
                  <div class="info-item2">
                    <img src="../../assets/icon/read.svg" alt="read" class="info-icon">
                    {{ scope.row.read_count }}
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="收藏数" align="center" class-name="collect-column">
                <template slot-scope="scope">
                  <div class="info-item3">
                    <img src="../../assets/icon/collect.svg" alt="collect" class="info-icon">
                    {{ scope.row.collect_count }}
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="点赞数" align="center" class-name="like-column">
                <template slot-scope="scope">
                  <div class="info-item4">
                    <img src="../../assets/icon/good.svg" alt="good" class="info-icon">
                    {{ scope.row.like_count }}
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
      <el-pagination v-if="totalPages > 1" background style="margin-top: 10px;" @current-change="changePage"
        :current-page="currentPage" :page-size="itemsPerPage" layout="prev, pager, next" :total="totalRecords">
      </el-pagination>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios'
import SearchInput from './SearchInput.vue'

export default {
  components: {
    'search-input': SearchInput
  },
  data () {
    return {
      recommendations: [],
      loading: true,
      currentPage: 1,
      itemsPerPage: 5,
      isDialogSearch: true
    }
  },
  computed: {
    totalPages () {
      return Math.ceil(this.recommendations.length / this.itemsPerPage)
    },
    totalRecords () {
      return this.recommendations.length
    },
    displayRecommendations () {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.recommendations.slice(start, end)
    }
  },
  created () {
    this.fetchRecommend()
  },
  methods: {
    fetchRecommend () {
      axios
        .get(this.$BASE_API_URL + '/paperRecommend')
        .then(response => {
          this.recommendations = response.data.papers
          this.loading = false
        })
        .catch(error => {
          console.error('Error', error)
        })
    },
    truncateTitle (abstract, maxLength) {
      if (abstract.length > maxLength) {
        return abstract.substring(0, maxLength) + '...'
      }
      return abstract
    },
    changePage (page) {
      this.currentPage = page
    }
  }
}
</script>

<style scoped>
.searchPage {
  position: relative;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 20px;
  padding-top: 2.5rem;
  min-height: 100vh;
  background-image: url('../../assets/dashboardBack2.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center bottom;
  background-attachment: fixed;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.el-row {
  width: 100%;
}

.el-col {
  display: flex;
  justify-content: center;
  align-items: center;
}

.hot_title {
  margin-top: 8.5rem;
  margin-bottom: 1rem;
  text-align: center;
  font-size: 2rem;
  color: #cd5b4c;
  font-family: '微软雅黑', 'Microsoft YaHei', sans-serif;
  font-weight: bold;
  display: flex;
  justify-content: center;
  width: 100%;
}

.hot_title img {
  width: 20%;
}

.typewriter {
  margin-top: 5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 2.5rem;
  margin-bottom: 2rem;
}

.typewriter h2 {
  color: #409EFE;
  font-family: '微软雅黑', 'Microsoft YaHei', sans-serif;
  font-weight: bold;
  overflow: hidden;
  border-right: 0.15em solid #409EFE;
  white-space: nowrap;
  margin-left: 35%;
  margin-right: 35%;
  animation: typing 4s steps(40, end) infinite, blink-caret 0.75s step-end infinite;
  animation-fill-mode: forwards;
}

@keyframes typing {
  0% {
    width: 0;
  }

  50% {
    width: 100%;
  }

  100% {
    width: 0;
  }
}

@keyframes blink-caret {

  from,
  to {
    border-color: transparent;
  }

  50% {
    border-color: #409EFE;
  }
}

.table-card {
  width: 70%;
  border-radius: 12px;
  margin: 0 auto;
}

.recommendations-table {
  width: 100%;
}

.title-column {
  /* width: 35%; */
  text-align: justify;
}

/*.subfield-column,
.citation-column,
.read-column,
.collect-column,
.like-column {
  width: 13%;
  text-align: center;
} */

.el-table .cell {
  display: flex;
  justify-content: center;
  align-items: center;
}

.el-table .title-column .cell {
  justify-content: flex-start;
}

.title {
  color: #409EFE;
  margin: 0;
  width: 100%;
  font-size: 14px;
  text-align: justify;
  word-break: break-all;
  /* Add this line */
}

.title:hover {
  color: #0056b3;
}

.info-item1,
.info-item2 {
  display: flex;
  align-self: center;
  align-items: center;
  font-size: 14px;
  color: #606266;
  margin-left: 2.4rem;
}

.info-item3,
.info-item4 {
  display: flex;
  align-self: center;
  align-items: center;
  font-size: 14px;
  color: #606266;
  margin-left: 2.6rem;
}

.info-icon {
  width: 1rem;
  height: 1rem;
}

.switch-row {
  width: 70%;
  /* 设置第一行的宽度为70% */
  margin: 0 auto;
  /* 居中第一行 */
  display: flex;
  /* 使用flex布局 */
  align-items: center;
  /* 垂直居中 */
  padding: 10px;
}

.switch-row>* {
  margin-right: auto;
  /* 将el-switch推向左边 */
}
</style>
