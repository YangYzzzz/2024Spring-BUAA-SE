<template>
    <el-dialog title="请输入举报理由" :visible.sync="showReportModal" width="50%" @close="closeReportModal">
        <el-form>
            <el-form-item>
                <el-input type="textarea" placeholder="输入举报理由..." v-model="reportMessage" autosize>
                </el-input>
            </el-form-item>
        </el-form>
        <span slot="footer">
            <el-button @click="showReportModal = false">取 消</el-button>
            <el-button type="primary" @click="submitReport(commentId, commentLevel)">发 送</el-button>
        </span>
    </el-dialog>
</template>

<script>
import axios from 'axios'
export default {
  props: {
    showReportModal: {
      type: Boolean,
      default: false
    },
    commentId: {
      type: String,
      default: ''
    },
    commentLevel: {
      type: Number,
      default: 1
    }
  },
  data () {
    return {
      reportMessage: ''
    }
  },
  methods: {
    submitReport (commentId, commentLevel) {
      if (!this.reportMessage.trim()) {
        this.$message({
          message: '请输入举报理由',
          type: 'warning'
        })
        return
      }
      axios.post(this.$BASE_API_URL + '/reportComment', {'comment_id': commentId, 'comment_level': commentLevel, 'report': this.reportMessage})
        .then((response) => {
          if (response.data.is_success) {
            this.$message({
              message: '举报成功！',
              type: 'success'
            })
          }
        })
        .catch((error) => {
          console.error('举报失败 ', error)
        })
        .finally(() => {
          this.reportMessage = ''
          this.closeReportModal()
        })
    },
    closeReportModal () {
      this.$emit('close-report-modal', false)
    }
  }
}
</script>
