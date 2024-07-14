<template>
  <div>
    <el-row>
      <el-col :span="24">
        <h1 class='reportTitle'>综述报告</h1>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-card class="table-card">
          <el-table :data="displayedDocuments" v-loading="loading" style="width: 100%; min-height: 420px;" :default-sort = "{prop: 'date', order: 'descending'}">
            <el-table-column prop="title" label="报告标题" align="center">
              <template slot-scope="scope">
                <el-link class="report-link" :underline="false" @click="viewReport(scope.row.report_id)" type="primary">{{ scope.row.title }}</el-link>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="生成时间" align="center" sortable></el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <el-button type="primary" size="small" icon="el-icon-delete" @click="deleteReport(scope.row.report_id)">删除</el-button>
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
import { fetchReports, deleteReport, fetchReportContent } from '@/request/userRequest.js'
// import marked from 'marked'
// import JsPDF from 'jspdf'
import markdownIt from 'markdown-it'
import html2pdf from 'html2pdf.js'

const md = markdownIt()

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
        var res = (await fetchReports()).data
        console.log(res)
        res.reports.sort((a, b) => {
          return new Date(b.data) - new Date(a.date)
        })
        this.documents = res.reports
        this.loading = false
      } catch (error) {
        console.log('error')
      }
    },
    async deleteReport (id) {
      // eslint-disable-next-line camelcase
      var report_ids = []
      report_ids.push(id)
      var data = {report_ids}
      try {
        var res = (await deleteReport({data}))
        console.log(res)
        this.$notify({
          title: '成功',
          message: '删除综述报告成功！',
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
    },
    convertMarkdownToPdf (markdownContent) {
      const htmlContent = md.render(markdownContent)
      const replacedHtmlContent = htmlContent.replace(/<h3>/g, '<h4>').replace(/<\/h3>/g, '</h4>')
        .replace(/<h2>/g, '<h3>').replace(/<\/h2>/g, '</h3>')
        .replace(/<h1>/g, '<h2>').replace(/<\/h1>/g, '</h2>')
      try {
        const pdf = html2pdf().from(replacedHtmlContent).set({ margin: [15, 20, 20, 20] })
        pdf.toPdf().get('pdf').then(function (pdfDocument) {
          const blob = pdfDocument.output('bloburl')
          window.open(blob, '_blank')
        })
      } catch (error) {
        console.log('markdown2pdf error')
        console.log(error)
      }
    },
    async viewReport (id) {
      try {
        var params = {report_id: id}
        const markdownContent = (await fetchReportContent({params})).data.summary
        console.log(markdownContent)
        this.convertMarkdownToPdf(markdownContent)
      } catch (error) {
        console.log('error')
      }
    }
  },
  mounted () {
    this.fetchDocuments()
  }
}
</script>

<style scoped>
/* 可以添加样式来美化表格 */
.reportTitle{
  font-size: 30px;
  font-weight: bold;
  margin-bottom: 20px;
  color:rgb(18, 19, 18);
}
.table-card {
  border-radius: 12px;
}

/*链接样式*/
.report-link {
  color: #409EFE;
  text-decoration: none;
}
.report-link:hover {
  opacity: 0.8;
  text-decoration: none;
}
</style>
