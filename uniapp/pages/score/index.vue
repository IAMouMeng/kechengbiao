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
            <u-row customStyle="margin-top:20px;margin-bottom: 10px;padding:10px 30px;">
                <u-col>
                    <view>
                        <view v-for="item in scoreList">
                            <view class="score-box">
                                <view class="header" :style="{ backgroundColor: mathColor() }">
                                    <view class="title">{{ item.year }} 年 {{ item.semester == '1' ? '上学期' : '下学期' }}</view>
                                </view>
                                <view class="main" v-if="item.exams != null && item.exams.length == 0">
                                    <u-skeleton rows="2" title loading></u-skeleton>
                                </view>
                                <view class="main" v-else-if="item.exams == null">
                                    <view style="width:100%;text-align:center;color:rgb(176,185,189)">暂无数据
                                    </view>
                                </view>

                                <view class="main" v-else>
                                    <view class="info-container">
                                        <view class="item" style="text-align:left;">
                                            <view class="title">当前数据</view>
                                            <view class="data">{{ item.exams.length }} 条</view>

                                        </view>
                                        <view class="item" style="text-align:center;">
                                            <view class="title">总学分</view>
                                            <view class="data">
                                                {{ item.exams.reduce((acc, obj) => {
                                                    const numericValue = parseFloat(obj.exam_credit_points);
                                                    const intValue = isNaN(numericValue) ? 0 : Math.round(numericValue * 100);
                                                    return (acc * 100 + intValue) / 100;
                                                }, 0) }}</view>

                                        </view>
                                        <view class="item" style="text-align:right;">
                                            <view class="title">总绩点</view>
                                            <view class="data">
                                                {{ item.exams.reduce((acc, obj) => {
                                                    const numericValue = parseFloat(obj.exam_gpa);
                                                    const intValue = isNaN(numericValue) ? 0 : Math.round(numericValue * 100);
                                                    return (acc * 100 + intValue) / 100;
                                                }, 0) }}
                                            </view>
                                        </view>
                                    </view>
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
                                        <u-col span="2" textAlign="right">
                                            <view>绩点</view>
                                        </u-col>
                                    </u-row>
                                    <u-divider :hairline="true"></u-divider>
                                    <u-row justify="space-between" v-for="exams in item.exams">
                                        <u-col span="6">
                                            <view>{{ exams.exam_name }} {{ exams.exam_makeup_score ? '【补】' :
                                                exams.exam_regrade_score ? '【修】' : '' }}</view>
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
                                        <u-col span="2" textAlign="right">
                                            <view>{{ exams.exam_gpa }}</view>
                                        </u-col>
                                    </u-row>
                                </view>
                            </view>
                            <u-divider color="#fa3534" half-width="200" border-color="#6d6d6d"></u-divider>
                        </view>
                    </view>
                </u-col>
            </u-row>
            <view class="info">数据来源：教务系统</view>
        </view>
    </view>
</template>
<script>
import { getExamsList, updateExamsList } from '../../common/api';

export default {
    data() {
        return {
            loading: false,
            updateTime: '',
            scoreList: []
        }
    },
    onLoad() {
        this.checkAuth()
    },
    beforeMount() {
        this.getScoreData();
    },
    methods: {
        getScoreData() {
            let self = this;
            uni.getStorage({
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

            this.scoreList = [];
            this.getScoreData();
            this.loading = false;
        },
        mathColor() {
            const randomR = Math.random() * 120;
            const randomG = Math.random() * 150;
            const randomB = Math.random() * 256;
            return `rgba(${randomR},${randomG},${randomB},0.5)`;
        }
    },
}
</script>
<style lang="scss">
.score-box {
    width: 100%;
    margin-bottom: 10px;
    background-color: rgb(255, 255, 255);
    border-radius: 10px;
    box-sizing: border-box;
    color: #123c50;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 0px 5px 0px, rgba(0, 0, 0, 0.1) 0px 0px 1px 0px;
    overflow: hidden;
}

.score-box .header {
    width: 100%;
    height: 50px;
    padding: 15px;
    box-sizing: border-box;
    background-color: rgb(59, 164, 253);
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}

.score-box .main {
    width: 100%;
    color: rgb(96, 98, 102);
    padding: 15px;
    box-sizing: border-box;
}

.score-box .header .title {
    font-size: 15px;
    font-weight: bold;
    color: #ffffff;
}

.score-box .info-container {
    width: 100%;
    height: 60px;
    display: flex;
}

.score-box .info-container .item {
    flex: 1;
}

.score-box .info-container .item .title {
    color: #123c50;
    font-size: 12px;
}

.score-box .info-container .item .data {
    color: #303133;
    font-size: 15px;
    font-weight: bolder;
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
    color: rgb(96, 98, 102);
    text-align: center;
    padding-bottom: 10px;
}

</style>