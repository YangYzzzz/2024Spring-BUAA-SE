<template>
  <a-card :bordered="false">
    <h2>选择用户类型</h2>
    <a-space>
      <a-input-search
          v-model="searchText"
          placeholder="请输入用户名"
          enter-button
          @search="onSearch()"
          style="width: 300px;margin-left: 10px;"
        />
    </a-space>
    <br/>
    <br/>
    <a-table :data-source="data" :columns="columns" :pagination="pagination" :key="itemKey">
      <template
        v-for="col in ['name', 'password']"
        :slot="col"
        slot-scope="text, record"
      >
        <div :key="col">
          <a-input
            v-if="record.editable"
            style="margin: -5px 0"
            :value="text"
            @change="(e) => handleChange(e.target.value, record, col)"
          />
          <template v-else>
            {{ text }}
          </template>
        </div>
      </template>
      <template slot="operation" slot-scope="text, record">
        <div class="editable-row-operations">
          <span v-if="record.editable">
            <a-space>
              <a @click="() => save(record.key)">Save</a>
              <a-popconfirm
                title="Sure to cancel?"
                @confirm="() => cancel(record.key)"
              >
                <a>Cancel</a>
              </a-popconfirm>
            </a-space>
          </span>
          <span v-else>
            <a :disabled="editingKey !== ''" @click="() => edit(record.key)"
              >Edit</a
            >
          </span>
        </div>
        <a-popconfirm
          v-if="data.length"
          title="Sure to delete?"
          @confirm="() => onDelete(record.key)"
        >
          <a href="javascript:0;">Ban</a>
        </a-popconfirm>
      </template>
    </a-table>


  </a-card>
</template>

<script>
import { message } from 'antd';
import { getUserAll,
        UserDel, 
        UserModify,
        getSelectUser,
        adminCreateCompanyAPI,
        adminCreateExpertAPI,
        adminCreateUserAPI,
        searchUser } from "../../../services/dataSource";
const columns = [
  {
    title: "用户名",
    dataIndex: "name",
    width: "20%",
    scopedSlots: { customRender: "name" },
  },
  {
    title:"密码",
    dataIndex:"password",
    width:"20%",
    scopedSlots:{customRender:"password"},
  },
  // {
  //   title: "邮箱",
  //   dataIndex: "email",
  //   width: "25%",
  //   scopedSlots: { customRender: "email" },
  // },
  {
    title: "操作",
    dataIndex: "operation",
    scopedSlots: { customRender: "operation" },
  },
];
const data = [];

