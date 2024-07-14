<template>
  <div>
    <search-form />
    <a-card :bordered="false">
      <a-list
        item-layout="vertical"
        size="large"
        :pagination="pagination"
        :data-source="listData"
      >
        <a-list-item slot="renderItem" key="item.title" slot-scope="item">
          <template v-for="{ type, text } in actions" slot="actions">
            <span :key="type" @click="handleShow(item.id, item.type)">
              <a-icon :type="type" style="margin-right: 8px" />
              {{ text }}
            </span>
          </template>

          <a-space
            direction="vertical"
            slot="extra"
            width="272"
            align="end"
            style="margin-right:20px"
          >
            <a-row>
              <a-col :span="24">
                <a-button
                  type="primary"
                  style="width: 80px"
                  @click="handle(item.id, item.type)"
                >
                  通过
                </a-button>
              </a-col>
            </a-row>

            <a-row>
              <a-col :span="24">
                <a-button
                  type="danger"
                  style="width: 80px"
                  @click="handle(item.id, item.type)"
                >
                  不通过
                </a-button>
              </a-col>
            </a-row>
          </a-space>
          <a-Modal v-model="showDetail" title="Basic Modal" @ok="handleOk" width=750px>
            <template slot="footer">
              <a-button
                key="submit"
                type="primary"
                :loading="loading"
                @click="handleOk"
              >
                通过
              </a-button>
              <a-button
                key="No"
                type="danger"
                :loading="loading"
                @click="handleNo"
              >
                不通过
              </a-button>
              <a-button key="back" @click="handleCancel">
                取消
              </a-button>
            </template>
            <PaperCard v-if="showDetail" v-bind="post" />
          </a-Modal>
          <a-list-item-meta :description="item.description">
            <a slot="title" :href="item.href">{{ item.title }}</a>
            <a-avatar slot="avatar" :src="item.avatar" />
          </a-list-item-meta>

          <a
            style="display:block"
            href="javascript:void(0)"
            @click="handleShow(item.id, item.type)"
            >{{ item.content }}</a
          >
        </a-list-item>
      </a-list>
    </a-card>
  </div>
</template>

<script>
import SearchForm from "./SearchForm";
import PaperCard from './paperCard'

const listData = [];
for (let i = 0; i < 3; i++) {
  listData.push({
    href: "https://www.antdv.com/",
    title: `ant design vue part ${i}`,
    avatar: "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png",
    description:
      "Ant Design, a design language for background applications, is refined by Ant UED Team.",
    content:
      "We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.",
  });
}

export default {
  name: "ArticleList",
  components: { SearchForm,PaperCard, },
  data() {
    return {
      post: {},
      showDetail: false,
      listData,
      pagination: {
        onChange: (page) => {
          console.log(page);
        },
        pageSize: 10,
      },
      actions: [
        { type: "star-o", text: "156" },
        { type: "like-o", text: "156" },
        { type: "message", text: "2" },
      ],
    };
  },
  methods: {
    handleShow: function() {
      this.showDetail = true;
    },
    handleOk(e) {
      console.log(e);
      this.showDetail = false;
    },
    handleCancel(e) {
      console.log(e);
      this.showDetail = false;
    },
  },
};
</script>

<style lang="less" scoped>
.extra {
  width: 272px;
  height: 1px;
}
.content {
  .detail {
    line-height: 22px;
    max-width: 720px;
  }
  .author {
    color: @text-color-second;
    margin-top: 16px;
    line-height: 22px;
    & > :global(.ant-avatar) {
      vertical-align: top;
      margin-right: 8px;
      width: 20px;
      height: 20px;
      position: relative;
      top: 1px;
    }
    & > em {
      color: @disabled-color;
      font-style: normal;
      margin-left: 16px;
    }
  }
}
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
