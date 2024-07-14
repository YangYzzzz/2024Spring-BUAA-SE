<template>
  <div>
    <a-card :bordered="false" dis-hover>
      <div slot="name">
        申请人：
        <a href="javascript:0">{{this.$props.name}}</a>
      </div>
      <a-Row>
        企业名称: {{name}}
      </a-Row>
      <br />
      <a-Row>
        地址: {{address}}
      </a-Row>
      <br />
      <a-Row>
        企业网址: {{website}}
      </a-Row>
      <br />
      <a-Row>
        联系电话：{{phone}}
      </a-Row>
      <br />
      <a-Row>
        法人代表: {{legal_representative}}
      </a-Row>
      <br />
      <a-Row>
        领域: {{field}}
      </a-Row>
      <br />
      <a-Row>
        企业简介: {{instruction}}
      </a-Row>
      <br />
      <a-Row>
        营业执照：<img :src="business_license" width="600px">
      </a-Row>
      <br />
      <a-Row>
        法人身份证：<img :src="legal_person_ID" width="600px">
      </a-Row>
    </a-card>
  </div>
</template>

<script>
export default {
  name: "EnterpriseCard",
  props: {
    name: {
      type: String,
      default: "未命名"
    },
    address: {
      type: String,
      default: "未命名"
    },
    website: {
      type: String,
      default: "未命名"
    },
    instruction: {
      type: String,
      default: "未命名"
    },
    phone: {
      type: String,
      default: "未命名"
    },
    legal_representative: {
      type: String,
      default: "未命名"
    },
    register_capital: {
      type: String,
      default: "未命名"
    },
    field: {
      type: String,
      default: "未命名"
    },
    business_license: {
      type: String,
      default: "未命名"
    },
    legal_person_ID: {
      type: String,
      default: "未命名"
    },
  }
}
</script>

<style scoped>

</style>
