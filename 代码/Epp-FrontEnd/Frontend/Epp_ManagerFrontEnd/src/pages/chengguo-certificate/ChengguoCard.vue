<template>
    <div>
      <a-card :bordered="false" dis-hover>
        <div slot="name">
          申请人：
          <a href="javascript:0">{{this.$props.name}}</a>
        </div>
        <a-Row>
          发布者: {{name}}
        </a-Row>
        <br />
        <a-Row>
          成果作者: {{scholars}}
        </a-Row>
        <br />
        <a-Row>
          成果名: {{result_name}}
        </a-Row>
        <br />
        <a-Row>
          成果描述: {{work_description}}
        </a-Row>
        <br />
        <a-Row>
          领域: {{field}}
        </a-Row>
        <br />
        <a-Row>
          成果示意图：<img :src="result_pic" width="600px">
        </a-Row>
      </a-card>
    </div>
  </template>
  
  <script>
  export default {
    name: "WorkCard",
    props: {
      name: {
        type: String,
        default: "未命名"
      },
      scholars: {
        type: String,
        default: "未命名"
      },
      result_name: {
        type: String,
        default: "未命名"
      },
      work_description: {
        type: String,
        default: "未命名"
      },
      field: {
        type: String,
        default: "未命名"
      },
      result_pic: {
        type: String,
        default: "未命名"
      },
    }
  }
  </script>
  
  <style scoped>
  
  </style>
  