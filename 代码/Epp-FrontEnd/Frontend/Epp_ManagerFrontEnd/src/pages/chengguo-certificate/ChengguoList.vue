<template>
<div>
    <a-card :bordered="false">
        <a-list item-layout="vertical" size="large" :pagination="pagination" :data-source="listData">
            <a-list-item slot="renderItem" key="item.title" slot-scope="item">
                <a-space direction="vertical" slot="extra" width="272" aligh="end" style="margin-right: 20px;">
                    <a-row>
                        <a-col :span="24">
                            <a-button type="text" style="width: 80px" @click="handleShow(item.id)">
                                查看
                            </a-button>
                        </a-col>
                    </a-row>
                    <a-row>
                        <a-col :span="24">
                            <a-popconfirm title="确定通过审核吗？" ok-text="确定" cancel-text="取消" @confirm="handleApply(item.id)">
                                <a-button type="primary" style="width: 80px"> 通过</a-button>
                            </a-popconfirm>
                        </a-col>
                    </a-row>
                    <a-row>
                        <a-col :span="24">
                            <a-popconfirm title="确定拒绝通过吗？" ok-text="确定" cancel-text="取消" @confirm="handleRefuse(item.id)">
                                <a-button type="danger" style="width: 80px"> 拒绝</a-button>
                            </a-popconfirm>
                        </a-col>
                    </a-row>
                </a-space>
                <a-modal v-model="showDetail" title="" @ok="handleOk" width="750px">
                    <ChengguoCard v-if="showDetail" v-bind="post"></ChengguoCard>
                </a-modal>
                <a-list-item-meta :description="item.scholars">
                    <a slot="title" :herf="item.herf">{{ item.result_name }}</a>
                    <a-avatar slot="avatar" shape="square"  :src="item.result_pic"></a-avatar>
                </a-list-item-meta>
                <a style="display: block;" class="textbreak" herf="javascript:void(0)" @click="handleShow(item.id)">
                    成果信息简介：{{ item.abstract | ellipsis }}
                </a>
            </a-list-item>
        </a-list>
    </a-card>
</div>
</template>

<script>
import ChengguoCard from './ChengguoCard.vue';
import {BASE_URL_IP} from "../../services/api";
import { getWorkUnaudited, getWork, WorkApply, WorkRefuse } from '../../services/work';
export default {
    name: "ChengguoList",
    components: {ChengguoCard},
    filters: {
        ellipsis (value) {
            if (!value) return ''
            if (value.length > 130) {
                return value.slice(0,130) + '...'
            }
            return value
        }
    },
    data() {
        return {
            loading: true,
            pageIndex: 1,
            data: [],
            post: {},
            showDetail: false,
            //翻页
            pagination: {
                onChange: (page) => {
                    console.log(page);
                },
                pageSize: 10,
            },
            listData: [
                {
                    // id: 0,
                    // result_name: "成果名称",
                    // create_time: "申请时间：2023-04-04T01:39:28.970Z",
                    // abstract: "成果简介成果简介成果简介成果简介成果简介成果简介成果简介成果简介",
                    // result_pic: "http://127.0.0.1:8000/api/images/202205/02/icons/zkg.jpg"
                }
            ]
        }
    },
    mounted() {
        this.init();
    },
    inject: ['reload'],
    methods: {
        init: async function() {
            this.pagination.current = 1
            this.loadPost();
        },
        loadPost: function () {
            this.loading = true;
            getWorkUnaudited(this.pagination.current).then((res) => {
                console.log(res);
                console.log(res.data.data)
                this.listData.length = 0;
                this.listData = [];
                res.data.data.map((item) => {
                    if(item.state == 0){
                        this.listData.push({
                            id: item.id,
                            result_name: item.title,
                            scholars: item.scholars,
                            field: item.field,
                            result_pic :BASE_URL_IP + '/api/' + item.picture,
                            abstract: item.abstract,
                        })
                    }
                })
                this.loading = false;
                console.log(this.listData);
                console.log(BASE_URL_IP);
            }).catch((error) => {
                console.log(error);
            });
        },
        handleOk(e) {
            this.showDetail = false;
        },
        handleShow: function (id) {
            getWork(id, "get").then((res) => {
                let item = res.data
                this.post = {
                    name: item.expert_name,
                    result_name: item.title,
                    scholars: item.scholars,
                    field: item.field,
                    result_pic :BASE_URL_IP + '/api/' + item.result_pic,
                    work_description: item.abstract,
                };
                this.showDetail = true;
                console.log(this.post);
            }).catch((error) => {
                console.log(error);
            })
        },
        handleRefuse: function (id) {
            WorkRefuse(id, "get").then((res) => {
                console.log(res);
                this.reload();
            }).catch((error) => {
                console.log(error);
                this.reload();
            });
        },
        handleApply: function (id) {
            WorkApply(id, "get").then((res) => {
                console.log(res);
                this.reload();
            }).catch((error) => {
                console.log(error);
                this.reload();
            });
        }
    },
}
</script>

<style scoped>
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