(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-af1c8dee"],{"07a6":function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return i}));var a=n("b775"),o=n("7424"),c=function(e){var t="".concat(o["BASE_URL_IP"],"/api/manage/commentReport");return Object(a["e"])(t,a["a"].GET,e)},i=function(e,t){var n="".concat(o["BASE_URL_IP"],"/api/manage/judgeCmtRpt");return Object(a["e"])(n,a["a"].POST,e)}},7594:function(e,t,n){"use strict";n.r(t);var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("a-card",{attrs:{bordered:!1}},[n("a-table",{attrs:{"data-source":e.data,columns:e.columns},scopedSlots:e._u([{key:"operation",fn:function(t,a){return[n("div",[n("span",[n("a-modal",{attrs:{title:"举报审核",width:"750px","mask-closable":!1,mask:!0,maskStyle:{opacity:"0.08",background:"#000000",animation:"none"}},on:{ok:function(t){return e.handleOk()}},model:{value:e.showDetail,callback:function(t){e.showDetail=t},expression:"showDetail"}},[n("a-card",{attrs:{bordered:!1,"dis-hover":""}},[n("a-row",[e._v("内容："+e._s(e.selectData.content))]),n("br"),n("a-row",[e._v("举报人："+e._s(e.selectData.user))]),n("br"),n("a-row",[e._v("日期："+e._s(e.selectData.date))]),n("br")],1)],1)],1)])]}},{key:"action",fn:function(t,a){return[n("a-button",{attrs:{type:"primary"},on:{click:function(t){return e.handleProcess(a.id)}}},[e._v("回复")])]}},{key:"expandedRowRender",fn:function(t){return[n("p",{staticStyle:{margin:"0"}},[e._v(" 举报内容："+e._s(t.content)+" ")]),n("br"),n("div",{staticClass:"detail"},[n("p",{staticStyle:{margin:"0"}},[e._v(" 评论人："+e._s(t.comment.user.user_name)+" ")]),n("p",{staticStyle:{margin:"0"}},[e._v(" 评论文章："+e._s(t.comment.paper.title)+" ")]),n("p",{staticStyle:{margin:"0"}},[e._v(" 评论内容："+e._s(t.comment.content)+" ")]),n("a-button",{attrs:{type:"danger"},on:{click:function(n){return e.deleteComment(t.comment.comment_id)}}},[e._v("删除评论")])],1)]}}])}),n("a-modal",{attrs:{title:"举报信息回复"},on:{ok:e.handleReplyOk,cancel:e.handleReplyCancel},model:{value:e.showReplyModalVisible,callback:function(t){e.showReplyModalVisible=t},expression:"showReplyModalVisible"}},[n("a-textarea",{attrs:{placeholder:"请输入回复内容",rows:"4"},model:{value:e.replyContent,callback:function(t){e.replyContent=t},expression:"replyContent"}})],1)],1)},o=[],c=n("1da1"),i=(n("96cf"),n("07a6")),s=[{title:"内容",dataIndex:"content",scopedSlots:{customRender:"content"},width:100},{title:"举报人",dataIndex:"user",scopedSlots:{customRender:"user"},width:100},{title:"日期",dataIndex:"date",scopedSlots:{customRender:"date"},width:100},{title:"操作",dataIndex:"action",scopedSlots:{customRender:"action"},width:150}],r=[],l={name:"handledFeedbbackList",inject:["reload"],components:{},data:function(){return{data:r,columns:s,showDetail:!1,reply:"",selectData:{},showReplyModalVisible:!1,replyContent:"",selectedRecord:null}},mounted:function(){this.init()},methods:{init:function(){var e=Object(c["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:this.loadNeed();case 1:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}(),loadNeed:function(){r.length=0,Object(i["a"])({mode:1}).then((function(e){for(var t=e.data.reports,n=0;n<t.length;n++)r.push({id:t[n].id,content:t[n].content,user:t[n].user.user_name,date:t[n].date,comment:t[n].comment})})).catch((function(e){}))},handleOk:function(){this.showDetail=!1;var e={feedback_id:this.selectData.feedback_id,message:this.reply};Object(i["b"])(e,"post").then((function(e){})).catch((function(e){})),this.reload()},handleProcess:function(e){this.selectedRecord=e,this.replyContent="",this.showReplyModalVisible=!0},handleReplyOk:function(){var e=this;this.replyContent&&Object(i["b"])({id:this.selectedRecord,judgment:this.replyContent}).then((function(){e.showReplyModalVisible=!1,e.loadNeed()})).catch((function(e){}))},handleReplyCancel:function(){this.showReplyModalVisible=!1},deleteComment:function(e){var t=this;deleteCommentApi(e).then((function(){t.loadNeed()})).catch((function(e){}))}}},d=l,u=(n("9ee7"),n("2877")),p=Object(u["a"])(d,a,o,!1,null,"576e0fa8",null);t["default"]=p.exports},"9ee7":function(e,t,n){"use strict";n("a9ea")},a9ea:function(e,t,n){}}]);