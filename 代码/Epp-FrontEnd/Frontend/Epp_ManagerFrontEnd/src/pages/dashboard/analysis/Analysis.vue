<template>
  <page-layout :avatar="currUser.avatar">
    <div slot="headerContent">
      <div class="title">
        {{ welcome.timeFix[lang] }}，{{ currUser.name }}，{{
          welcome.message[lang]
        }}
      </div>
      <div>{{ currUser.position[lang] }}</div>
    </div>
    <template slot="extra">
      <head-info class="split-right" title="用户数量" :content="user" />
      <head-info class="split-right" title="解读数量" :content="paper" />
      <head-info class="split-right" title="解读访问量" :content="visit" />
    </template>
    <div :class="['analysis', layout, pageWidth]">
      <!--
    <a-row style="margin-top: 0" :gutter="[24, 24]">
      <a-col :sm="24" :md="12" :xl="6">
        <chart-card :loading="loading" :title="$t('totalSales')" total="￥ 189,345">
          <a-tooltip :title="$t('introduce')" slot="action">
            <a-icon type="info-circle-o" />
          </a-tooltip>
          <div>
            <trend style="margin-right: 16px" :term="$t('wow')" :percent="12" :is-increase="true" :scale="0" />
            <trend :term="$t('dod')" :target="100" :value="89" :scale="0" />
          </div>
          <div slot="footer">{{$ta('daily|sales', 'p')}}<span> ￥234.56</span></div>
        </chart-card>
      </a-col>

      <a-col :sm="24" :md="12" :xl="6">
        <chart-card :loading="loading" :title="$t('visits')" total="￥ 189,345">
          <a-tooltip :title="$t('introduce')" slot="action">
            <a-icon type="info-circle-o" />
          </a-tooltip>
          <div>
            <mini-area />
          </div>
          <div slot="footer">{{$ta('daily|visits', 'p')}}<span> 123,4</span></div>
        </chart-card>
      </a-col>
      <a-col :sm="24" :md="12" :xl="6">
        <chart-card :loading="loading" :title="$t('payments')" total="￥ 189,345">
          <a-tooltip :title="$t('introduce')" slot="action">
            <a-icon type="info-circle-o" />
          </a-tooltip>
          <div>
            <mini-bar />
          </div>
          <div slot="footer">{{$t('conversion')}} <span>60%</span></div>
        </chart-card>
      </a-col>
      <a-col :sm="24" :md="12" :xl="6">
        <chart-card :loading="loading" :title="$t('operating')" total="73%">
          <a-tooltip :title="$t('introduce')" slot="action">
            <a-icon type="info-circle-o" />
          </a-tooltip>
          <div>
            <mini-progress target="90" percent="78" color="#13C2C2" height="8px"/>
          </div>
          <div slot="footer" style="white-space: nowrap;overflow: hidden">
            <trend style="margin-right: 16px" :term="$t('wow')" :percent="12" :is-increase="true" :scale="0" />
            <trend :term="$t('dod')" :target="100" :value="89" :scale="0" />
          </div>
        </chart-card>
      </a-col>
    </a-row>
    -->
      <a-card
        :loading="loading"
        style="margin-top: 24px"
        :bordered="false"
        :body-style="{ padding: '24px' }"
      >
        <div class="salesCard">
          <a-tabs
            default-active-key="1"
            size="large"
            :tab-bar-style="{ marginBottom: '24px', paddingLeft: '16px' }"
          >
            <div class="extra-wrap" slot="tabBarExtraContent">
              <!--
            <div class="extra-item">
              <a>{{$t('day')}}</a>
              <a>{{$t('week')}}</a>
              <a>{{$t('month')}}</a>
              <a>{{$t('year')}}</a>
            </div>
            <a-range-picker :style="{width: '256px'}"></a-range-picker>
            --></div>

            <a-tab-pane :tab="$t('visits')" key="1"
              ><a-row>
                <a-col :xl="16" :lg="12" :md="12" :sm="24" :xs="24">
                  <bar :title="$ta('visits|trend', 'p')" />
                </a-col>
                <a-col :xl="8" :lg="12" :md="12" :sm="24" :xs="24">
                  <ranking-list
                    :title="$ta('stores|visits|ranking', 'p')"
                    :list="rankList"
                  />
                </a-col> </a-row
            ></a-tab-pane>
          </a-tabs>
        </div>
      </a-card>
      <a-row style="margin: 0 -12px">
        <a-col
          style="padding: 0 12px"
          :xl="12"
          :lg="24"
          :md="24"
          :sm="24"
          :xs="24"
        >
          <a-card
            :loading="loading"
            :bordered="false"
            style="margin-top: 24px"
            :title="$t('search')"
          >
            <hot-search />
            <!--热门搜索-->
          </a-card>
        </a-col>
        <a-col
          style="padding: 0 12px"
          :xl="12"
          :lg="24"
          :md="24"
          :sm="24"
          :xs="24"
        >
          <a-card
            :loading="loading"
            :bordered="false"
            style="margin-top: 24px;"
            :title="$t('proportion')"
          >
            <sales-data />
            <!--解读占比-->
          </a-card>
        </a-col>
      </a-row>
    </div>
  </page-layout>