export default {
  name: "UserForm",
  inject: ['reload'],
  i18n: require("./i18n-user"),
  data() {
    this.cacheData = data.map((item) => ({ ...item }));
    return {
      type:"",
      type1:0,
      data,
      columns,
      form: this.$form.createForm(this),
      user_info:{
        username:'',
        password:'',
      },
      user_visible: true,
      searchText: '',
      editingKey: "",
      editData: {},
      changeable: true,
      selectedType: "全部",
      pagination: {
        current: 1,
        onChange: (page) => {
          if (!this.changeable) {
            alert("请完成修改后再切换页面！")
            return
          }
          this.$forceUpdate()
          console.log('Page-->')
          console.log(page);
          console.log('paginationselectedType='+this.selectedType);
          if (this.selectedType=="搜索") {
            var params = {
              "keyword": this.searchText,
              "page_num": current,
               "page_size":20,
            }
            searchUser(params).then((oriRes) => {
              console.log('searching');
              // console.log(res.data.all_page)
              console.log(oriRes);
              let res = oriRes.data
              
              console.log(res);
              data.length = 0;
              console.log(data);

              for (let i = 0; i < res.total; i++) {
                
                data.push({
                  // key: res.data[i].id,
                  name: res.users[i].username,
                  password: res.users[i].password,
                  // email: res.data[i].email,
                 editable: true
                });
              }

              this.cacheData = data.map((item) => ({ ...item }));
              this.totalCnt +=res.total;
              this.pagination.total =res.total;
              this.loading = false;
              this.itemKey = Math.random();
              this.pagination.current = page;

            }).catch((error) => {
              console.log(error);
            });

          } else {
            var params = {
          "keyword": "",
          "page_num": this.pagination.current,
          "page_size":20,
      }
           getSelectUser(params).then((oriRes) => {
        for (let i = 0; i < data.length; i++) {
          data[i].target = false;
        }
        console.log(oriRes);
        let res = oriRes.data
        console.log(res);
        data.length = 0;
        for (let i = 0; i < res.total; i++) {
          data.push({
            name: res.users[i].username,
            password: res.users[i].password,
            // email: res.users[i].email,
            // email:"21373005@buaa.edu.cn"
          });
        }
        this.cacheData = data.map((item) => ({ ...item }));
        // this.totalCnt += res.total;
        // console.log("total="+res.total)
        this.loading = false;
        this.pagination.total =res.total;
        this.pagination.current = page;
        console.log(data)
        console.log(this.cacheData)
      }).catch((error) => {
        console.log(error);
      });


          }



          
        },
        total: 10
      },
      itemKey: "",
    };
  },
  watch: {
    editingKey: function (newValue) {
      this.changeable = newValue === "";
    }
  },

  mounted() {
    this.init();
  },

  methods: {
    // ...mapMutations("account", ["setPage"]),
    init: async function() {
      this.loadUser();
    },

    loadUser: function() {
      this.loading = true;
      data.length=0;
      this.pagination.current = 1;
      var params = {
          "keyword": "",
          "page_num": this.pagination.current,
          "page_size":20,
      }
      getSelectUser(params).then((oriRes) => {
        for (let i = 0; i < data.length; i++) {
          data[i].target = false;
        }
        console.log(oriRes);
        let res = oriRes.data
        console.log(res);
        data.length = 0;
        for (let i = 0; i < res.total; i++) {
          data.push({
            name: res.users[i].username,
            password: res.users[i].password,
          });
        }
        this.cacheData = data.map((item) => ({ ...item }));
        this.totalCnt = res.total;
        this.loading = false;
        this.pagination.total = res.total;
        console.log(data)
        console.log(this.cacheData)
      }).catch((error) => {
        console.log(error);
      });
    },
    onDelete(key) {
      const newData = [...this.data];
      this.data = newData.filter((item) => item.key !== key);
      const target = newData.filter((item) => key === item.key)[0];
      const params = {
        id:target.key,
        name: target.name,
        usertype: this.type1,
        institution:target.ins,
        mail: target.email,
      };
      let that = this
      UserDel(params)
        .then((res) => {
          this.$message.info("成功删除");
          // this.loadUser();
          console.log(res)
        }).then((res) => {
          that.reload()
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleChange(value, record, col) {
      if (!this.editData.key) {
        this.editData = record
      }
      if (col === "name") {
        this.editData.name = value;
      } else if (col === 'ins') {
        this.editData.ins = value;
      } else if (col === 'email') {
        /*todo*/
        this.editData.email = value;
      } else if (col === 'type') {
        alert("暂不允许修改用户类型！！")
        this.reload()
      }
      console.log(this.editData)

      this.loadUser()
    },
    edit(key) {
      const newData = [...this.data];
      const target = newData.filter((item) => key === item.key)[0];
      console.log(target)
      this.editingKey = key;
      if (target) {
        target.editable = true;
        this.data = newData;
      }
    },
    // edit(key) {
    //   const target = data.filter((item) => key === item.key)[0];
    //     this.editingKey = key;
    //     if (target) {
    //       target.editable = true;
    //     }
    // },
    save(key) {
      const newData = [...this.data];
      const newCacheData = [...this.cacheData];
      const target = newData.filter((item) => key === item.key)[0];
      const targetCache = newCacheData.filter((item) => key === item.key)[0];
      console.log(target);
      console.log(targetCache);
      if (target && targetCache) {
        delete target.editable;
        this.data = newData;
        Object.assign(targetCache, target);
        this.cacheData = newCacheData;
      }
      this.editingKey = "";
      if(target.type=="个人"){
        this.type1=0
      }else if(target.type=="学校"){
        this.type1=1
      }else{
        this.type1=2
      }
      const params = {
        id: this.editData.key,
        name: this.editData.name,
        // usertype: this.type1,

        institution:this.editData.ins,
        mail: this.editData.email,
      };

      let that = this
      UserModify(params)
        .then((res) => {
          if (res.data.code === 501) {
            // this.$message.error(res.data.message);
            console.log('bug')
            alert(res.data.message)
            
          } else {
            this.$message.info("成功修改");
          }
          console.log(res)
        }).then((res) => {
          that.reload()
        })
        .catch((error) => {
          this.$message.error("无法修改")
          /*todo*/
          // this.$message.error(res.data.message)
          console.log("无法修改");
          alert("修改失败")
        });
      if (target) {
        Object.assign(
          target,
          this.cacheData.filter((item) => key === item.key)[0]
        );
        delete target.editable;searchUser
        this.data = newData;
      }
      console.log('111')
      this.reload()
      this.loadUser()
      // console.log(target.editable
    },
    cancel(key) {
      let that = this
      let promise = new Promise(function (resolve, reject) {
            const newData = [...that.data];
            const target = newData.filter((item) => key === item.key)[0];
            that.editingKey = "";
            if (target) {
              Object.assign(
                  target,
                  that.cacheData.filter((item) => key === item.key)[0]
              );
              delete target.editable;
              that.data = newData;
            }
            resolve()
          }
      )
      promise.then(
          that.reload()
      )
    },
    check_user_info(){
      if(this.user_visible){
        // add user
        if(this.user_info.username == '' ||
        this.user_info.password == '' ||
        this.user_info.email == ''){
              console.log('More Info')
              alert('请填写完整信息')
              return false
        }
      }else if(this.expert_visible){
        // add expert
        if(this.expert_info.username == '' ||
        this.expert_info.password == '' ||
        this.expert_info.email == '' ||
        this.expert_info.name == '' ||
        this.expert_info.organization == '' ||
        this.expert_info.ID_num == ''){
              alert('请填写完整信息')
              return false
        }        
        var arrExp = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];//加权因子
        var arrValid = [1, 0, "X", 9, 8, 7, 6, 5, 4, 3, 2];//校验码
        if (/^\d{17}\d|x$/i.test(this.expert_info.ID_num)) {
          var sum = 0, idx;
          for (var i = 0; i < this.expert_info.ID_num.length - 1; i++) {
              // 对前17位数字与权值乘积求和
              sum += parseInt(this.expert_info.ID_num.substr(i, 1), 10) * arrExp[i];
          }
          // 计算模（固定算法）
          idx = sum % 11;
          // 检验第18为是否与校验码相等
          if (arrValid[idx] == this.expert_info.ID_num.substr(17, 1).toUpperCase()) {
            return true;
          } else {
            alert('身份证格式有误')
            return false;
          }
        } else {
          alert('身份证格式有误')
          return false;
        }
      }else if(this.company_visible){
        // add company
        if(this.company_info.username == '' ||
        this.company_info.password == '' ||
        this.company_info.email == '' ||
        this.company_info.name == '' ||
        this.company_info.address == ''){
              alert('请填写完整信息')
              return false
        }    
      }else{
        console.log('Create Type Error!')
      }
      return true
    },
    adminCreateUser(){
      this.user_visible = true;
      console.log('Admin Create User');
      console.log('user_visible')
      // console.log(this.user_visible)
      // console.log(this.expert_visible)
      // console.log(this.company_visible)
    },
    adminCreateExpert(){
      this.expert_visible = true;
      console.log('Admin Create expert');
      
    },
    adminCreateCompany(){
      this.company_visible = true;
      console.log('Admin Create company');
    },
    handleSubmit(){
      if(!this.check_user_info()){
        return
      }
      console.log('submit')



      if(this.user_visible){
        // add user
        console.log('user_visible')
        console.log(this.user_info)

        adminCreateUserAPI(this.user_info).then((oriRes) => {
            console.log(oriRes)
            if(oriRes.data.code == 410){
              alert('用户名或邮箱已被注册')
            } else if(oriRes.data.code == 501) {
              alert(oriRes.data.message)
              // alert('用户名或邮箱已被注册')
              console.log('用户名或邮箱已被注册')
              
            }else{
              console.log(oriRes)
              this.resetUserInfo()
              this.user_visible = false
            }
        }).catch((error) => {


            console.log(error)
            console.log('error')
        });        

      }else if(this.expert_visible){
        // add expert
        console.log(this.expert_info)
        adminCreateExpertAPI(this.expert_info).then((oriRes) => {
            if(oriRes.data.code == 410){
              alert('用户名或邮箱已被注册')
            }else if(oriRes.data.code == 501) {
              alert(oriRes.data.message)
            }
            else{
              console.log(oriRes)
              this.resetExpertInfo()
              this.expert_visible = false
            }
        }).catch((error) => {
            console.log(error)
        });  

      }else if(this.company_visible){
        // add company
        console.log(this.company_info)
        adminCreateCompanyAPI(this.company_info).then((oriRes) => {
            if(oriRes.data.code == 410){
              alert('用户名或邮箱已被注册')
            }else if(oriRes.data.code == 501) {
              alert(oriRes.data.message)
            }else{
              console.log(oriRes)
              this.resetCompanyInfo()
              this.company_visible = false
            }
        }).catch((error) => {
            console.log(error)
        });  

      }else{
        console.log('Create Type Error!')
      }
    },
    resetUserInfo(){
      this.user_info = {
        username:'',
        password:'',
        email:''
      }
    },
    resetExpertInfo(){
      this.expert_info = {
        username:'',
        password:'',
        email:'',
        name:'',
        organization:'',
        ID_num:''  
      }
    },
    resetCompanyInfo(){
      this.company_info = {
        username:'',
        password:'',
        email:'',
        name:'',
        address:''
      }
    },
    onSearch(){
      this.pagination.current = 1;
      // let encode_text = encodeURIComponent(this.searchText)
      let encode_text = this.searchText
      console.log(encode_text);
      var params = {
          "keyword": encode_text,
          "page_num": this.pagination.current,
          "page_size":20,
      }
      this.selectedType="搜索";
      searchUser(params).then((oriRes) => {
        console.log('searching');
        // console.log(res.data.all_page)
        console.log(oriRes);
        let res = oriRes.data
        console.log(res);
        data.length = 0;
        console.log(data);
        console.log("chazhao")
        console.log(res);

        for (let i = 0; i < res.total; i++) {
          
         data.push({
            name: res.users[i].username,
            password:res.users[i].password,
            // email: res.data[i].email,
            editable: true
          });
        }
        this.totalCnt = res.total;
        
        this.loading = false;
        this.pagination.total += this.totalCnt;
        this.itemKey = Math.random();

      }).catch((error) => {
        console.log(error);
      });
    },
    selectChange(value) {
      if (!this.changeable) {

        alert("请先完成编辑！")
        return
      }
      console.log(value);
      console.log('selectedType=' + this.selectedType);
      this.pagination.current = 1;
      var params = {
          "keyword": "",
          "page_num": this.pagination.current,
          "page_size":20,
      }
      getSelectUser(params).then((oriRes) => {
        console.log(oriRes);
        let res = oriRes.data
        console.log(res);
        data.length = 0;
        console.log(data);
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].type==0) {
            this.type="普通用户"
          } else if (res.data[i].type==1){
            this.type="专家认证中"
          } else if (res.data[i].type==2){
            this.type="企业认证中"
          }else if (res.data[i].type==3){
            this.type="封禁中"
          }else if (res.data[i].type==4){
            this.type="认证专家"
          }else if (res.data[i].type==5){
            this.type="认证企业"
          }
          data.push({
            key: res.data[i].id,
            name: res.data[i].username,
            ins: res.data[i].institution,
            type: this.type,
            email: res.data[i].email,
            editable: false
          });
        }
        
        this.totalCnt = res.data.total_count;
        this.loading = false;
        this.pagination.total = res.page_num;
        this.itemKey = Math.random();
      }).catch((error) => {
        console.log(error);
      });
    }
  },
};
</script>

<style scoped>
.highlight {
  background-color: rgb(255, 192, 105);
  padding: 0px;
}
.editable-row-operations a {
  margin-right: 8px;
}
</style>
