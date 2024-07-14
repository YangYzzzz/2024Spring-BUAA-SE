<template>
<div class="documentMan">
   <h1 class="documentManTitle">全文解读</h1>
  <div class="uploadDo">
   <a for="file-upload" class="file-upload-label" style="text-decoration: underline; color: #409EFE; cursor: pointer;" @click="$refs.fileInput.click()">选择文件</a>
  <input id="file-upload" type="file" @change="handleFileUpload" accept=".pdf,.doc,.docx" style="display: none;" ref="fileInput">
  <span class='filename'>{{ fileName }}</span>
  <el-button type="primary" @click="uploadDocument">Upload<i class="el-icon-upload el-icon-right"></i></el-button>
  </div>
  <div class="documentsTable">
  <Documents/>
  </div>
 </div>
</template>

<script>
import Documents from '@/components/Personal/Documents.vue'
import { uploadDocument } from '@/request/userRequest.js'
import { EventBus } from '@/main.js'

export default {
  components: {
    Documents
  },
  data () {
    return {
      documents: [],
      currentPage: 1,
      totalPages: 1,
      itemsPerPage: 10,
      report_id: '',
      fileName: '未选择文件'
    }
  },
  methods: {
    handleFileUpload (event) {
      this.file = event.target.files[0]
      if (this.file) {
        this.fileName = this.file.name
      } else {
        this.fileName = '未选择文件'
      }
    },
    async uploadDocument () {
      try {
        const formData = new FormData()
        formData.append('new_paper', this.file) // 将文件字段名改为new_paper
        await uploadDocument(formData)
        alert('文献上传成功！')
        EventBus.$emit('fetchDocuments')
        // this.fetchDocuments()
      } catch (error) {
        console.error(error)
        alert('文献上传失败，请重试。')
      }
    }
  }
}
</script>

<style scoped>
.documentMan{
  margin-top:5rem;
}
.documentManTitle{
  font-size:1.5rem;
}
/* .uploadTitle {
  text-align: center;
  /* margin-top: 2rem;
  margin-bottom: 2rem;
} */
/* .file-upload-label {
  margin-right: 1rem; /* 调整<label>元素右侧的间距
}

#file-upload {
  margin-right: 1rem; /* 调整<input>元素右侧的间距
} */

.filename {
  margin-left: 1rem;
  margin-right: 1rem;/* 调整<span>元素左侧的间距 */
}
.uploadDo {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 0rem;
  border: 8px solid #409EFE;
  border-radius: 10px 10px 0 0;
  padding: 0.5rem;
}

.uploadDo input[type="file"] {
  margin-right: 1rem;
}

.uploadDo button {
  padding: 0.5rem 1rem;
  background-color: #409EFE;
  color: white;
  border: none;
  cursor: pointer;
}

.uploadDo button:hover {
  background-color: #0056b3;
}

.documentsTable {
  margin-left: 3rem;
  margin-right: 3rem;
}

.documentMan::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 120%;
  background-image: url('../../assets/personal-back.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center bottom;
  z-index: -1; /* 确保背景图片在内容后面 */
}
</style>
