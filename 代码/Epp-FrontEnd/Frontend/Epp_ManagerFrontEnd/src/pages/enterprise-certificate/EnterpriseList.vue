<template>
  <div>
    <a-card :bordered="false">
      <a-list item-layout="vertical" size="large" :pagination="pagination" :data-source="listData">
        <a-list-item slot="renderItem" key="item.title" slot-scope="item">
          <a-space direction="vertical" slot="extra" width="272" align="end" style="margin-right:20px;">
            <a-row>
              <a-col :span="24">
                <a-button
                    type="text"
                    style="width: 80px"
                    @click="handleShow(item.id)"
                >
                  查看
                </a-button>
              </a-col>
            </a-row>

            <a-row>
              <a-col :span="24">
                <a-popconfirm
                    title="确定通过认证吗？"
                    ok-text="确定"
                    cancel-text="取消"
                    @confirm="handleApply(item.id)"
                >
                  <a-button type="primary" style="width: 80px"> 通过</a-button>
                </a-popconfirm>
              </a-col>
            </a-row>

            <a-row>
              <a-col :span="24">
                <a-popconfirm
                    title="确定要拒绝认证吗？"
                    ok-text="确定"
                    cancel-text="取消"
                    @confirm="handleRefuse(item.id)"
                >
                  <a-button type="danger" style="width: 80px"> 拒绝</a-button>
                </a-popconfirm>
              </a-col>
            </a-row>
          </a-space>
          <a-modal v-model="showDetail" title="" @ok="handleOk" width="750px">
            <EnterpriseCard v-if="showDetail" v-bind="post"></EnterpriseCard>
          </a-modal>
          <a-list-item-meta :description="item.create_time">
            <a slot="title" :href="item.href">{{ item.username }}</a>
            <a-avatar slot="avatar" :src="item.userpic" />
          </a-list-item-meta>
          <a
              style="display:block"
              class="textbreak"
              href="javascript:void(0)"
              @click="handleShow(item.id)"
          >企业简介：{{item.profile|ellipsis}}          </a>
        </a-list-item>
      </a-list>
    </a-card>
  </div>
</template>

<script>
import {enterpriseApply, enterpriseRefuse, getEnterprise, getEnterpriseAll} from "../../services/enterprise";
import {BASE_URL_IP} from "../../services/api"
import EnterpriseCard from "./EnterpriseCard";


export default {
  name: "EnterpriseList",
  components: {EnterpriseCard},
  filters: {
    ellipsis (value) {
      if (!value) return ''
      if (value.length > 130) {
        return value.slice(0,130) + '...'
      }
      return value
    }
  },
  data() {
    return {
      loading: true,
      pageIndex: 1,
      data: [],
      post: {},
      showDetail: false,
      //翻页
      pagination: {
        onChange: (page) => {
          console.log(page);
        },
        pageSize: 10,
      },
      listData: [],
    }
  },
  mounted() {
    this.init();
  },
  inject:[
    'reload'
  ],
  methods: {
    init: async function() {
      this.loadPost();
    },
    loadPost: function () {
      this.loading = true;
      getEnterpriseAll().then((res) => {
        console.log(res);
        this.listData.length = 0;
        this.listData = [];
        for (let i = 0; i < res.data.length; i++) {
          this.listData.push({
            id: res.data[i].id,
            username: res.data[i].username,
            userpic: BASE_URL_IP + '/api/' + res.data[i].userpic,
            nickname: res.data[i].nickname,
            email: res.data[i].email,
            institution: res.data[i].institution,
            usertype: res.data[i].usertype,
            total_post: res.data[i].total_post,
            total_like: res.data[i].total_like,
            total_fan: res.data[i].total_fan,
            type :res.data[i].type,
            profile: res.data[i].profile,
            create_time: "申请时间：" + res.data[i].create_time
          })
        }
        this.loading = false;
        console.log(this.listData);
        console.log(BASE_URL_IP);
      }).catch((error) => {
        console.log(error);
      });
    },
    handleOk(e) {
      this.showDetail = false;
    },
    handleShow: function (id) {
      getEnterprise(id, "get").then((res) => {
        this.post = {
          name : res.data.name,
          address: res.data.address,
          website: res.data.website,
          instruction: res.data.instruction,
          phone: res.data.phone,
          legal_representative: res.data.legal_representative,
          register_capital: res.data.register_capital,
          field: res.data.field,
          business_license: BASE_URL_IP + '/api/' + res.data.business_license,
          legal_person_ID: BASE_URL_IP + '/api/' + res.data.legal_person_ID,
        };
        this.showDetail = true;
        console.log(this.post);
      }).catch((error) => {
        console.log(error);
      })
    },
    handleRefuse: function (id) {
      enterpriseRefuse(id, "get").then((res) => {
        console.log(res);
        this.reload();
      }).catch((error) => {
        console.log(error);
        this.reload();
      });
    },
    handleApply: function (id) {
      enterpriseApply(id, "get").then((res) => {
        console.log(res);
        this.reload();
      }).catch((error) => {
        console.log(error);
        this.reload();
      });
    }
  }
}
</script>

<style scoped>
a:link {
  color: black;
} /* 未被访问的链接 */
a:hover {
  color: #13c2c2;
} /* 鼠标指针移动到链接上 */
a:active {
  color: #13c2c2;
} /* 正在被点击的链接 */
</style>
