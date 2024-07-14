<template>
    <el-row style="overflow: hidden; height: 100vh;">
      <el-col :span="16" style="margin-top: 60px;">
        <iframe :src="pdfUrl" style="width: 100%; height: 755px;" frameborder="0">
        </iframe>
      </el-col>
      <el-col :span="8" style="margin-top: 60px">
        <read-assistant :paperID="paper_id" :fileReadingId="fileReadingID" />
      </el-col>
    </el-row>
</template>

<script>
import ReadAssistant from './LocalReadAssistant.vue'
import axios from 'axios'
export default {
  components: {
    'read-assistant': ReadAssistant
  },
  props: {
    paper_id: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      pdfUrl: '',
      fileReadingID: ''
    }
  },
  created () {
    this.fetchPaperPDF()
    this.fileReadingID = this.$route.query.fileReadingID
  },
  methods: {
    fetchPaperPDF () {
      axios.get(this.$BASE_API_URL + '/getDocumentURL?document_id=' + this.paper_id)
        .then((response) => {
          this.pdfUrl = this.$BASE_URL + response.data.local_url
          //   this.pdfUrl = '../../../static/Res3ATN -- Deep 3D Residual Attention Network for Hand Gesture  Recognition in Videos.pdf'
          console.log('论文PDF为', this.pdfUrl)
        })
        .catch((error) => {
          console.log('请求论文PDF失败 ', error)
        })
    }
  }

}
</script>

<style scoped>

</style>
