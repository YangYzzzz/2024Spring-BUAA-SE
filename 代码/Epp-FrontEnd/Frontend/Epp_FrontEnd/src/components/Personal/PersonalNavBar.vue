<template>
  <div class="sidebar">
    <h1>个人中心</h1>
    <ul>
      <li
        v-for="tab in tabs"
        :key="tab.name"
        @click="selectTab(tab.name)"
        :class="{ active: selectedTab === tab.name }"
        >
        <span class="icon" v-if="tab.icon_off">
          <img v-if="selectedTab === tab.name" :src="tab.icon_on" alt="icon" width="20" height="20" />
          <img v-else :src="tab.icon_off" alt="icon" width="20" height="20" />
        </span>
        <span class="label">{{ tab.label }}</span>
      </li>
      <li class="logout" @click="logout">
        <span class="icon">
          <img src="@/assets/icon/logout.svg" alt="icon" width="20" height="20" />
        </span>
        <span class="label">退出登录</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { logout } from '@/request/userRequest.js'
export default {
  data () {
    return {
      selectedTab: 'personal',
      tabs: [
        { name: 'personal', label: '我的信息', icon_off: require('@/assets/icon/personal-off.svg'), icon_on: require('@/assets/icon/personal-on.svg') },
        { name: 'ai', label: '研读历史', icon_off: require('@/assets/icon/ai-off.svg'), icon_on: require('@/assets/icon/ai-on.svg') },
        { name: 'search', label: '搜索记录', icon_off: require('@/assets/icon/search-off.svg'), icon_on: require('@/assets/icon/search-on.svg') },
        { name: 'reports', label: '综述报告', icon_off: require('@/assets/icon/reports-off.svg'), icon_on: require('@/assets/icon/reports-on.svg') },
        { name: 'collections', label: '收藏夹', icon_off: require('@/assets/icon/collections-off.svg'), icon_on: require('@/assets/icon/collections-on.svg') },
        { name: 'notices', label: '消息通知', icon_off: require('@/assets/icon/notices-off.svg'), icon_on: require('@/assets/icon/notices-on.svg') }
      ]
    }
  },
  methods: {
    selectTab (tabName) {
      this.$emit('tabSelected', tabName) // 发送事件通知父组件选中了哪个选项
      this.selectedTab = tabName // 更新当前选中的选项
      localStorage.setItem('selectedPersonalTab', tabName) // 保存当前选中的选项
    },
    logout () {
      logout().then(() => {
        this.$router.push('/dashboard')
        this.$message({
          message: '退出登录成功',
          type: 'success'
        })
      })
    }
  },
  created () {
    const selectedTab = localStorage.getItem('selectedPersonalTab')
    if (selectedTab) {
      this.selectedTab = selectedTab
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 150px;
  height:100%;
  border-radius: 15px;
  position: fixed;
}

.sidebar h1 {
  text-align: center; /* 标题居中显示 */
  padding: 10px 0; /* 上下留出一定的空白 */
  margin-bottom: 20px; /* 与导航栏之间的间距 */
  border-bottom: 1px solid #ccc; /* 添加底部边框 */
  font-size: 30px;
  color:#409EFF;
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  display: flex;
  align-items: center;
  padding: 10px;
  cursor: pointer;
  transition: box-shadow 0.3s ease, transform 0.3s ease; /* 添加border-color的过渡效果 */
  border-radius: 12px;
}

.sidebar li:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
  position: relative;
  z-index: 1;
}

.sidebar li.active {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
  position: relative;
  z-index: 1;
}

.sidebar li:not(:last-child) {
  margin-bottom: 18px; /* 选项之间的间距 */
}

.label {
  transition: font-size 0.3s;
}

.sidebar li.active .label{
  font-size: 20px; /* 选中时的字体大小 */
}

.icon {
  margin-right: 3px;
}
.logout {
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
