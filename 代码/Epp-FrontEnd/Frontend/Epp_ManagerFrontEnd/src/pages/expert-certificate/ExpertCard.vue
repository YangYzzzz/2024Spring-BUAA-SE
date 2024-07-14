<template>
  <div>
    <a-card :bordered="false" dis-hover>
      <div slot="name">
        申请人：
        <a href="javascript:0">{{this.$props.name}}</a>
      </div>
        <a-Row>
          姓名: {{name}}
        </a-Row>
        <br />
        <a-Row>
          身份证号码: {{ID_num}}
        </a-Row>
        <br />
        <a-Row>
          电话号码: {{phone}}
        </a-Row>
        <br />
        <a-Row>
          身份证照片：
          <img :src="ID_pic" width="600px"></img>
        </a-Row>
        <br />
        <a-Row>
          组织: {{organization}}
        </a-Row>
        <br />
        <a-Row>
          领域: {{field}}
        </a-Row>
        <br />
        <a-Row>
          个人简介: {{self_profile}}
        </a-Row>
    </a-card>
  </div>
</template>

<script>
import {Image} from "antd";
export default {
  name: "ExpertCard",
  components: {Image},
  props: {
    name: {
      type: String,
      default: "未命名",
    },
    ID_num: {
      type: String,
      default: ""
    },
    organization: {
      type: String,
      default: "无组织"
    },
    field: {
      type: String,
      default: ""
    },
    self_profile: {
      type: String,
      default: "个人简介"
    },
    phone: {
      type: String,
      default: ""
    },
    ID_pic: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      // name: this.$props.name,
      // ID_num: this.$props.ID_num,
      // organization: this.$props.organization,
      // field: this.$props.field,
      // self_profile: this.$props.self_profile,
      // phone: this.$props.phone,
      // ID_pic: this.$props.ID_pic
    }
  },
  methods: {

  }
}
</script>

<style scoped>

</style>
