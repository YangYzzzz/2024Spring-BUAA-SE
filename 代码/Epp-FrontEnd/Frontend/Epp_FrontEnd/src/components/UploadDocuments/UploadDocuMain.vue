<template>
<div class="uploadDocu">
  <div id="uploadDocu-main">
    <transition name="sidebar-transition">
      <Sidebar v-if="showSidebar" @tabSelected="selectTab" />
    </transition>
    <div class="content">
      <Upload v-if="selectedTab === 'upload'" />
      <Documents v-else-if="selectedTab === 'documents'" />
    </div>
  </div>
</div>
</template>

<script>
import Sidebar from '@/components/UploadDocuments/UploadDocuNavbar.vue'
import Upload from '@/components/UploadDocuments/Upload.vue'
import Documents from '@/components/UploadDocuments/Documents.vue'

export default {
  name: 'uploadDocuMain',
  components: {
    Sidebar,
    Upload,
    Documents
  },
  data () {
    return {
      selectedTab: 'upload',
      showSidebar: false
    }
  },
  methods: {
    selectTab (tabName) {
      this.selectedTab = tabName
    }
  },
  mounted () {
    const selectedTab = localStorage.getItem('selectedUploadDocuTab')
    if (selectedTab) {
      this.selectedTab = selectedTab
    }
    this.showSidebar = true
  }
}
</script>

<style scoped>
#uploadDocu-main {
  display: flex;
}
.content {
  flex: 1;
  padding: 20px;
  margin-left: 150px; /* 侧边栏宽度 */
}
.uploadDocu{
  position: relative;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 20px;
  padding-top: 50px;
  min-height: 100vh;
  background-image: url('../../assets/personal-back.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center bottom;
  background-attachment: fixed;
}

.sidebar-transition-enter-active, .sidebar-transition-leave-active {
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
}
.sidebar-transition-enter {
  transform: translateX(-200px);
}
.sidebar-transition-leave-to {
  opacity: 0;
}
</style>
