<template>
    <div class="column paper-card">
        <div>
            <router-link :to="{ name: 'paper-info', params: { paper_id: paper.paper_id } }"
                class="is-size-5 has-text-weight-bold" style="text-align: left; display: block;">
                {{ paper.title }}
            </router-link>
        </div>
        <div style="text-align: left;">
          <el-tag size="mini" v-for="subclass in paper.sub_classes" :key="subclass" type="warning" style="margin-right: 5px">
            {{ subclass }}
          </el-tag>
        </div>
        <div style="text-align: left;">
            <el-tag size="mini">
                {{ getPublicationYear(paper.publication_date) }}
            </el-tag>
            <span class="is-size-6">- {{ paper.authors }}</span>
        </div>
        <div style="text-align: left;">
            <span class="is-size-7">
                <span class="mr-3 truncate-multiline">{{ paper.abstract }}</span>
            </span>
        </div>
    </div>
</template>

<script>
export default {
  props: {
    paper: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
    }
  },
  methods: {
    getPublicationYear (dateString) {
      return new Date(dateString).getFullYear()
    }
  }
}
</script>

<style scoped>
.paper-card {
  background-color: white;
  border-radius: 6px;
  box-shadow: 0 0.5em 1em -0.125em rgba(10, 10, 10, 0.1), 0 0px 0 1px rgba(10, 10, 10, 0.02);
  color: #4a4a4a;
  display: block;
  padding: 1.25rem;
  margin-bottom: 20px;
  margin-right: 0.25rem;
  /* word-break: break-word; */
}

.truncate-multiline {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  /* 设置为2行文本 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
  /* 重写可能的 nowrap */
  max-height: 3em;
  /* 可选，基于行高和所需行数调整 */
}
</style>
