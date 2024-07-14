<template>
  <div class="new-page" :style="`min-height: ${pageMinHeight}px`">
    <h2>接口测试</h2>
    <span>请输入API地址(只测试GET请求)</span>
    <a-input-search
      placeholder="input a API"
      size="large"
      @search="onSearch"
      v-model="api_str"
      :loading="loading"
      @click="test"
    >
      <a-button slot="enterButton" type="primary"> 请求此API </a-button>
    </a-input-search>
    <a-divider></a-divider>
    <h3>{{ rev_data1 }}</h3>

  </div>
</template>
 
<script>
import {mapState} from 'vuex'
import {api_get_test,followerList} from "@/services/testapi";
export default {
  data() {
    return {
      api_str: "https://api.apiopen.top/singlePoetry",
      loading: false,
      rev_data: "收到的响应",
      rev_data1:'',
    };
  },
   computed: {
      ...mapState('setting', ['pageMinHeight']),
    },
  methods: {
    onSearch() {
      this.loading = true;
      api_get_test(this.api_str)
        .then((result) => {
          this.loading = false;
          this.rev_data = result;
        })
        .catch((err) => {
          this.rev_data = err;
        });
      console.log(this.rev_data1);
    },

    test(){
      this.loading=true;
      followerList(1).then((result)=>{
          this.loading=false;
          this.rev_data1=result;
      })
      .catch((err)=>{
        this.rev_data1=err;
      });
    },
    
  },
};
</script>
 
<style scoped lang="less">
@import "index.less";
</style>
