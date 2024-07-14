<template>
  <div>
    <el-row>
      <el-col :span="24">
        <h1 class='searchTitle'>搜索记录</h1>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-card class="table-card">
          <el-table :data="displayedDocuments" v-loading="loading" style="width: 100%; min-height: 400px;" :default-sort = "{prop: 'date', order: 'descending'}">
            <el-table-column prop="keyword" label="关键词" align="center">
              <template slot-scope="scope">
                <router-link class="search-link" :to="{ name: 'search-results', query: { searchRecordID: scope.row.search_record_id }}">{{ scope.row.keyword }}</router-link>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="搜索时间" align="center" sortable></el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <el-button type="primary" icon="el-icon-delete" size="small" @click="deleteReport(scope.row.search_record_id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    <el-pagination
      v-if="totalPages > 1"
      background
      style="margin-top: 10px;"
      @current-change="changePage"
      :current-page="currentPage"
      :page-size="itemsPerPage"
      layout="prev, pager, next"
      :total="totalRecords">
    </el-pagination>
  </div>
</template>

<script>
import { fetchSearchHistory, deleteSearchHistory } from '@/request/userRequest.js'
export default {
  data () {
    return {
      documents: [],
      currentPage: 1,
      itemsPerPage: 6,
      report_id: '',
      loading: true
    }
  },
  computed: {
    totalPages () {
      return Math.ceil(this.documents.length / this.itemsPerPage)
    },
    totalRecords () {
      return this.documents.length
    },
    displayedDocuments () {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.documents.slice(start, end)
    }
  },
  methods: {
    async fetchDocuments () {
      try {
        this.documents = []
        var res = (await fetchSearchHistory()).data
        res.keywords.sort((a, b) => {
          return new Date(b.date) - new Date(a.date)
        })
        this.documents = res.keywords
        this.loading = false
      } catch (error) {
        console.log(error)
      }
    },
    async deleteReport (id) {
      // eslint-disable-next-line camelcase
      var data = {search_record_id: id}
      try {
        var res = (await deleteSearchHistory({data}))
        console.log(res)
        this.$notify({
          title: '成功',
          message: '删除搜索记录成功！',
          type: 'success'
        })
      } catch (error) {
        console.log('error')
      }
      this.fetchDocuments()
    },
    changePage (page) {
      this.currentPage = page
    },
    truncateAbstract (abstract, maxLength) {
      if (abstract.length > maxLength) {
        return abstract.substring(0, maxLength) + '...'
      }
      return abstract
    }
  },
  mounted () {
    this.fetchDocuments()
  }
}
</script>

<style scoped>
/* 可以添加样式来美化表格 */
.searchTitle{
  font-size: 30px;
  font-weight: bold;
  margin-bottom: 20px;
  color:rgb(18, 19, 18);
}
.table-card {
  border-radius: 12px;
}

/*链接样式*/
.search-link {
  color: #409EFE;
  text-decoration: none;
}
.search-link:hover {
  opacity: 0.8;
  text-decoration: none;
}
</style>
