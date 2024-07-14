<template>
<div class="personal">
  <div id="personal-main">
    <transition name="sidebar-transition">
      <sidebar v-if="showSidebar" @tabSelected="selectTab" />
    </transition>
    <div class="content">
      <transition name="content-transition">
        <PersonalInfo v-if="selectedTab === 'personal'" />
        <AiConversations v-else-if="selectedTab === 'ai'" />
        <SearchRecords v-else-if="selectedTab === 'search'" />
        <MyReports v-else-if="selectedTab === 'reports'" />
        <CollectedPapers v-else-if="selectedTab === 'collections'" />
        <Notifications v-else-if="selectedTab === 'notices'" />
      </transition>
    </div>
  </div>
</div>
</template>

<script>
import Sidebar from '@/components/Personal/PersonalNavbar.vue'
import PersonalInfo from '@/components/Personal/PersonalInfo.vue'
import AiConversations from '@/components/Personal/PersonalChat.vue'
import SearchRecords from '@/components/Personal/PersonalSearch.vue'
import MyReports from '@/components/Personal/PersonalReport.vue'
import CollectedPapers from '@/components/Personal/PersonalCollections.vue'
import Notifications from '@/components/Personal/PersonalNotices.vue'

export default {
  name: 'PersonalMain',
  components: {
    Sidebar,
    PersonalInfo,
    AiConversations,
    SearchRecords,
    MyReports,
    CollectedPapers,
    Notifications
  },
  data () {
    return {
      selectedTab: 'personal', // 默认选中“我的信息”
      showSidebar: false
    }
  },
  methods: {
    selectTab (tabName) {
      this.selectedTab = tabName
    }
  },
  created () {
    const selectedTab = localStorage.getItem('selectedPersonalTab')
    if (selectedTab) {
      this.selectedTab = selectedTab
    }
  },
  mounted () {
    this.showSidebar = true
  },
  destroyed () {
    localStorage.removeItem('loginTime')
    localStorage.removeItem('favorites')
    localStorage.removeItem('likes')
  }
}
</script>

<style scoped>
#personal-main {
  display: flex;
}
.content {
  flex: 1;
  padding: 20px;
  margin-left: 150px; /* 侧边栏宽度 */
}
.personal{
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

.content-transition-enter-active, .content-transition-leave-active {
  transition: opacity 0.3s ease-in-out, transform 0.4s ease-in-out;
}
.content-transition-enter {
  opacity: 0;
  transform: translateY(200px);
}
.content-transition-leave-to {
  opacity: 0;
  transform: scale(0.8);
  position: absolute;
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
