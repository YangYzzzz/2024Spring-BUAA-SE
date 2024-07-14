<template>
  <div class="documentMan">
    <div
      class="uploadCard"
      :class="{ 'hovered': isHovered, 'clicked': isClicked, 'dragover': isDragOver }"
      @click="handleCardClick"
      @mouseenter="isHovered = true"
      @mouseleave="isHovered = false"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
    >
      <img src="../../assets/icon/chooseFile.svg" alt="Upload Icon" class="upload-icon" />
      <div class="upload-text">选择文件</div>
      <div class="upload-support">仅支持pdf格式，文件大小不得超过5MB</div>
      <input id="file-upload" type="file" @change="handleFileUpload" accept=".pdf" ref="fileInput" style="display: none;">
      <span class="filename">{{ fileName }}</span>
      <el-button type="primary" @click.stop="uploadDocumentClick">
        上传<i class="el-icon-upload el-icon-right"></i>
      </el-button>
    </div>
  </div>
</template>

<script>
import { uploadDocument } from '@/request/userRequest.js'

export default {
  data () {
    return {
      file: null,
      fileName: '未选择文件',
      isHovered: false,
      isClicked: false,
      isDragOver: false
    }
  },
  methods: {
    handleFileUpload (event) {
      const file = event.target.files[0]
      const maxSizeInMB = 5
      const maxSizeInBytes = maxSizeInMB * 1024 * 1024

      if (file.size > maxSizeInBytes) {
        this.$message.error('文件大小不得超过5MB')
        this.$refs.fileInput.value = '' // 清空文件输入
        return
      }

      this.file = event.target.files[0]
      this.fileName = this.file ? this.file.name : '未选择文件'
    },
    async uploadDocument () {
      if (!this.file) {
        this.$notify({
          title: '警告',
          message: '请先选择一个文件！',
          type: 'warning'
        })
        return
      }

      try {
        const formData = new FormData()
        formData.append('new_paper', this.file)
        await uploadDocument(formData)
        this.$notify({
          title: '成功',
          message: '本地文件上传成功！',
          type: 'success'
        })
        this.resetFileState()
      } catch (error) {
        console.log(error)
        this.$notify({
          title: '失败',
          message: '本地文件上传失败！',
          type: 'error'
        })
      }
    },
    uploadDocumentClick (event) {
      event.stopPropagation()
      this.uploadDocument()
    },
    resetFileState () {
      this.file = null
      this.fileName = '未选择文件'
      this.$refs.fileInput.value = ''
    },
    handleCardClick () {
      this.isClicked = !this.isClicked
      this.$refs.fileInput.click()
    },
    handleDragOver (event) {
      this.isDragOver = true
    },
    handleDragLeave (event) {
      this.isDragOver = false
    },
    handleDrop (event) {
      this.isDragOver = false
      const files = event.dataTransfer.files
      if (files.length > 0) {
        const file = files[0]
        const maxSizeInMB = 5
        const maxSizeInBytes = maxSizeInMB * 1024 * 1024
        if (file.size > maxSizeInBytes) {
          this.$message.error('文件大小不得超过5MB')
          this.$refs.fileInput.value = '' // 清空文件输入
          return
        }
        this.file = files[0]
        this.fileName = this.file ? this.file.name : '未选择文件'
      }
    }
  }
}
</script>

<style scoped>
.documentMan {
  background: transparent;
  margin-top: 5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.uploadCard {
  /* background: white; */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 44rem;
  height: 22rem;
  border: 5px dashed #409EFE;
  border-radius: 12px;
  cursor: pointer;
  text-align: center;
  margin-bottom: 1rem;
  transition: opacity 0.2s ease;
  opacity: 1; /* 初始透明度 */
}

.uploadCard.hovered {
  opacity: 0.9;
  background: white;
}

.uploadCard.clicked {
  background: #cfc5c5;
  opacity: 0.9;
}

.upload-icon {
  width: 8rem;
}

.upload-text {
  font-weight: bold;
  font-size: 1.2rem;
  margin-top: 1rem;
  color: #409EFE;
}

.upload-support {
  font-size: 1rem;
  color: #999;
  margin-top: 0.5rem;
}

.filename {
  margin-top: 0.25rem;
  margin-bottom: 1rem;
}

.el-button {
  padding: 0.5rem 1rem;
  background-color: #409EFE;
  color: white;
  border: none;
  cursor: pointer;
}

.el-button:hover {
  background-color: #0056b3;
}

.uploadCard.dragover {
  border-color: #409EFE;
  opacity: 0.9;
  background: white;
}
</style>
