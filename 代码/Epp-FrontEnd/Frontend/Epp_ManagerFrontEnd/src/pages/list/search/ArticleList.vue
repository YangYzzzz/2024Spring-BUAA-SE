<template>
  <div>
    <!--<search-form />-->
    <a-card :bordered="false">
      <a-spin :spinning="loading">
      <a-list
        item-layout="vertical"
        size="large"
        :pagination="pagination"
        :data-source="listData"
      >
        <a-list-item slot="renderItem" key="item.title" slot-scope="item">
          <template slot="actions">
            <span>
              <a-icon type="star-o" style="margin-right: 8px" />
              {{ item.startext }}
            </span>
            <span>
              <a-icon type="eye" style="margin-right: 8px" />
              {{ item.read }}
            </span>
            <span>
              <a-icon type="like-o" style="margin-right: 8px" />
              {{ item.liketext }}
            </span>
            <span>
              <a-icon type="download" style="margin-right: 8px" />
              {{ item.download }}
            </span>
            <span>
              <a-icon type="fire" style="margin-right: 8px" />
              {{ item.score }}
            </span>
            <span >
              <a-icon type="clock-circle" style="margin-right: 8px" />
              {{ item.messagetext }}
            </span>
          </template>

          <a-space
            direction="vertical"
            slot="extra"
            width="272"
            align="end"
            style="margin-right:20px;"
          >
          </a-space>

          <a-list-item-meta >
            <a slot="title" :href="item.href">
    <a-icon type="book" style="margin-right: 8px;" /> <!-- 使用 margin-right 添加图标和标题之间的间距 -->
    {{ item.title }}
  </a>
          </a-list-item-meta> 
          <a
  style="display: block"
  class="textbreak"
  href="javascript:void(0)"
>
  <a-icon type="user" style="margin-right: 8px;" /> <!-- 使用 margin-right 添加图标和文本之间的间距 -->
  {{ item.content | ellipsis }}
</a>
        </a-list-item>
      </a-list>
      </a-spin>
    </a-card>
  </div>
</template>

<script>
// import SearchForm from "./SearchForm";
import editor from "@/pages/components/editor/editor.vue";
import PaperCard from "./paperCard";
import { getWorkAll} from '../../../services/work';
const listData = [];

export default {
  filters: {
    ellipsis (value) {
      if (!value) return ''
      if (value.length > 130) {
        return value.slice(0,130) + '...'
      }
      return value
    }
  },
  name: "ArticleList",
  components: { PaperCard, editor},
  data() {
    return {
       loading: false, 
      pageIndex: 1,
      data: [],
      totalCnt: 1,
      showCutter: false,
      post: {},
      interpretation: {},
      postType: 0,
      InterpretationeType: 0,
      postSelectType: "论文解读",
      projectTotalCnt: 1,
      projectList: [],
      showDetail: false,
      showModify: false,
      listData,
      pagination: {
        onChange: (page) => {
          console.log(page);
          this.handlePageChange(page)
        },
        current: 1, // 设置当前页
        total: 0,   // 总条目数
        pageSize: 5,
      },
      actions: [
        { type: "star-o", text: "" },
        { type: "like-o", text: "" },
        { type: "message", text: "" },
      ],
    };
  },

  mounted() {
    this.init();
  },

  methods: {
    init: async function() {
      this.loadPost();
    },
    handlePageChange(page) {
      this.pagination.current = page;
      this.loadPost();
    },
    loadPost: async function() {
      this.loading = true;
      var params={
                  keyword:"",
                  page_num:this.pagination.current,
                  page_size:this.pagination.pageSize,
              }
        console.log("size")
        console.log(params)
        try{
        await getWorkAll({params}).then((oriRes) => {
        console.log(oriRes)
        console.log('response')
        console.log(oriRes);
        let res = oriRes.data
        console.log(res);
        listData.length=0;
        this.pagination.total = res.total; 
        // this.listData = {};
        console.log('length')
        console.log(res.papers.length)
        for (let i = 0; i < res.papers.length; i++) {
            listData.push({
                 id:res.papers[i].paper_id,
                 href: "javascript:0",
                 title:res.papers[i].title,
                 content:res.papers[i].authors[1],
                 messagetext:res.papers[i].publication_date,
                //  description:res.papers[i].journal,
                //  citation:res.papers[i].citation_count,
                 read:res.papers[i].read_count,
                 liketext:res.papers[i].like_count,
                 startext:res.papers[i].collect_count,
                 download:res.papers[i].download_count,
                 score:res.papers[i].score,
                });
        }
      })} catch (error) {
        console.error("Failed to load data:", error);
      } finally {
        console.log('listData')
      console.log(listData)
      console.log('over')
        console.log('加载完成')
        this.loading = false;  // 请求完成后设置 loading 状态为 false
      }
    },
  },
};
</script>

<style lang="less" scoped>
.textbreak .text-div {
    word-break: break-all;
}


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
