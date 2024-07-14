<template>
    <div class="collections">
      <el-row>
        <el-col :span="24">
          <h1 class="chatTitle">研读历史</h1>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-card class="table-card">
          <el-table :data="displayedDocuments" v-loading="loading" style="width: 100%; min-height: 420px;" :default-sort = "{prop: 'date', order: 'descending'}">
            <el-table-column prop="paper_title" label="论文标题" width="400">
              <template slot-scope="scope">
                <router-link v-if="scope.row.mode === 1" class="paper-link" :to="{ name: 'paper-reader', params: { paper_id: scope.row.paper_id }, query: { fileReadingID: scope.row.file_reading_id }}">
                  {{ scope.row.paper_title }}
                </router-link>
                <router-link v-else class="paper-link" :to="{ name: 'localPaper-reader', params: { paper_id: scope.row.paper_id }, query: { fileReadingID: scope.row.file_reading_id }}">
                  {{ scope.row.paper_title }}
                </router-link>
              </template>
            </el-table-column>
            <el-table-column prop="mode" label="类型" align="center" width="100">
              <template slot-scope="scope">
                <el-tag v-if="scope.row.mode === 1" type="success">在线</el-tag>
                <el-tag v-else type="warning">上传</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="研读时间" align="center" sortable></el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <el-button type="primary" icon="el-icon-delete" size="small" @click="deleteDocument(scope.row.mode, scope.row.paper_id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-pagination
            v-if="totalPages > 1"
            background
            style="margin-top: 10px;"
            @current-change="changePage"
            :current-page="currentPage"
            :page-size="itemsPerPage"
            layout="prev, pager, next"
            :total="totalDocuments">
          </el-pagination>
        </el-col>
      </el-row>
    </div>
  </template>

<script>
import { fetchChat, deleteChat } from '@/request/userRequest.js'
export default {
  data () {
    return {
      documents: [],
      currentPage: 1,
      itemsPerPage: 6,
      loading: true
    }
  },
  computed: {
    totalDocuments () {
      return this.documents.length
    },
    totalPages () {
      return Math.ceil(this.totalDocuments / this.itemsPerPage)
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
        var res = (await fetchChat()).data
        res.paper_reading_list.sort((a, b) => {
          return new Date(b.date) - new Date(a.date)
        })
        this.documents = res.paper_reading_list
        this.totalDocuments = res.total
        this.loading = false
      } catch (error) {
        console.log('error')
      }
    },
    async deleteDocument (mode, id) {
      try {
        // eslint-disable-next-line camelcase
        var paper_ids = []
        paper_ids.push(id)
        var data = {mode, paper_ids}
        var res = (await deleteChat({data}))
        console.log(res)
        this.$notify({
          title: '成功',
          message: '删除对话历史成功！',
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

.chatTitle{
   font-size: 30px;
  font-weight: bold;
  margin-bottom: 20px;
  color:rgb(18, 19, 18);
}

.table-card {
  border-radius: 12px;
}
/*链接样式*/
.paper-link {
  color: #409EFE;
  text-decoration: none;
}
.paper-link:hover {
  opacity: 0.8;
  text-decoration: none;
}

</style>