</template>

<script>
// import ChartCard from '../../../components/card/ChartCard'
// import MiniArea from '../../../components/chart/MiniArea'
// import MiniBar from '../../../components/chart/MiniBar'
// import MiniProgress from '../../../components/chart/MiniProgress'
import PageLayout from "@/layouts/PageLayout";
import HeadInfo from "@/components/tool/HeadInfo";
import { mapState } from "vuex";
import Bar from "../../../components/chart/Bar";
import RankingList from "../../../components/chart/RankingList";
import HotSearch from "./HotSearch";
import { request, METHOD } from "@/utils/request";
import SalesData from "./SalesData";
import {getUserAll, getvis, recommend, getPaperAll } from "@/services/dataSource";
// import Trend from '../../../components/chart/Trend'

const rankList = [];

export default {
  name: "Analysis",
  i18n: require("./i18n"),
  data() {
    return {
      user: "597",
      visit: "300",
      paper: "20",
      rankList,
      loading: true,
      projects: [],
      activities: [],
      teams: [],
      welcome: {
        timeFix: "",
        message: "",
      },
    };
  },
  computed: {
    ...mapState("setting", ["layout", "pageWidth"]),
    ...mapState("account", { currUser: "user" }),
    ...mapState("setting", ["lang"]),
  },
  created() {
    setTimeout(() => (this.loading = !this.loading), 1000),
      request("/user/welcome", METHOD.GET).then(
        (res) => (this.welcome = res.data)
      ),
      request("/work/activity", METHOD.GET).then(
        (res) => (this.activities = res.data)
      );
    request("/work/team", METHOD.GET).then((res) => (this.teams = res.data));
    request("/project", METHOD.GET).then((res) => {
      this.projects = res.data;
    });
    recommend().then((res) => {
      // console.log(res)
      for (let i = 0; i < 8; i++) {
        rankList.push({
          name: res.data[i].title,
          total: res.data[i].viscount,
        });
      }
    });
    getvis().then((res) => {
      this.visit = res.data.totcount;
    });
    getPaperAll().then((res) => {
      this.paper = res.data.length;
    });
    getUserAll().then((res) => {
      this.user = res.data.count;
    });
  },
  components: { SalesData, HotSearch, RankingList, Bar, PageLayout, HeadInfo },
};
</script>

<style lang="less" scoped>
.extra-wrap {
  .extra-item {
    display: inline-block;
    margin-right: 24px;
    a:not(:first-child) {
      margin-left: 24px;
    }
  }
}
@media screen and (max-width: 992px) {
  .extra-wrap .extra-item {
    display: none;
  }
}
@media screen and (max-width: 576px) {
  .extra-wrap {
    display: none;
  }
}
</style>
