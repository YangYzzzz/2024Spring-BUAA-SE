<template>
  <el-menu class="navbar has-shadow" :class="{ 'trans-menu': isTop }" role="navigation" aria-label="" style="position: fixed; width: 100%; top: 0;">
    <div class="container">
      <div class="navbar-brand">
        <a href="" class="navbar-item-logo">
          <img src="../../static/favicon.png" alt="Epp" width="42" height="42">
          <img src="../assets/title.png" class="title" alt="title">
        </a>
        <a role="button" class="navbar-burger" :class="{ 'is-active': isMenuActive }" @click="toggleMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" :class="{ 'is-active': isMenuActive }">
        <div class="navbar-start">
          <router-link to="/search" class="navbar-item" :class="{ 'selected-tab': selectedTab === 'search'}" @click.native="selectTab('search', $event)">文献调研</router-link>
          <router-link to="/upload" class="navbar-item" :class="{ 'selected-tab': selectedTab === 'upload'}" @click.native="selectTab('upload', $event)">全文解读</router-link>
          <router-link to="/personal" class="navbar-item" :class="{ 'selected-tab': selectedTab === 'personal'}" @click.native="selectTab('personal', $event)">个人中心</router-link>
          <router-link to="/aboutus" class="navbar-item" :class="{ 'selected-tab': selectedTab === 'aboutus'}" @click.native="selectTab('aboutus', $event)">关于我们</router-link>
        </div>
        <transition name="fade-avatar">
          <div class="navbar-end" v-if="selectedTab !== 'personal'">
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                  <img :src="avatar" alt="Profile Icon" class="profile-icon">
              </span>
              <el-dropdown-menu slot="dropdown" class="down-menu">
                <el-dropdown-item disabled class="down-menu-item">
                  <div class="profile-details">
                    <p class="username">用户名：{{ username }}</p>
                  </div>
                </el-dropdown-item>
                <el-dropdown-item command="logout" class="down-menu-item">
                  <img src="@/assets/icon/logout.svg" alt="Logout Icon" style="width: 18px; height: 18px; margin-right: 2px;">
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
      </transition>
      </div>
    </div>
  </el-menu>
</template>

<script>
import { logout, fetchUserInfo } from '@/request/userRequest.js'
import { EventBus } from '../utils/eventBus'
export default {
  name: 'NavBar',
  data () {
    return {
      isTop: true,
      selectedTab: '',
      isMenuActive: false,
      avatar: '',
      username: ''
    }
  },
  watch: {
    $route (to, from) {
      this.updateSelectedTab()
    }
  },
  created () {
    this.updateSelectedTab()

    var username = localStorage.getItem('username')
    if (username) {
      this.username = username
    } else {
      fetchUserInfo().then(res => {
        this.username = res.data.username
      })
    }
    var avatar = localStorage.getItem('avatar')
    if (avatar) {
      this.avatar = avatar
    } else {
      fetchUserInfo().then(res => {
        this.avatar = res.data.avatar
      })
    }

    fetchUserInfo()
    EventBus.$on('updateAvatar', avatar => {
      this.avatar = avatar
    })
  },
  mounted () {
    window.addEventListener('scroll', this.handleScroll)
  },
  destroyed () {
    window.removeEventListener('scroll', this.handleScroll)
    EventBus.$off('updateAvatar')
  },
  methods: {
    updateSelectedTab () {
      if (this.$route.path.includes('/search')) {
        this.selectedTab = 'search'
      } else if (this.$route.path.includes('/upload')) {
        this.selectedTab = 'upload'
      } else if (this.$route.path.includes('/personal')) {
        this.selectedTab = 'personal'
      } else if (this.$route.path.includes('/aboutus')) {
        this.selectedTab = 'aboutus'
      } else {
        this.selectedTab = ''
      }
    },
    handleScroll () {
      this.isTop = window.scrollY === 0
    },
    selectTab (tabName, event) {
      this.selectedTab = tabName
      event.target.blur()
      this.isMenuActive = false
    },
    toggleMenu () {
      this.isMenuActive = !this.isMenuActive
    },
    logout () {
      logout().then(() => {
        this.$router.push('/dashboard')
        this.$message({
          message: '退出登录成功',
          type: 'success'
        })
      })
    },
    handleCommand (command) {
      if (command === 'logout') {
        this.logout()
      }
    }
  }
}
</script>

<style scoped>
@import "../../static/css/bulma.css";
.trans-menu {
  background-color: transparent !important;
  box-shadow: none !important;
}
.navbar-item {
  margin-top: 2px;
  background-color: transparent; /* 设置背景颜色 */
  transition: box-shadow 0.3s ease, transform 0.3s ease, color 0.3s ease, font-size 0.3s ease; /* 添加过渡效果 */
  border-radius: 12px;
  text-decoration: none;
}
.navbar-item:hover {
  text-decoration: none;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
  position: relative;
  z-index: 1;
}
.navbar-item-logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: #485fc7;
}
.selected-tab {
  color: #485fc7;
  font-size: 20px;
}
.navbar-burger {
  display: none;
}

@media screen and (max-width: 768px) {
  .navbar-burger {
    display: block;
  }

  .navbar-menu {
    display: none;
  }

  .navbar-menu.is-active {
    display: block;
  }
}

.navbar-end {
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-icon {
  border-radius: 50%;
  width: 38px;
  height: 38px;
  cursor: pointer;
}

.down-menu {
  width: 150px;
  border-radius: 12px;
}

.down-menu-item {
  padding: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 0.95rem;
  border-radius: 12px;
}

.fade-avatar-enter-active, .fade-avatar-leave-active {
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
}
.fade-avatar-enter, .fade-avatar-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.title {
  margin-left: 0px;
  padding-top: 1px;
  width: 130px;
  height: 42px;
}
</style>
