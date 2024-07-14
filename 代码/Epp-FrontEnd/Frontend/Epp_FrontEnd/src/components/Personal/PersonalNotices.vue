<template>
  <div class="collections">
    <el-row>
      <el-col :span="24">
        <h1 class="noticesTitle">通知消息</h1>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-card class="table-card">
          <div class="table-header">
            <div v-if="unreadSum > 0" class="unread">你还有{{ unreadSum }}条未读消息！</div>
            <div v-else class="unread">暂时没有未读消息啦~</div>
            <!-- 选择全部或者未读/已读 -->
            <el-radio-group v-model="showMode" @change="changeTable" class="radio-group">
              <el-radio-button label="1">全部</el-radio-button>
              <el-radio-button label="2">未读</el-radio-button>
            </el-radio-group>
          </div>
          <el-table :data="displayedNotifications" v-loading="loading" style="width: 100%; min-height: 400px;" :default-sort = "{prop: 'date', order: 'descending'}">
            <el-table-column prop="title" label="通知标题">
              <template slot-scope="scope">
                <el-link class="notice-link" :underline="false" type="primary" @click="showModal(scope.row)">{{ scope.row.title }}</el-link>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="日期" align="center" sortable></el-table-column>
            <el-table-column label="状态" align="center">
              <template slot-scope="scope">
                <el-tag v-if="scope.row.is_read" type="success">已读</el-tag>
                <el-tag v-else type="danger">未读</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <el-button-group>
                  <el-button type="primary" size="small" icon="el-icon-check" @click="toggleRead(scope.row)"></el-button>
                  <el-button type="primary" size="small" icon="el-icon-delete" @click="deleteDocument(scope.row.notification_id)"></el-button>
                </el-button-group>
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
    <el-dialog :visible.sync="modalShow" title="消息内容">
      <p class="notice-content">{{ selectedNotification.content }}</p>
    </el-dialog>
  </div>
</template>

<script>
import { fetchNotification, deleteNotification, readNotification } from '@/request/userRequest.js'
export default {
  data () {
    return {
      notifications: [],
      allNotifications: [],
      currentPage: 1,
      itemsPerPage: 6,
      unreadSum: 0,
      modalShow: false,
      selectedNotification: {},
      showMode: '1',
      loading: true
    }
  },
  computed: {
    totalRecords () {
      return this.notifications.length
    },
    totalPages () {
      return Math.ceil(this.totalRecords / this.itemsPerPage)
    },
    displayedNotifications () {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.notifications.slice(start, end)
    }
  },
  methods: {
    async fetchDocuments (id) {
      try {
        var params = { mode: parseInt(id) }
        if (id === 2) {
          console.log(2)
          var res = (await fetchNotification({params})).data
          // 按照date排序
          res.notifications.sort((a, b) => {
            return new Date(b.date) - new Date(a.date)
          })
          this.notifications = res.notifications
          this.allNotifications = res.notifications
        } else {
          console.log(id)
          res = (await fetchNotification({params})).data
          this.unreadSum = res.total
        }
        this.loading = false
      } catch (error) {
        console.log('error:fetchDocuments')
      }
    },
    async deleteDocument (id) {
      try {
        // eslint-disable-next-line camelcase
        var notification_ids = []
        notification_ids.push(id)
        var data = {notification_ids}
        var res = await deleteNotification({data})
        console.log(res)
        this.$notify({
          title: '成功',
          message: '删除消息成功！',
          type: 'success'
        })
      } catch (error) {
        console.log('error:deleteNotification')
      }
      this.fetchDocuments(1)
      this.fetchDocuments(2)
    },
    async read (id) {
      try {
        var data = {notification_id: id}
        await readNotification(data)
        this.fetchDocuments(1)
      } catch (error) {
        console.log('error:read')
      }
    },
    changePage (page) {
      this.currentPage = page
    },
    showModal (notification) {
      this.selectedNotification = notification
      this.toggleRead(notification)
      this.modalShow = true
    },
    toggleRead (notification) {
      if (notification.is_read) {
        return
      }
      this.read(notification.notification_id)
      this.$notify({
        title: '成功',
        message: '消息标记为已读！',
        type: 'success'
      })
      notification.is_read = true
    },
    changeTable () {
      if (this.showMode === '1') {
        this.notifications = this.allNotifications
      } else {
        this.notifications = this.allNotifications.filter(item => !item.is_read)
      }
    }
  },
  mounted () {
    this.fetchDocuments(1)
    this.fetchDocuments(2)
  }
}
</script>

<style scoped>
/* 可以添加样式来美化表格 */

.noticesTitle{
   font-size: 30px;
  font-weight: bold;
  margin-bottom: 20px;
  color:rgb(18, 19, 18);
}
.table-card {
  border-radius: 12px;
}

/*链接样式*/
.notice-link {
  color: #409EFE;
  text-decoration: none;
}
.notice-link:hover {
  opacity: 0.8;
  text-decoration: none;
}
/*消息弹窗*/
/deep/ .el-dialog{
  border-radius: 12px;
}
.notice-content{
  font-size: 16px;
  font-weight: bold;
}
/*未读消息*/
.unread{
  font-size: 18px;
  font-weight: bold;
  color:rgb(18, 19, 18);
}
.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-left: 10px;
  padding-right: 50px;
}
</style>
