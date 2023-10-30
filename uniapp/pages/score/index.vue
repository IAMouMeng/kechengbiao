<template>
    <view>
        <view v-if="loading">
            <u-loading-page :loading="loading" loading-text="数据更新中" iconSize="32" loadingColor="blue"
                fontSize="15"></u-loading-page>
        </view>
        <view v-else>
            <u-row justify="space-between"
                customStyle="margin-top:20px;margin-bottom: 10px;padding-left:20px;padding-right:25px;">
                <u-col span="6">
                    <view style="padding-left:10px;color:#8f9ca2;font-size:10px;float:left;">
                        最近更新于 {{ updateTime }}
                    </view>
                </u-col>
                <u-col span="6">
                    <view style="float:right;margin-right:5px;">
                        <u-button type="primary" :plain="true" @click="updateScoreData" size="mini" :hairline="true"
                            text="更新"></u-button>
                    </view>
                    <!-- <view style="float:right;margin-right:10px;">
                        <u-button type="primary" :plain="true" size="mini" :hairline="true" text="导出"></u-button>
                    </view> -->
                </u-col>
            </u-row>
            <u-row customStyle="margin-top:20px;margin-bottom: 10px;padding-left:20px;padding-right:20px;">
                <u-col>
                    <view>
                        <u-steps :dot="true" current="0" direction="column">
                            <u-steps-item :title="item.year + '年'" :activeIcon="true" v-for="item in scoreList">
                                <view slot="desc"><text class="title">{{ item.semester == '1' ? '上学期' : '下学期' }}</text>
                                    <view class="score-container">
                                        <view v-if="item.exams != null && item.exams.length == 0">
                                            <u-skeleton rows="2" title loading></u-skeleton>
                                        </view>
                                        <view v-else-if="item.exams == null">
                                            <view class="score-box">
                                                <view style="width:100%;text-align:center;color:rgb(176,185,189)">暂无数据
                                                </view>
                                            </view>

                                        </view>
                                        <view class="score-box" v-else>
                                            <u-row justify="space-between">
                                                <u-col span="6">
                                                    <view>科目</view>
                                                </u-col>
                                                <u-col span="2" textAlign="center">
                                                    <view>学分</view>
                                                </u-col>
                                                <u-col span="2" textAlign="center">
                                                    <view>成绩</view>
                                                </u-col>
                                                <u-col span="2" textAlign="center">
                                                    <view>绩点</view>
                                                </u-col>
                                            </u-row>
                                            <u-divider :hairline="true"></u-divider>
                                            <u-row justify="space-between" v-for="exams in item.exams">
                                                <u-col span="6">
                                                    <view>{{ exams.exam_name }} {{ exams.exam_regrade_score ? '(补)' :
                                                        exams.exam_regrade_score ? '(修)' : '' }}</view>
                                                </u-col>
                                                <u-col span="2" textAlign="center">
                                                    <view>{{ exams.exam_credit_points }}</view>
                                                </u-col>
                                                <u-col span="2" textAlign="center">
                                                    <view>{{ exams.exam_regrade_score ? exams.exam_regrade_score + '分' :
                                                        exams.exam_regrade_score ? exams.exam_regrade_score + '分' :
                                                            isNaN(exams.exam_score) ? exams.exam_score : exams.exam_score +
                                                                '分' }}</view>
                                                </u-col>
                                                <u-col span="2" textAlign="center">
                                                    <view>{{ exams.exam_gpa }}</view>
                                                </u-col>
                                            </u-row>
                                        </view>
                                    </view>
                                </view>
                            </u-steps-item>
                        </u-steps>
                    </view>
                </u-col>
            </u-row>
            <view class="info">数据来源：教务系统</view>
        </view>
    </view>
</template>
<script>
import { getExamsList, updateExamsList,checkUserToken } from '../../common/api';

export default {
    data() {
        return {
            loading: false,
            updateTime: '',
            scoreList: []
        }
    },
    onLoad(){
		this.checkAuth()
	},
    async beforeMount() {
        await this.getScoreData();
    },
    mounted() {
        this.$forceUpdate();
    },
    methods: {
        async getScoreData() {
            let self = this;
            await uni.getStorage({
                key: 'year',
                success: async function (res) {
                    let dateNow = new Date();
                    let yearNow = dateNow.getFullYear();
                    let monthNow = dateNow.getMonth() + 1;

                    for (let year = yearNow; year >= res.data; year--) {
                        let semester = ["2", "1"];
                        if (year == yearNow && monthNow >= 6 && monthNow <= 12) {
                            semester.splice(0, 1);

                        }
                        semester.forEach((item) => {
                            self.scoreList.push({
                                "year": year,
                                "semester": item,
                                "exams": []
                            })
                        })
                    }
                    for (const [key, value] of Object.entries(self.scoreList)) {
                        await getExamsList(
                            `${value.year}-${value.year + 1}`,
                            value.semester
                        ).then(res => {
                            self.updateTime = res.student.exams_updatetime != null ? res.student.exams_updatetime : '[暂未更新]';
                            self.scoreList[key].exams = res.exams.data.length == 0 ? null : res.exams.data;
                        })
                    }
                }
            });
        },
        async updateScoreData() {
            this.loading = true;
            for (let i = 0; i < this.scoreList.length; i++) {
                await updateExamsList(
                    `${this.scoreList[i].year}-${this.scoreList[i].year + 1}`,
                    this.scoreList[i].semester
                )
            }
            this.scoreList = []
            await this.getScoreData();
            this.loading = false;
        }
    },
}
</script>
<style lang="scss">
.score-container {
    display: flex;
    flex-direction: column;
    padding-right: 10%;
    padding-bottom: 10px;
}

.title {
    font-size: 12px;
    color: #8f9ca2;
    margin-bottom: 8px;
    display: flex;
    flex-direction: row;
}

.score-box {
    width: 100%;
    background-color: rgba(113, 173, 225, 0.1);
    border-radius: 5px;
    padding: 10px;
    color: #123c50;
    box-shadow: rgba(0, 0, 0, 0.08) 0px 4px 12px;
}

.score-box .u-row {
    margin-top: 3px;
}

.score-box .u-col {
    text-align: center;
    font-size: 10px;
}

.info {
    font-size: 10px;
    color: #8f9ca2;
    padding-top: 10px;
    padding-bottom: 10px;
    text-align: center;
}</style>