<template>
  <a-card :bordered="false" class="search-form">
    <div
      :class="['search-head', layout, pageWidth]"
      style="text-align:center;margin-top:20px"
    >
      <div class="search-input">
        <a-input-search
          class="search-ipt"
          style="width:75%"
          placeholder="请输入..."
          size="large"
          enterButton="搜索"
        />
      </div>
    </div>
    <a-form :form="form" id="searchForm">
      <form-row label=" ">
        <a-form-item> </a-form-item>
      </form-row>
      <form-row label="所属类目：">
        <a-form-item>
          
            <template v-for="tag in tags">
            <a-checkable-tag
              :key="tag"
              class="tag-default"
              :checked="selectedTags.indexOf(tag) > -1"
              @change="(checked) => handleChange(tag, checked)"
            >
              {{ tag }}
            </a-checkable-tag>
          </template>
          
          
        </a-form-item>
      </form-row>
    </a-form>
  </a-card>
</template>

<script>
// import TagSelect from "../../../components/tool/TagSelect";
import FormRow from "../../../components/form/FormRow";
import { mapState } from "vuex";
// const TagSelectOption = TagSelect.Option;

export default {
  name: "SearchForm",
  components: { FormRow},
  data() {
    return {
      form: this.$form.createForm(this),
      
      tags: ["Movies", "Books", "Music", "Sports"],
      selectedTags: ["Movies", "Books", "Music", "Sports"],
    };
  },
  computed: {
    ...mapState("setting", ["layout", "pageWidth"]),
  },
  methods: {
    lookMyself() {
      this.form.setFieldsValue({
        owner: "3",
      });
    },
    formReset() {
      document.getElementById("searchForm").reset(),
        console.log(this.id),
        this.$message.info("已重置");
    },
    handleChange(tag, checked) {
      const { selectedTags } = this;
      const nextSelectedTags = checked
        ? [...selectedTags, tag]
        : selectedTags.filter((t) => t !== tag);
      console.log("You are interested in: ", nextSelectedTags);
      this.selectedTags = nextSelectedTags;
    },
  },
};
</script>

<style lang="less" scoped>
.search-form {
  margin-bottom: 24px;
}
.tag-default{
    font-size: 14px;
    padding: 0 8px;
    height: auto;
    margin-right: 24px;
  }
</style>
