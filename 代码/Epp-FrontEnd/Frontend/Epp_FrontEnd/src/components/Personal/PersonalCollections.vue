<template>
  <div class="collections">
    <el-row>
      <el-col :span="24">
        <h1 class="collectionsTitle">收藏文献</h1>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-card class="table-card">
          <el-table :data="displayedDocuments" v-loading="loading" style="width: 100%; min-height: 420px;" :default-sort = "{prop: 'publication_date', order: 'descending'}">
            <el-table-column prop="title" label="论文标题" width="300">
              <template slot-scope="scope">
                <router-link class="collection-link" :to="{ name: 'paper-info', params: { paper_id: scope.row.paper_id }}">{{ scope.row.title }}</router-link>
              </template>
            </el-table-column>
            <el-table-column prop="authors" label="作者">
              <template slot-scope="scope">
                {{ transauthors(scope.row.authors) }}
              </template>
            </el-table-column>
            <el-table-column prop="abstract" label="摘要">
              <template slot-scope="scope">
                {{ truncateAbstract(scope.row.abstract, 50) }}
              </template>
            </el-table-column>
            <el-table-column prop="publication_date" label="发表日期" align="center" sortable></el-table-column>
            <el-table-column prop="score" label="论文评分" width="150" align="center" sortable>
              <template slot-scope="scope">
                <el-rate
                v-model="scope.row.score"
                disabled
                text-color="#409EFE"
                score-template="{value}">
                </el-rate>
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <el-button type="primary" size="small" icon="el-icon-delete" @click="deleteDocument(scope.row.paper_id)">删除</el-button>
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
import { fetchCollectedPapers, deleteCollectedPapers } from '@/request/userRequest.js'
export default {
  data () {
    return {
      documents: [{paper_id: '0000f570-04bc-49fa-b2d4-56447ca1bd9b', title: 'Quantization of Deep Neural Networks for Accurate Edge Computing', score: '9', author: 'Wentao Chen', date: '2021-04-25', abstract: 'Deep neural networks (DNNs) have demonstrated their great potential in recent\nyears, exceeding the per-formance of human experts in a wide range of\napplications. Due to their large sizes, however, compressiontechniques such as\nweight quantization and pruning are usually applied before they can be\naccommodated onthe edge. It is generally believed that quantization leads to\nperformance degradation, and plenty of existingworks have explored quantization\nstrategies aiming at minimum accuracy loss. In this paper, we argue\nthatquantization, which essentially imposes regularization on weight\nrepresentations, can sometimes help toimprove accuracy. We conduct\ncomprehensive experiments on three widely used applications: fully con-nected\nnetwork (FCN) for biomedical image segmentation, convolutional neural network\n(CNN) for imageclassification on ImageNet, and recurrent neural network (RNN)\nfor automatic speech recognition, and experi-mental results show that\nquantization can improve the accuracy by 1%, 1.95%, 4.23% on the three\napplicationsrespectively with 3.5x-6.4x memory reduction.\n'},
        {paper_id: 'f570111-04bc-49fa-b2d4-56447ca1bd9b', title: 'Quantization of Deep Neural Networks for Accurate Edge Computing', score: '9', author: 'Wentao Chen', date: '2021-04-25', abstract: 'Deep neural networks (DNNs) have demonstrated their great potential in recent\nyears, exceeding the per-formance of human experts in a wide range of\napplications. Due to their large sizes, however, compressiontechniques such as\nweight quantization and pruning are usually applied before they can be\naccommodated onthe edge. It is generally believed that quantization leads to\nperformance degradation, and plenty of existingworks have explored quantization\nstrategies aiming at minimum accuracy loss. In this paper, we argue\nthatquantization, which essentially imposes regularization on weight\nrepresentations, can sometimes help toimprove accuracy. We conduct\ncomprehensive experiments on three widely used applications: fully con-nected\nnetwork (FCN) for biomedical image segmentation, convolutional neural network\n(CNN) for imageclassification on ImageNet, and recurrent neural network (RNN)\nfor automatic speech recognition, and experi-mental results show that\nquantization can improve the accuracy by 1%, 1.95%, 4.23% on the three\napplicationsrespectively with 3.5x-6.4x memory reduction.\n'}],
      currentPage: 1,
      itemsPerPage: 4,
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
        console.log('getres')
        this.documents = []
        var res = (await fetchCollectedPapers()).data
        console.log(res)
        console.log(res.total)
        console.log(res.papers)
        res.papers.sort((a, b) => {
          return new Date(b.publication_date) - new Date(a.publication_date)
        })
        this.documents = res.papers
        this.loading = false
      } catch (error) {
        console.log(error.message)
      }
    },
    async deleteDocument (id) {
      // eslint-disable-next-line camelcase
      var paper_ids = []
      paper_ids.push(id)
      try {
        var data = {paper_ids}
        var res = await deleteCollectedPapers({data})
        console.log(res)
        this.paper_ids = []
        this.$notify({
          title: '成功',
          message: '删除收藏记录成功！',
          type: 'success'
        })
        localStorage.removeItem('favorites')
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
    },
    transauthors (authors) {
      var str = ''
      authors.forEach(element => {
        str = str + element + ','
      })
      var ans = this.truncateAbstract(str, 20)
      return ans
    }
  },
  mounted () {
    this.fetchDocuments()
  }
}
</script>

<style scoped>
/* 可以添加样式来美化表格 */

.collectionsTitle{
   font-size: 30px;
  font-weight: bold;
  margin-bottom: 20px;
  color:rgb(18, 19, 18);
}
.table-card {
  border-radius: 12px;
}

/*链接样式*/
.collection-link {
  color: #409EFE;
  text-decoration: none;
}
.collection-link:hover {
  opacity: 0.8;
  text-decoration: none;
}
</style>
