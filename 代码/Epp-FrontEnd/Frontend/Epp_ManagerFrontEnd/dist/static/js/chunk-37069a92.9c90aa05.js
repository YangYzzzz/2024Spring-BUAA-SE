(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-37069a92"],{"51d2":function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("a-card",{attrs:{"body-style":{padding:"24px 32px"},bordered:!1}},[a("a-form",{attrs:{form:e.form},on:{submit:e.handleSubmit}},[a("a-form-item",e._b({attrs:{label:"E-mail",labelCol:{span:7},wrapperCol:{span:10}}},"a-form-item",e.formItemLayout,!1),[a("a-input",{directives:[{name:"decorator",rawName:"v-decorator",value:["email",{rules:[{type:"email",message:"The input is not valid E-mail!"},{required:!0,message:"Please input your E-mail!"}]}],expression:"[\n          'email',\n          {\n            rules: [\n              {\n                type: 'email',\n                message: 'The input is not valid E-mail!',\n              },\n              {\n                required: true,\n                message: 'Please input your E-mail!',\n              },\n            ],\n          },\n        ]"}]})],1),a("a-form-item",e._b({attrs:{label:"Password","has-feedback":"",labelCol:{span:7},wrapperCol:{span:10}}},"a-form-item",e.formItemLayout,!1),[a("a-input",{directives:[{name:"decorator",rawName:"v-decorator",value:["password",{rules:[{required:!0,message:"Please input your password!"},{validator:e.validateToNextPassword}]}],expression:"[\n          'password',\n          {\n            rules: [\n              {\n                required: true,\n                message: 'Please input your password!',\n              },\n              {\n                validator: validateToNextPassword,\n              },\n            ],\n          },\n        ]"}],attrs:{type:"password"}})],1),a("a-form-item",e._b({attrs:{label:"Confirm Password","has-feedback":"",labelCol:{span:7},wrapperCol:{span:10}}},"a-form-item",e.formItemLayout,!1),[a("a-input",{directives:[{name:"decorator",rawName:"v-decorator",value:["confirm",{rules:[{required:!0,message:"Please confirm your password!"},{validator:e.compareToFirstPassword}]}],expression:"[\n          'confirm',\n          {\n            rules: [\n              {\n                required: true,\n                message: 'Please confirm your password!',\n              },\n              {\n                validator: compareToFirstPassword,\n              },\n            ],\n          },\n        ]"}],attrs:{type:"password"},on:{blur:e.handleConfirmBlur}})],1),a("a-form-item",e._b({attrs:{labelCol:{span:7},wrapperCol:{span:10}}},"a-form-item",e.formItemLayout,!1),[a("span",{attrs:{slot:"label"},slot:"label"},[e._v(" Nickname "),a("a-tooltip",{attrs:{title:"What do you want others to call you?"}},[a("a-icon",{attrs:{type:"question-circle-o"}})],1)],1),a("a-input",{directives:[{name:"decorator",rawName:"v-decorator",value:["nickname",{rules:[{required:!0,message:"Please input your nickname!",whitespace:!0}]}],expression:"[\n          'nickname',\n          {\n            rules: [\n              {\n                required: true,\n                message: 'Please input your nickname!',\n                whitespace: true,\n              },\n            ],\n          },\n        ]"}]})],1),a("a-form-item",e._b({staticStyle:{"margin-top":"24px"},attrs:{wrapperCol:{span:10,offset:7}}},"a-form-item",e.tailFormItemLayout,!1),[a("a-button",{attrs:{type:"primary","html-type":"submit"}},[e._v(" Register ")])],1)],1)],1)},s=[],i=(a("d3b7"),a("d81d"),a("99af"),a("93d6")),o={name:"BasicForm",i18n:a("b368"),data:function(){return{confirmDirty:!1,autoCompleteResult:[],formItemLayout:{labelCol:{xs:{span:24},sm:{span:8}},wrapperCol:{xs:{span:24},sm:{span:16}}},tailFormItemLayout:{wrapperCol:{xs:{span:24,offset:0},sm:{span:16,offset:8}}}}},beforeCreate:function(){this.form=this.$form.createForm(this,{name:"register"})},methods:{handleSubmit:function(e){var t=this;e.preventDefault(),this.form.validateFieldsAndScroll((function(e,a){if(!e)return new Promise((function(e,t){Object(i["c"])("post",{username:a.userName,password:a.password,email:a.email}).then((function(t){e()})).catch((function(e){t(e)}))}));t.$Message.error("注册失败!")}))},handleConfirmBlur:function(e){var t=e.target.value;this.confirmDirty=this.confirmDirty||!!t},compareToFirstPassword:function(e,t,a){var r=this.form;t&&t!==r.getFieldValue("password")?a("Two passwords that you enter is inconsistent!"):a()},validateToNextPassword:function(e,t,a){var r=this.form;t&&this.confirmDirty&&r.validateFields(["confirm"],{force:!0}),a()},handleWebsiteChange:function(e){var t;t=e?[".com",".org",".net"].map((function(t){return"".concat(e).concat(t)})):[],this.autoCompleteResult=t}},computed:{desc:function(){return this.$t("pageDesc")}}},n=o,l=a("2877"),u=Object(l["a"])(n,r,s,!1,null,"6da3ce2a",null),c=u.exports;t["default"]=c},b368:function(e,t){e.exports={messages:{CN:{pageDesc:"填写相关信息并直接创建用户",title:"标题",titleInput:"给目标起个名字",date:"起止日期",describe:"目标描述",describeInput:"请输入你阶段性工作目标",metrics:"衡量标准",metricsInput:"请输入衡量标准",customer:"客户",customerInput:"请描述你服务的客户，内部客户直接 @姓名／工号",critics:"邀评人",criticsInput:"请直接 @姓名／工号，最多可邀请 5 人",weight:"权重",disclosure:"目标公开",disclosureDesc:"客户、邀评人默认被分享",public:"公开",partially:"部分公开",private:"不公开",submit:"提交",save:"保存",colleague1:"同事甲",colleague2:"同事乙",colleague3:"同事丙"},HK:{pageDesc:"表單頁用於向用戶收集或驗證信息，基礎表單常見於數據項較少的表單場景。",title:"標題",titleInput:"給目標起個名字",date:"起止日期",describe:"目標描述",describeInput:"請輸入你階段性的工作目標",metrics:"衡量標準",metricsInput:"請輸入衡量標準",customer:"客戶",customerInput:"請描述你服務的客戶，內部客戶直接 @姓名／工號",critics:"邀評人",criticsInput:"請直接 @姓名／工號，最多可邀請 5 人",weight:"圈中人",disclosure:"目標公開",disclosureDesc:"客戶、邀評人默認被分享",public:"公開",partially:"部分公開",private:"不公開",submit:"提交",save:"保存",colleague1:"同事甲",colleague2:"同事乙",colleague3:"同事丙"},US:{pageDesc:"Form pages are used to collect or verify information to users, and basic forms are common in scenarios where there are fewer data items.",title:"Title",titleInput:"Give the target a name",date:"Start and end date",describe:"Goal description",describeInput:"Please enter your work goals",metrics:"Metrics",metricsInput:"Please enter a metric",customer:"Customer",customerInput:"Please describe your customer service, internal customers directly @ Name / job number",critics:"Inviting critics",criticsInput:"Please direct @ Name / job number, you can invite up to 5 people",weight:"Weight",disclosure:"Target disclosure",disclosureDesc:"Customers and invitees are shared by default",public:"Public",partially:"Partially public",private:"Private",submit:"Submit",save:"Save",colleague1:"Colleague A",colleague2:"Colleague B",colleague3:"Colleague C"}}}}}]);